from slope_model import binom_lmm,binom_lmm_init,SlopesModel
import save_model as sv
import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
import numpy as np
import time
import os.path as op

execfile(op.join('preprocessing','files.txt'))

# choose the largest reasonable variation.
# a value of 5 on the logsitic scale moves us from 50% to 99% accuracy
# or from 50% to 1% accuracy.
population_mean = 5
population_SD = 5

# From the 50% level, a value of 1 along the logistic scale
# moves us to ~75%, i.e.  (1/(1+exp(-1))).
# Limiting this variation within a relatively plausible range leads to a more
# conservative estimate as it shrinks values closer to 0, mitigating
# the effect of outliers.
population_mean_SD_by_id = 1

model_type_groups = {
  'standard_model':
  ['correct ~ 0',
   {'grouping': ['regimen'],
    'formula': 'day * foil_label - 1',
    'group_formula': '1',
    'mean_prior': population_SD,
    'var_prior': population_mean_SD_by_id},
   {'grouping': ['sid'],
    'formula': 'day * foil_label - 1',
    'var_prior': population_mean_SD_by_id}],

  'musician_model':
  ['correct ~ 0',
   {'grouping': ['sid'],
    'formula': 'day * foil_label - 1',
    'group_formula': '1+experience',
    'mean_prior': population_SD,
    'var_prior': population_mean_SD_by_id},
   {'grouping': ['regimen'],
    'formula': 'day * foil_label - 1',
    'var_prior': population_mean_SD_by_id}],
}


def load_df(query=None):
  df = pd.read_csv(op.join('preprocessing','data',discrim_data))

  # merge with demographic, musical experience
  dem = pd.read_excel(op.join('data','demographics.xlsx'),'Sheet1')
  dem['experience'] = np.max([dem.music,dem.dancevoice],axis=0)
  df = df.join(dem.set_index(['regimen','sid']).experience,on=['regimen','sid'])

  if query is not None:
    df = df.query(query)
  #ispretest = (df.block_index < 3) & (df.day == 1)
  #df = df[~ispretest & df.correct.notnull() & (df.condition == '4th')]

  # this is what brings us down to 23 participants...
  # looking at what's going on with the following code
  # df.query('day == 1').groupby('sid').head(1)
  df = df[df.condition.isin(['4th','4th_fam'])]

  cols = ['sid','regimen','day','foil_label','pretest','experience']
  df.sort_values(by=['sid','regimen'],inplace=True)

  dfs = df.groupby(cols).correct.sum().reset_index()
  dfc = df.groupby(cols).correct.count().reset_index()
  dfs['total'] = dfc.correct

  dfs['meanpre'] = float('NaN')
  dfs.set_index('sid',inplace=True)
  for sid,group in dfs.groupby(level='sid'):
    dfs.ix[sid,'meanpre'] = dfs.ix[sid].pretest.mean()
  dfs.reset_index(inplace=True)

  return df,dfs


def run_slopes_model(model_type,data=None,iters=5,warmup=2,chains=1,cache_file=None):
  if data is None:
    df,dfs = load_df()
  else:
    df,dfs = data

  simple_fit = smf.glm(formula='correct.astype(int) ~ 1',
                       data=df,family=sm.families.Binomial()).fit()
  mean_init = simple_fit.params

  error_scale = dfs.total.min()
  mean_model = model_type_groups[model_type][0]

  model = binom_lmm(mean_model,'total',dfs,error_prior=error_scale,
                    mean_prior=population_mean,mean_init=mean_init,
                    iters=iters,warmup=warmup,chains=chains,
                    groups=model_type_groups[model_type][1:])

  if cache_file:
    cache_file = cache_file+"_"+time.strftime("%Y-%m-%d_%H.%M.%S")+'.h5'
    print "Created "+cache_file
    sv.write_samples(model.fit.extract(),cache_file)
    print model.fit

  return model


def load_slopes_model(model_type,cache_file,data=None):
  if data is None:
    _,df = load_df()
  else:
    _,df = data

  init = binom_lmm_init(model_type_groups[model_type][0],'total',df,
                        model_type_groups[model_type][1:])

  samples = sv.read_samples(cache_file)

  return SlopesModel(samples,init)
