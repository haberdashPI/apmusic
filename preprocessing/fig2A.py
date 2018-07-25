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

rmodel = (p.groupby(level='foil_label').y.
          apply(lambda xs: ss.coef_stats(xs,show_sig=False)).
          unstack(level=1).reset_index())

rdata = model.init.df.query('day == 1')
dt = datetime.date.today().strftime("%Y-%m-%d")

data_file = op.join("preprocessing","data","fig2A_data_"+dt+".csv")
rdata.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig2A_model_"+dt+".csv")
rmodel.to_csv(model_file,header=True)
print "Created "+model_file


print "Please manually update preprocessing/files.txt"
