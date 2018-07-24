import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

c = setup.counts.query('(condition == "4th")').copy()
c = c.groupby(['regimen','day','sid','foil_label']).agg(np.mean).reset_index()

model = regress.robit('mean ~ (day + day:regimen) * foil_label',
                      c,r=1e-2,error_prior=100,
                      cache_file=op.join("preprocessing","data",
                                         fig2A_byfoil_samples))

print "----------------------------------------"
print "validation:"
print model.validate()

d = (c.query('day in [1,4]').groupby(['regimen','day','foil_label']).
     meanpre.mean().to_frame('mean').reset_index())
p = model.predict(d,use_dataframe=True)
imps = p.set_index(['regimen','day','foil_label','sample']).y.unstack('day')
imps['imp'] = imps.loc[:,4] - imps.loc[:,1]

foils = imps.imp.unstack(['regimen','foil_label'])*100
foils.columns = [foils.columns.levels[0][i] + ": " + foils.columns.levels[1][j]
                           for i,j in zip(*foils.columns.labels)]
print ss.coef_table(foils,foils.columns)

print "----------------------------------------"
print "% improvement by foil and regimen"
print ss.coef_table(foils,foils.columns)

print "----------------------------------------"
print "% improvement by foil"
foils = imps.imp.unstack('foil_label')*100
print ss.coef_table(foils,foils.columns)

print "----------------------------------------"
print "% improvement differences by foil"
print ss.contrast_table(foils,foils.columns)
