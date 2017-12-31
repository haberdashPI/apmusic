import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

# update the date in this file if you re-run preprocessing/standard_model.py
model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))
p = pd.DataFrame([{'day': 1, 'regimen': regimen,
                   'sid': -1, 'foil_label': foil_label}
                   for regimen in model.init.df.regimen.unique()
                   for foil_label in model.init.df.foil_label.unique()])
p = (slm.predict(model,p,marginalize=[1],use_dataframe=True).
     set_index(['day','regimen','foil_label','sample']))

foils = p.y.unstack(['foil_label'])*100
foil_names = p.index.levels[2]

print "----------------------------------------"
print "% correct on day 1 vs. foil"
print ss.coef_table(foils,foil_names)

# we do not need to correct for multiple comparisons, because we are jointly
# modeling interactions in a multi-level model (see comments in Methods
# section)
print "----------------------------------------"
print "comparisons between foils:"
print ss.contrast_table(foils,foil_names,correct=False)
