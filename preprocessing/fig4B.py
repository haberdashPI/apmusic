import os.path as op
execfile(op.join('util', 'header.py'))

dt = datetime.date.today().strftime("%Y-%m-%d")

lc = setup.label_counts

model_samples = op.join("preprocessing", "data", "fig5B_samples_"+dt+".h5")
if op.isfile(model_samples):
  os.remove(model_samples)
model = regress.robit('mean ~ posttest', lc, error_prior=100,
                      cache_file=model_samples)

model_noo_samples = op.join("preprocessing", "data",
                            "fig5B_samples_no_outlier_"+dt+".h5")
if op.isfile(model_noo_samples):
  os.remove(model_noo_samples)
model_no_outlier = regress.robit('mean ~ posttest', lc[lc['mean'] <= 0.8],
                                 error_prior=100, cache_file=model_noo_samples)
print "Created "+model_samples
print "Created "+model_noo_samples

d = pd.DataFrame({'posttest': np.linspace(0.4, 1, 50),
                  'pretest': model.df.pretest.mean()})
rmodel = (model.predict(d, use_dataframe=True).groupby('posttest').y.
          apply(ss.coef_stats_ns).unstack(level=1).reset_index())

data_file = op.join("preprocessing", "data", "fig5B_data_"+dt+".csv")
lc.to_csv(data_file, header=True)
print "Created "+data_file

model_file = op.join("preprocessing", "data", "fig5B_model_"+dt+".csv")
rmodel.to_csv(model_file, header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
