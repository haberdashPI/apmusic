import os.path as op
execfile(op.join('util', 'header.py'))
execfile(op.join('preprocessing', 'files.txt'))

c = (setup.counts.query('condition == ["4th", "4th_gen"] and day == 4').
     groupby(['regimen', 'sid', 'condition', 'meanpre'])['mean'].
     agg(np.mean).unstack('condition').reset_index())

c.rename(columns={'4th': 'trained',  '4th_gen': 'untrained'}, inplace=True)

model = regress.robit("untrained ~ trained", c, error_prior=100,
                      cache_file=op.join("preprocessing", "data",
                                         fig3B_samples))

print "Analysis of trained vs. untrained"
print "----------------------------------------"
print "Model validation"
print model.validate()

print "----------------------------------------"
print "Model stats"
print "R^2: %4.3f (SE = %3.3f)" % (np.mean(model.R2()), np.std(model.R2()))
print "p-value: %4.3f" % (ss.p_value(model.R2()))

print "----------------------------------------"
print "Does regimen infuence trained vs. untrained analysis?"

model_reg = regress.robit("untrained ~ trained*regimen", c,
                          error_prior=100,
                          cache_file=op.join("preprocessing", "data",
                                             fig3B_samples_byregimen))

print "----------------------------------------"
print "model validation"
print model_reg.validate()

print "----------------------------------------"
print "differences in trained vs. untrained by regimen:"
p = pd.DataFrame([{'regimen': regimen, 'trained': model_reg.df.trained.mean()}
                  for regimen in model_reg.df.regimen.unique()])
pdf = (model_reg.predict(p, use_dataframe=True).
       set_index(['regimen', 'sample']).y)
pdf = pdf.unstack('regimen')
print ss.contrast_table(pdf*100, pdf.columns)



print "----------------------------------------"
print "Does regimen infuence trained vs. untrained analysis?"

cf = (setup.counts.query('condition == ["4th", "4th_gen"] and day == 4').
      groupby(['regimen', 'sid', 'condition', 'meanpre',
               'foil_label'])['mean'].
      agg(np.mean).unstack('condition').reset_index())
cf.rename(columns={'4th': 'trained',  '4th_gen': 'untrained'}, inplace=True)
model_foil = regress.robit("untrained ~ trained * foil_label", cf,
                           error_prior=100,
                           cache_file=op.join("preprocessing", "data",
                                              fig3B_samples_byfoil))

print "----------------------------------------"
print "validation"
print model_foil.validate()

print "----------------------------------------"
print "differences in trained vs. untrained by foil:"
p = pd.DataFrame([{'trained': model_foil.df.trained.mean(),
                   'foil_label': foil_label}
                  for foil_label in model_foil.df.foil_label.unique()])
pdf = (model_foil.predict(p, use_dataframe=True).
       set_index(['foil_label', 'sample']).y)
pdf = pdf.unstack('foil_label')
print ss.contrast_table(pdf*100, pdf.columns)
