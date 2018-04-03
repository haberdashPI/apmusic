import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('musician_model',
                             op.join("preprocessing","data",
                                     musician_sample_file))
model.init.df['mcorrect'] = ((model.init.df.correct.astype('float64')+0.5) /
                             (model.init.df.total+1))

print "----------------------------------------"
print "validation"
print slm.validate(model)

imp = 4*np.array([[0,0,0,1,0,0],
                 [0,0,0,1,1,0],
                 [0,0,0,1,0,1]])

imp_s = np.einsum('ij,jk->ik',model.fit['gamma_1'][:,1,:],imp.T)
print "----------------------------------------"
print "% improvement as a function of musical experience "
print ss.coef_stats(100*(ilogit(imp_s)-0.5).reshape(-1))

d = (model.init.df.query('day in [1,4]').
     groupby(['day','regimen','sid','foil_label','experience']).
        meanpre.mean().reset_index())
d.experience = d.experience.mean() # set musical experience to population mean
pind = (slm.predict(model,d,use_dataframe=True).
        set_index(['regimen','sid','foil_label','day','sample','experience']).y)

days = pind.unstack(['day'])
days['imp'] = days[4] - days[1]
simp = days.groupby(level=['regimen','sid','sample']).imp.mean()*100
ind = simp.groupby(level=['regimen','sid']).apply(ss.coef_stats).unstack(level=2)

print "----------------------------------------"
print "% improvement by individual, after removing effect of musical experience"
print ind
