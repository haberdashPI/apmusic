import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

c = setup.counts.query('(condition == "4th")').copy()
c = c.groupby(['regimen','day','sid']).agg(np.mean).reset_index()

model = regress.robit('mean ~ day * regimen',c,r=1e-24,
                      error_prior=100,
                      cache_file=op.join("preprocessing","data",fig3A_samples))
print "----------------------------------------"
print "validation:"
print model.validate()

predict = (model.df.query('day in [1,4]').
           groupby(['regimen','day'])['sum'].
           mean().reset_index())
predict = (model.predict(predict,use_dataframe=True).
           set_index(['regimen','day','sample']))

print "----------------------------------------"
print "day 1 % Correct: "
day1 = predict.query('day == 1').y.unstack('regimen')*100
print ss.coef_table(day1,day1.columns)

print "----------------------------------------"
print "day 4 % Correct: "
day4 = predict.query('day == 4').y.unstack('regimen')*100
print ss.coef_table(day4,day4.columns)

print "----------------------------------------"
print "day 1 to day 4 % improvement"
imp = predict.y.unstack('day')
imp['imp'] = imp[4] - imp[1]
imp = imp.imp.unstack('regimen')*100
print ss.coef_table(imp,imp.columns)
print ""

print "----------------------------------------"
print "day 4 % correct differeces: "
day4 = predict.query('day == 4').y.unstack('regimen')*100
print ss.contrast_table(day4,day4.columns)
