import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))

d = pd.DataFrame([{'day': day, 'sid': sid, 'foil_label': foil_label,
                   'regimen': regimen}
                  for (regimen,sid,foil_label),_
                  in model.init.df.groupby(['regimen','sid','foil_label'])
                  for day in np.linspace(1,4,50)])

pind = (slm.predict(model,d,use_dataframe=True).
        set_index(['regimen','sid','foil_label','day','sample']).y)

days = pind.unstack(['day'])
days['imp'] = days[4] - days[1]
simp = days.groupby(level=['regimen','sid','sample']).imp.mean()*100
ind = (simp.groupby(level=['regimen','sid']).
       apply(ss.coef_stats).unstack(level=2))

print "----------------------------------------"
print "validation"
print slm.validate(model)

print "----------------------------------------"
print "% improvement by individual"
print ind
