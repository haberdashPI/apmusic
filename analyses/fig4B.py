import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

df = pd.read_csv(op.join('preprocessing','data',fig4B_data))
model = regress.robit('mean ~ posttest',df,error_prior=100,
                      cache_file=op.join("preprocessing","data",fig4B_samples))

print "----------------------------------------"
print "Before outlier above 80% correct is removed..."

print "----------------------------------------"
print "validation"
print model.validate()

print "----------------------------------------"
print "R^2: %4.3f (SE = %3.3f)" % (np.mean(model.R2()),np.std(model.R2()))
print "p-value: %4.3f" % (ss.p_value(model.R2()))

print "----------------------------------------"
print "After outlier above 80% correct is removed..."
model = regress.robit('mean ~ posttest',df[df['mean'] <= 0.8],error_prior=100,
                      cache_file=op.join("preprocessing","data",
                                         fig4B_samples_no_outlier))

print "----------------------------------------"
print "validation"
print model.validate()

print "----------------------------------------"
print "R^2: %4.3f (SE = %3.3f)" % (np.mean(model.R2()),np.std(model.R2()))
print "p-value: %4.3f" % (ss.p_value(model.R2()))
