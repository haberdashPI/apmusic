import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))
model.init.df['mcorrect'] = ((model.init.df.correct.astype('float64')+0.5) /
                             (model.init.df.total+1))

d = pd.DataFrame([{'day': day, 'sid': sid, 'foil_label': foil_label,
                   'regimen': regimen}
                   for (regimen,sid,foil_label),_
                   in model.init.df.groupby(['regimen','sid','foil_label'])
                   for day in np.linspace(1,4,50)])

p = (slm.predict(model,d,use_dataframe=True).
     groupby(['regimen','sid','day','sample']).y.mean())

rmodel = (p.groupby(level=['regimen','sid','day']).
          apply(ss.coef_stats_ns).unstack(level=3).reset_index())
rdata = (model.init.df.groupby(['regimen','sid','day']).
         mcorrect.mean().reset_index())

pind = (slm.predict(model,d,use_dataframe=True).
        set_index(['regimen','sid','foil_label','day','sample']).y)
days = pind.unstack(['day'])
days['imp'] = days[4] - days[1]
simp = days.groupby(level=['regimen','sid','sample']).imp.mean()*100
ind = (simp.groupby(level=['regimen','sid']).
       apply(ss.coef_stats).unstack(level=2))

rmodel = rmodel.join((ind[['mean','p_value']].
                      rename(columns={'mean': 'imp', 'p_value': 'p_imp'})),
                     on=['regimen','sid'])
rmodel.imp = rmodel.imp.astype('float64')
rmodel.p_imp = rmodel.p_imp.astype('float64')

dt = datetime.date.today().strftime("%Y-%m-%d")

data_file = op.join("preprocessing","data","fig3B_data_"+dt+".csv")
rdata.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig3B_model_"+dt+".csv")
rmodel.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
