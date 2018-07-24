import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))

d =  pd.DataFrame([{'day': day, 'sid': sid, 'foil_label': foil_label,
                    'regimen': regimen}
                   for (regimen,sid,foil_label),_ 
                   in model.init.df.groupby(['regimen','sid','foil_label'])
                   for day in np.linspace(1,4,50)])
                  
p = (slm.predict(model,d,use_dataframe=True).
     groupby(['regimen','sid','day','foil_label','sample']).y.mean())

days = p.unstack(['day'])
days['imp'] = (days[4] - days[1])*100
rimp = days.groupby(level=['regimen','sample']).imp.mean().unstack(['regimen'])

print "----------------------------------------"
print "mult-level anlaysis of % improvement by regimen"
print ss.contrast_table(rimp,rimp.columns)

fimp = days.groupby(level=['foil_label','sample']).imp.mean().unstack(['foil_label'])
print "----------------------------------------"
print "mult-level anlaysis of % improvement by foil"
print ss.contrast_table(fimp,fimp.columns)

