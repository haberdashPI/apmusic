import os.path as op
execfile(op.join('util','header.py'))

dt = datetime.date.today().strftime("%Y-%m-%d")

df = setup.label_counts
model_reg_samples = op.join("preprocessing","data",
                            "fig4C_samples_byregimen_"+dt+".h5")
if op.isfile(model_reg_samples):
  os.remove(model_reg_samples)
model_reg = regress.robit('mean ~ posttest*regimen',df,error_prior=100,
                          cache_file=model_reg_samples)

lcl = setup.label_counts_bylabel
model_foil_samples = op.join("preprocessing","data",
                            "fig4C_samples_byfoil_"+dt+".h5")
if op.isfile(model_foil_samples):
  os.remove(model_foil_samples)
model_foil = regress.robit('mean ~ center(posttest)*stimulus_label',lcl,
                         error_prior=100,cache_file=model_foil_samples)

print "Created "+model_reg_samples
print "Created "+model_foil_samples

d = pd.DataFrame([{'posttest': posttest, 'pretest': model_foil.df.pretest.mean(),
                   'stimulus_label': stimulus_label}
                   for posttest in np.linspace(0.4,1,50)
                   for stimulus_label in model_foil.df.stimulus_label.unique()])
predict = (model_foil.predict(d,use_dataframe=True).groupby(['posttest','stimulus_label']).y.
           apply(ss.coef_stats_ns).unstack(level=2).reset_index())


data_file = op.join("preprocessing","data","fig4C_data_"+dt+".csv")
lcl.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig4C_model_"+dt+".csv")
predict.to_csv(model_file,header=True)
print "Created "+model_file

