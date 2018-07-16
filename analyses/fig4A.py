import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

c = (setup.counts.query('condition == ["4th","4th_gen"] and day == 4').
     groupby(['regimen','sid','condition','meanpre'])['mean'].
     agg(np.mean).reset_index())

model = regress.robit("mean ~ center(meanpre) + regimen * condition",
                          c,error_prior=100,
                      cache_file=op.join("preprocessing","data",fig4A_samples))

d = c.groupby(['condition','regimen']).meanpre.mean().reset_index()
p = model.predict(d,use_dataframe=True)

print "----------------------------------------"
print "validation"
print model.validate()

d = c.groupby(['condition','regimen']).meanpre.mean().reset_index()
p = model.predict(d,use_dataframe=True)
regs = (p.set_index(['regimen','condition','sample']).y.
        unstack(level='regimen')*100)

print "----------------------------------------"
print ("Difference in % improvement from trained to untrained"+
       " stimulus (by regimen)")
print (ss.coef_table(regs.query('condition == "4th"').values -
       regs.query('condition == "4th_gen"').values,regs.columns))

print "----------------------------------------"
print ("% improvement differences by regimen for the untrained"+
       " stimlus (triangle tone)")
print ss.contrast_table(regs.query('condition == "4th_gen"'),regs.columns)
