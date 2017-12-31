import os.path as op
execfile(op.join('util','header.py'))

dt = datetime.date.today().strftime("%Y-%m-%d")

lc = setup.label_counts
model_samples = op.join("preprocessing","data","fig4A_samples_"+dt+".h5")
if op.isfile(model_samples):
  os.remove(model_samples)
model = regress.robit('mean ~ center(pretest) + regimen',lc,
                      error_prior=lc['len'].max(),cache_file=model_samples)
print "Created "+model_samples

d = lc.groupby(['regimen']).pretest.mean().to_frame('pretest').reset_index()
p = model.predict(d,use_dataframe=True)
predict = p.groupby(['regimen']).y.apply(ss.coef_stats_ns).unstack(level=1).reset_index()

data_file = op.join("preprocessing","data","fig4A_data_"+dt+".csv")
lc.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig4A_model_"+dt+".csv")
predict.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
