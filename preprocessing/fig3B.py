import os.path as op
execfile(op.join('util','header.py'))

dt = datetime.date.today().strftime("%Y-%m-%d")

c = (setup.counts.query('condition == ["4th","4th_gen"] and day == 4').
     groupby(['regimen','sid','condition','meanpre'])['mean'].
     agg(np.mean).unstack('condition').reset_index())

c.rename(columns={'4th': 'trained', '4th_gen': 'untrained'},inplace=True)

model_samples = op.join("preprocessing","data","fig3B_samples_"+dt+".h5")
if op.isfile(model_samples):
  os.remove(model_samples)
model = regress.robit("untrained ~ trained",c,error_prior=100,
                      cache_file=model_samples)

model_reg_samples = op.join("preprocessing","data","fig3B_samples_byregimen_"+dt+".h5")
if op.isfile(model_reg_samples):
  os.remove(model_reg_samples)
model_reg = regress.robit("untrained ~ trained*regimen",c,
                          error_prior=100,cache_file=model_reg_samples)

model_foil_samples = op.join("preprocessing","data","fig3B_samples_byfoil_"+dt+".h5")
if op.isfile(model_foil_samples):
  os.remove(model_foil_samples)
cf = (setup.counts.query('condition == ["4th","4th_gen"] and day == 4').
     groupby(['regimen','sid','condition','meanpre','foil_label'])['mean'].
     agg(np.mean).unstack('condition').reset_index())
cf.rename(columns={'4th': 'trained', '4th_gen': 'untrained'},inplace=True)
model_foil = regress.robit("untrained ~ trained * foil_label",
                           cf,error_prior=100,cache_file=model_foil_samples)


print "Created "+model_samples
print "Created "+model_reg_samples
print "Created "+model_foil_samples

d = pd.DataFrame({'trained': np.linspace(0.4,1,50), 'meanpre': model.df.meanpre.mean()})
rmodel = (model.predict(d,use_dataframe=True).groupby('trained').y.
          apply(ss.coef_stats_ns).unstack(level=1).reset_index())
rdata = model.df

data_file = op.join("preprocessing","data","fig3B_data_"+dt+".csv")
rdata.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig3B_model_"+dt+".csv")
rmodel.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"

