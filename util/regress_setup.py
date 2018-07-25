import pandas as pd
import numpy as np
import os.path as op

execfile(op.join('preprocessing','files.txt'))

df = pd.read_csv(op.join('preprocessing','data',discrim_data))

df.set_index('sid',inplace=True)
df['meanpre'] = df.groupby(level='sid').pretest.mean()
df.reset_index(inplace=True)
df['ispretest'] = (df.block_index < 3) & (df.day == 1)

counts = (df.groupby(['regimen','sid','meanpre','day','foil_label',
          'condition','date']).
          correct.agg([np.sum,len,np.mean]).
          reset_index())
counts_nopre = (df[~df.ispretest].
                groupby(['regimen','sid','meanpre','day',
                        'foil_label','condition','date']).
                correct.agg([np.sum,len,np.mean]).
                reset_index())

rc_names = ['AP vs. SA','AP vs. P','AP vs. LA',
            'SA vs. P','SA vs. LA','P vs. LA']
rc_contrasts = np.array([[0,0,1],[0,1,0],[1,0,0],
                        [0,-1,1],[-1,0,1],[-1,1,0]])

cs = counts.query('condition == "4th" and day == 4')
pretest = cs.groupby(['regimen','sid']).meanpre.mean().to_frame('pretest')
posttest = cs.groupby(['regimen','sid'])['mean'].mean().to_frame('posttest')

labeld = pd.read_csv(op.join('preprocessing','data',class_data))
labeld = labeld.join(pretest,on=['regimen','sid'])
labeld = labeld.join(posttest,on=['regimen','sid'],rsuffix='post')
labeld.rename(columns={'correctpost': 'posttest'},inplace=True)
lcounts = (labeld.groupby(['regimen','sid',
                           'stimulus_label','pretest','posttest']).
           correct.agg([np.sum,len,np.mean]).
           reset_index())
label_counts = lcounts.groupby(['regimen','sid',
                                'pretest','posttest']).mean().reset_index()


lcounts = (labeld.groupby(['regimen','sid','stimulus_label',
                           'pretest','posttest']).
           correct.agg([np.sum,len,np.mean]).
           reset_index())
label_counts_bylabel = (lcounts.
                        groupby(['regimen','sid','pretest',
                                 'posttest','stimulus_label']).
                        mean().reset_index())

labels = ['3rd','4th','5th','6th']
label_counts_bylabel.stimulus_label = \
    np.array(labels)[label_counts_bylabel.stimulus_label-1]


def prediction_error(model,null_model=False):
  if null_model:
    mean_hat = model.y.mean()
  else:
    mean_hat = model.predict().mean(axis=1)

  return np.mean(1-(model.y*mean_hat + (1-model.y)*(1-mean_hat)))


