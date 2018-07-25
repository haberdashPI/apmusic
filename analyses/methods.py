import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

c = setup.counts.query('(condition == "4th")').copy()
c = c.groupby(['regimen','day','sid','date']).agg(np.mean).reset_index()

cday = (c.set_index(['regimen','sid','day'])[['date','mean']].
        unstack('day')[[('date',1),('mean',1),('mean',4)]])
cday.columns = pd.Index([e[0] + str(e[1]) for e in cday.columns])
cday.date1 = pd.to_numeric(pd.to_datetime(cday.date1))
cday.date1 = (cday.date1 - cday.date1.mean()) / cday.date1.std()

model = regress.robit('mean4 ~ date1',cday,r=1e-24,error_prior=100,
                      cache_file=op.join("preprocessing","data",
                                         method_samples))

print "----------------------------------------"
print "validation:"
print model.validate()

print "----------------------------------------"
print "coefs:"
print model.summary()

model = regress.robit('mean4 ~ date1*mean1',cday,r=1e-24,error_prior=100,
                      cache_file=op.join("preprocessing","data",
                                         method_samples_day1))

print "----------------------------------------"
print "validation:"
print model.validate()

print "----------------------------------------"
print "coefs:"
print model.summary()

