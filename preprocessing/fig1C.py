import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('musician_model',
                             op.join("preprocessing","data",
                                     musician_sample_file))

cs = np.ones((200,2))
cs[:,1] = np.linspace(0,15,200)
start = np.array([1,1./3,1./3,0,0,0])
Xs = np.einsum('ik,jkh->jih',cs,model.fit['gamma_1'])
X = ilogit(np.einsum('ijk,k->ij',Xs,start))*100
rmodel = ss.coef_table(X,cs[:,1]).reset_index()

rmodel['experience'] = rmodel['index'].astype('float64')
rmodel['mean'] = rmodel['mean'].astype('float64')
rmodel['lower'] = rmodel['lower'].astype('float64')
rmodel['upper'] = rmodel['upper'].astype('float64')

rdata = model.init.df.query('day == 1')

rdata = rdata.groupby(['regimen','sid','experience']).sum()

dt = datetime.date.today().strftime("%Y-%m-%d")

data_file = op.join("preprocessing","data","fig1C_data_"+dt+".csv")
rdata.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig1C_model_"+dt+".csv")
rmodel.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
