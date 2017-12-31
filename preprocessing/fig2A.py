import os.path as op
execfile(op.join('util','header.py'))

dt = datetime.date.today().strftime("%Y-%m-%d")

c = setup.counts.query('(condition == "4th")').copy()
c = c.groupby(['regimen','day','sid']).agg(np.mean).reset_index()


model_samples = op.join("preprocessing","data","fig2A_samples_"+dt+".h5")
if op.isfile(model_samples):
  os.remove(model_samples)
model = regress.robit('mean ~ day * regimen',c,r=1e-24,
                      error_prior=100,cache_file=model_samples)

cf = setup.counts.query('(condition == "4th")').copy()
cf = cf.groupby(['regimen','day','sid','foil_label']).agg(np.mean).reset_index()

model_foil_samples = op.join("preprocessing","data","fig2A_byfoil_samples_"+dt+".h5")
if op.isfile(model_foil_samples):
  os.remove(model_foil_samples)
model_foil = regress.robit('mean ~ (day + day:regimen) * foil_label',
                           cf,r=1e-2,error_prior=100,cache_file=model_foil_samples)


print "Created "+model_samples
print "Created "+model_foil_samples

data = model.df
p = model.predict(pd.DataFrame([{'regimen': regimen, 'day': day} 
                             for regimen in model.df.regimen.unique()
                             for day in np.linspace(1,4,25)]),
               use_dataframe=True)
predict = (p.groupby(['regimen','day']).y.
           agg([np.mean,cilower,ciupper]).reset_index())

data_file = op.join("preprocessing","data","fig2A_data_"+dt+".csv")
data.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig2A_model_"+dt+".csv")
predict.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
