import os.path as op
execfile(op.join('util','header.py'))

dt = datetime.date.today().strftime("%Y-%m-%d")

c = (setup.counts.query('condition == ["4th","4th_gen"] and day == 4').
     groupby(['regimen','sid','condition','meanpre'])['mean'].
     agg(np.mean).reset_index())

model_samples = op.join("preprocessing","data","fig3A_samples_"+dt+".h5")
if op.isfile(model_samples):
  os.remove(model_samples)
model = regress.robit("mean ~ center(meanpre) + regimen * condition",
                          c,error_prior=100,cache_file=model_samples)

print "Created "+model_samples

d = c.groupby(['condition','regimen']).meanpre.mean().reset_index()
p = model.predict(d,use_dataframe=True)

predict = (p.set_index(['regimen','condition','sample']).y.
          groupby(level=['regimen','condition']).apply(ss.coef_stats_ns).
          unstack(level=2).reset_index())


data_file = op.join("preprocessing","data","fig3A_data_"+dt+".csv")
c.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig3A_model_"+dt+".csv")
predict.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"

