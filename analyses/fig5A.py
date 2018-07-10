import os.path as op
execfile(op.join('util', 'header.py'))
execfile(op.join('preprocessing', 'files.txt'))

df = pd.read_csv(op.join('preprocessing', 'data', fig5A_data))
model = regress.robit('mean ~ center(pretest) + regimen', df,
                      error_prior=df['len'].max(),
                      cache_file=op.join("preprocessing", "data",
                                         fig5A_samples))

print "----------------------------------------"
print "validation"
print model.validate()

d = df.groupby(['regimen']).pretest.mean().to_frame('pretest').reset_index()
p = model.predict(d, use_dataframe=True)
regs = p.set_index(['regimen', 'sample']).y.unstack(level='regimen')*100

print "----------------------------------------"
print "% correct classification by regimen"
print ss.coef_table(regs, regs.columns)

print "----------------------------------------"
print "% correct classification differences across regimen"
print ss.contrast_table(regs, regs.columns)
