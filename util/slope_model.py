import scipy
import numpy as np
import pandas as pd
import patsy
import save_model as sv
import util.sample_stats as ss
import os.path as op

model1 = sv.load_model(op.join('util','mixed.identified1'))
model2 = sv.load_model(op.join('util','mixed.identified2'))
model3 = sv.load_model(op.join('util','mixed.identified3'))

class SlopesInit:
  def __init__(self,mean_formula,countvar,groups,df,y,A,gdf,gg,group_keys,B,G):
    self.mean_formula = mean_formula
    self.countvar = countvar
    self.groups = groups
    self.df = df
    self.y = y
    self.A = A
    self.gdf = gdf
    self.gg = gg
    self.group_keys = group_keys
    self.B = B
    self.G = G


class SlopesModel:
  def __init__(self,fit,init):
    self.fit = fit
    self.init = init

def unique_rows(a):
    order = np.lexsort(a.T)
    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1)
    return a[ui]


def _organize_group_labels(grouped):
    group_labels = np.array(grouped.grouper.labels).T
    unique_labels = unique_rows(group_labels)
    group_index_map = {tuple(labels): i
                       for i,labels in enumerate(unique_labels)}

    group_indices = np.array([group_index_map[tuple(labels)]
                              for labels in group_labels])

    group_keys = pd.DataFrame([{grouped.grouper.names[j]:
                                grouped.grouper.levels[j][labels[j]]
                                for j in range(len(labels))}
                               for labels in unique_labels])
    return group_indices,group_keys

def _setup_groups(df,groups):
    group_df = df.groupby(groups)
    group_indices,group_keys = _organize_group_labels(group_df)

    return group_df.head(1),group_indices,group_keys

def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def predict(model,df=None,marginalize=[],randomize=[],condition={},use_dataframe=False):
  if df is not None and df is not model.init.df:
    df = df.copy()
    df['correct'] = 0

    init = binom_lmm_init(model.init.mean_formula,model.init.countvar,
                          df,model.init.groups,marginalize=marginalize)
    A = init.A
    B = init.B
    G = init.G
    gg = init.gg
  else:
    G = model.init.G
    A = model.init.A
    B = model.init.B
    gg = model.init.gg

  if A.shape[1] > 0:
    # p = np.einsum('ij,kj->ik', A,model.fit['alpha'][:, np.newaxis])
    print "Fixed coefficients are not supported in this implementation, define "
    print "an additional group instead."
  else:
    p = 0

  if 0 in marginalize:
    p += (np.einsum('ik,jlk->ij',B[0],model.fit['beta_1']) /
          model.fit['beta_1'].shape[1])
  elif 0 in randomize:
    # samples, groups, predictors
    mean_1 = np.einsum('ik,jkh->jih',G,model.fit['gamma_1'])
    # samples, groups, predictors
    z_1 = np.random.normal(size=(mean_1.shape[1],mean_1.shape[2]))
    cov_1 = np.einsum('ij,ijk,hj->ihj',model.fit['tau_1'],
                      model.fit['L_Omega_1'],z_1)
    p += np.einsum('ik,jik->ij',B[0],(mean_1 + cov_1)[:,gg[0],:])
  else:
    p += np.einsum('ik,jik->ij',B[0],model.fit['beta_1'][:,gg[0],:])

  if 1 in marginalize:
    p += (np.einsum('ik,jlk->ij',B[1],model.fit['beta_2']) /
          model.fit['beta_2'].shape[1])
  elif 1 in randomize:
    z_2 = np.random.normal(gg[1].unique(),model.fit['z_2'].shape[1])
    beta_2 = np.einsum('ij,ijk,hj->ihj',model.fit['tau_2'],
                      model.fit['L_Omega_2'],z_2)
    p += np.einsum('ij,jik->ij',B[1],beta_2[:,gg[1],:])
  elif len(model.init.B) >= 2:
    p += np.einsum('ik,jik->ij',B[1],model.fit['beta_2'][:,gg[1],:])

  if 2 in marginalize:
    p += (np.einsum('ik,jlk->ij',B[2],model.fit['beta_3']) /
          model.fit['beta_3'].shape[1])
  elif 2 in randomize:
    z_2 = np.random.normal(gg[2].unique(),model.fit['z_3'].shape[1])
    beta_2 = np.einsum('ij,ijk,hj->ihj',model.fit['tau_3'],
                      model.fit['L_Omega_3'],z_2)
    p += np.einsum('ij,jik->ij',B[2],beta_2[:,gg[2],:])
  elif len(model.init.B) >= 3:
    p += np.einsum('ik,jik->ij',B[2],model.fit['beta_3'][:,gg[2],:])

  p = 1 / (1 + np.exp(-p))

  if use_dataframe:
    dfp = df.copy()
    dfp = dfp.iloc[np.repeat(np.arange(p.shape[0]),p.shape[1]),:]
    dfp['sample'] = np.tile(np.arange(p.shape[1]),p.shape[0])
    dfp['y'] = np.reshape(p,p.shape[0]*p.shape[1])
    return dfp
  else:
    return p


def validate(model,stats=ss.default_stats,N=None):
  p = predict(model)
  counts = model.init.df.ix[model.init.A.index, model.init.countvar].values
  tests = ss.ppp(np.squeeze(model.init.y.values) / counts,p.T,error_fn(model),stats,N=N)

  g = tests.groupby('type')
  summary = g.mean()
  summary['fakeSE'] = g.fake.std()
  summary['realSE'] = g.real.std()
  summary['p_val'] = g.apply(lambda d: ss.p_value(d.real - d.fake))
  return summary


def error_fn(model,counts=None):
  if counts is None:
    counts = model.init.df.ix[model.init.A.index, 'total']
  scale = model.fit['scale']

  def fn(y_hat,indices,scale=scale,counts=counts):
    y_hat = y_hat[indices,:]
    scale = scale[indices,np.newaxis]
    counts = counts[np.newaxis,:]

    p = np.random.beta(y_hat * scale, (1 - y_hat) * scale)
    successes = np.random.binomial(counts, p)
    return successes.astype('float64') / counts - y_hat

  return fn


def predict_summary(model,p,percentiles=[02.5, 97.5]):
  dfm = model.init.df
  dfm['y'] = dfm.correct.astype('float64') / dfm.total
  dfm['y_hat'] = np.mean(p, axis=1)

  ef = error_fn(model)
  bounds = np.percentile(np.vstack([ef(p[:,i], i) for i in range(p.shape[1])]),
                         percentiles, axis=0)
  dfm['y_hat_lower'] = bounds[0,:] + dfm['y_hat']
  dfm['y_hat_upper'] = bounds[1,:] + dfm['y_hat']

  return dfm


def beta_binomial_ln(n,N,alpha,beta):
      from scipy.special import gammaln, betaln

      def chooseln(N,k): return gammaln(N+1) - gammaln(N-k+1) - gammaln(k+1)
      return chooseln(N,n) + betaln(n+alpha, N-n+beta) - betaln(alpha,beta)


def WAIC(model):
  scale = model.fit['scale']
  correct = model.init.df.ix[model.init.A.index,'correct']
  counts = model.init.df.ix[model.init.A.index, 'total']
  p = predict(model)

  log_post = beta_binomial_ln(correct[:,np.newaxis],counts[:,np.newaxis],
                              scale[np.newaxis,:]*p,scale[np.newaxis,:]*(1-p))
  p_waic = np.std(log_post,axis=1,ddof=1)
  lpd = scipy.misc.logsumexp(log_post,axis=1) - np.log(log_post.shape[1])
  return -2*np.sum(lpd - p_waic),2*np.sqrt(lpd.shape[0] * np.std(lpd - p_waic))


def binom_lmm_init(mean_formula,countvar,df,groups,marginalize=[]):

  y,A = patsy.dmatrices(mean_formula,df,return_type='dataframe')

  gdf_1,gg_1,group_keys_1 = _setup_groups(df,groups[0]['grouping'])
  B_1 = patsy.dmatrix(groups[0]['formula'],df,return_type='dataframe')
  G_1 = patsy.dmatrix(groups[0]['group_formula'],gdf_1,return_type='dataframe')
  if len(groups) == 1:
    return SlopesInit(mean_formula,countvar,groups,df,y,A,
                      [gdf_1],[gg_1],[group_keys_1],[B_1],G_1)

  if len(groups) >= 2:
    gdf_2,gg_2,group_keys_2 = _setup_groups(df,groups[1]['grouping'])
    B_2 = patsy.dmatrix(groups[1]['formula'],df,return_type='dataframe')

    if len(groups) == 2:
      return SlopesInit(mean_formula,countvar,groups,df,
                        y,A,[gdf_1,gdf_2],[gg_1,gg_2],
                        [group_keys_1,group_keys_2],[B_1,B_2],G_1)

  if len(groups) >= 3:
    gdf_3,gg_3,group_keys_3 = _setup_groups(df,groups[2]['grouping'])
    B_3 = patsy.dmatrix(groups[2]['formula'],df,return_type='dataframe')

    if len(groups) == 3:
      return SlopesInit(mean_formula,countvar,groups,df,y,A,
                        [gdf_1,gdf_2,gdf_3],[gg_1,gg_2,gg_3],
                        [group_keys_1,group_keys_2,group_keys_3],[B_1,B_2,B_3],
                        G_1)


def binom_lmm(mean_formula,countvar,df,groups,mean_prior=5,
              error_prior=1000,mean_init=0,iters=5,warmup=2,chains=1):
  assert (len(groups) >= 1) and (len(groups) <= 3)

  init = binom_lmm_init(mean_formula,countvar,df,groups)

  model_input = {"y": np.squeeze(init.y).astype('int64'),
                 "totals": init.df.ix[init.A.index,countvar],
                 "A": init.A, "n": len(init.y),
                 "k": init.A.shape[1],
                 "B_1": init.B[0].ix[init.A.index],
                 "h_1": init.B[0].shape[1],
                 "gg_1": init.gg[0][init.A.index]+1,
                 "G_1": init.G, "l_1": init.G.shape[1],
                 "g_1": init.G.shape[0],

                 "fixed_mean_prior": mean_prior,
                 "prediction_error_prior": error_prior,

                 "group1_mean_prior": groups[0]['mean_prior'],
                 "group1_var_prior": groups[0]['var_prior'],
                 "group1_cor_prior": 2}

  if len(groups) >= 2:
    model_input2 = {"B_2": init.B[1].ix[init.A.index],
                    "h_2": init.B[1].shape[1],
                    "gg_2": init.gg[1][init.A.index]+1,
                    "g_2": init.gdf[1].shape[0],

                    "group2_var_prior": groups[1]['var_prior'],
                    "group2_cor_prior": 2}
    model_input = merge_dicts(model_input,model_input2)

  if len(groups) == 3:
    model_input3 = {"B_3": init.B[2].ix[init.A.index],
                    "h_3": init.B[2].shape[1],
                    "gg_3": init.gg[2][init.A.index]+1,
                    "g_3": init.gdf[2].shape[0],

                    "group3_var_prior": groups[2]['var_prior'],
                    "group3_cor_prior": 2}

    model_input = merge_dicts(model_input,model_input3)

  def init_fn():
    g_1,l_1 = init.G.shape
    h_1 = init.B[0].shape[1]
    if len(groups) >= 2:
      g_2 = init.gdf[1].shape[0]
      h_2 = init.B[1].shape[1]
    if len(groups) >= 3:
      g_3 = init.gdf[2].shape[0]
      h_3 = init.B[2].shape[1]

    model_init = {"gamma_1": np.random.rand(l_1,h_1)*0.001,
                  "z_1": np.random.rand(h_1,g_1)+0.001,
                  "L_Omega_1": np.zeros((h_1,h_1)),
                  "tau_1": np.random.rand(h_1)+0.001,

                  "scale": error_prior+np.random.rand()*0.001}
    if init.A.shape[1] > 0:
      model_init['alpha'] = mean_init+np.random.rand()*0.001
    else:
      model_init['alpha'] = []

    if len(groups) >= 2:
      model_init2 = {"z_2": np.random.rand(h_2,g_2)+0.001,
                     "L_Omega_2": np.zeros((h_2,h_2)),
                     "tau_2": np.random.rand(h_2)+0.001}
      model_init = merge_dicts(model_init,model_init2)

    if len(groups) >= 3:
      model_init3 = {"z_3": np.random.rand(h_3,g_3)+0.001,
                     "L_Omega_3": np.zeros((h_3,h_3)),
                     "tau_3": np.random.rand(h_3)+0.001}
      model_init = merge_dicts(model_init,model_init3)

    return model_init

  if len(groups) == 1:
    fit = model1.sampling(data=model_input,init=init_fn,iter=iters,
                          chains=chains,warmup=warmup)
  if len(groups) == 2:
    fit = model2.sampling(data=model_input,init=init_fn,iter=iters,
                          chains=chains,warmup=warmup)
  if len(groups) == 3:
    fit = model3.sampling(data=model_input,init=init_fn,iter=iters,
                          chains=chains,warmup=warmup)

  return SlopesModel(fit,init)
