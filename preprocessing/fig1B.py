import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))

day1 = np.array([[1,0,0,1,0,0],
                 [0,1,0,1,1,0],
                 [0,0,1,1,0,1]])

cov = np.einsum('ij,kjh,hl->kil',day1,model.fit['Sigma_beta_2'],day1.T)
mu = np.dot(model.fit['gamma_1'],day1.T)[:,0,:]

slope_35 = cov[:,1,0] / cov[:,0,0]
intercept_35 = mu[:,1] - mu[:,0]*slope_35

slope_56 = cov[:,2,1] / cov[:,1,1]
intercept_56 = mu[:,2] - mu[:,1]*slope_56

slope_63 = cov[:,0,2] / cov[:,2,2]
intercept_63 = mu[:,0] - mu[:,2]*slope_63


xs = np.linspace(0.4,1)
ys = logit(ilogit(xs[:,np.newaxis])*slope_35[np.newaxis,:] + intercept_35[np.newaxis,:])
bounds = ss.mean_bounds(ys.T)
pred_35 = pd.DataFrame({'x': xs,'y': np.median(ys,axis=1),
                        'ymin': bounds.lower, 'ymax': bounds.upper,
                        'a': '3rd', 'b': '5th'})

ys = logit(ilogit(xs[:,np.newaxis])*slope_56[np.newaxis,:] + intercept_56[np.newaxis,:])
bounds = ss.mean_bounds(ys.T)
pred_56 = pd.DataFrame({'x': xs,'y': np.median(ys,axis=1),
                        'ymin': bounds.lower, 'ymax': bounds.upper,
                        'a': '5th', 'b': '6th'})

ys = logit(ilogit(xs[:,np.newaxis])*slope_63[np.newaxis,:] + intercept_63[np.newaxis,:])
bounds = ss.mean_bounds(ys.T)
pred_63 = pd.DataFrame({'x': xs,'y': np.median(ys,axis=1),
                        'ymin': bounds.lower, 'ymax': bounds.upper,
                        'a': '6th', 'b': '3rd'})
rmodel = pd.concat([pred_35,pred_56,pred_63])

model.init.df['y'] = ((model.init.df.correct.astype('float64')+0.5) /
                             (model.init.df.total+1))
df = (model.init.df.query('day == 1').
      groupby(['regimen','sid','foil_label']).
      y.mean())
rdata = (df.to_frame("y").
         groupby(level=['regimen','sid','foil_label']).
         y.agg('mean')*100).unstack('foil_label').reset_index()


dt = datetime.date.today().strftime("%Y-%m-%d")

data_file = op.join("preprocessing","data","fig2B_data_"+dt+".csv")
rdata.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig2B_model_"+dt+".csv")
rmodel.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
