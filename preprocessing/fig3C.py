import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))
model.init.df['mcorrect'] = ((model.init.df.correct.astype('float64')+0.5) /
                             (model.init.df.total+1))

p = pd.DataFrame([{'day': day, 'regimen': regimen,
                   'sid': -1, 'foil_label': foil_label} for day in [1,4]
                   for regimen in model.init.df.regimen.unique()
                   for foil_label in model.init.df.foil_label.unique()])
p = (slm.predict(model,p,marginalize=[1],use_dataframe=True).
     set_index(['day','regimen','foil_label','sample']))

d = (model.init.df.query('day in [1,4]').
        groupby(['day','regimen','sid','foil_label']).
        meanpre.mean().reset_index())

dt = datetime.date.today().strftime("%Y-%m-%d")

data_file = op.join("preprocessing","data","fig3B_data_"+dt+".csv")
d.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig3B_model_"+dt+".csv")
p.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
