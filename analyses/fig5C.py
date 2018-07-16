import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

df = pd.read_csv(op.join('preprocessing','data',fig5B_data))
model_reg = regress.robit('mean ~ posttest*regimen',df,error_prior=100,
                          cache_file=op.join("preprocessing","data",
                                             fig5C_samples_byregimen))

print "----------------------------------------"
print "Does the regimen matter?"
print "----------------------------------------"
print "validation"
print model_reg.validate()

print "----------------------------------------"
print "trained vs. untrained task differences across regimen"
p = pd.DataFrame([{'posttest': pt, 'regimen': reg}
                  for pt in model_reg.df.posttest.unique()
                  for reg in model_reg.df.regimen.unique()])
pdf = model_reg.predict(p,use_dataframe=True)
pdf = pdf.set_index(['regimen','posttest','sample']).y
pdf = pdf.unstack('regimen')
print ss.contrast_table(pdf*100,pdf.columns)


df = pd.read_csv(op.join('preprocessing','data',fig5C_data))
model_foil = regress.robit('mean ~ center(posttest)*stimulus_label',df,
                           error_prior=100,
                           cache_file=op.join("preprocessing","data",
                                              fig5C_samples_byfoil))


print "----------------------------------------"
print "Does the class (3rd, 4th, 5th, 6th) matter?"
print "----------------------------------------"
print "validation"
print model_foil.validate()

print "----------------------------------------"
print "trained vs. untrained task differences across class"
contrasts = np.array([[1,0,0,0],
                      [1,1,0,0],
                      [1,0,1,0],
                      [1,0,0,1]])
coefs = np.dot(model_foil.fit['alpha'][:,:4],contrasts.T)
print ss.contrast_table(coefs,['3rd','4th','5th','6th'],alpha=0.05)
