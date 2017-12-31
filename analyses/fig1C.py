import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))


model = sl.load_slopes_model('musician_model',
                             op.join("preprocessing","data",musician_sample_file))

day1 = np.array([[1,0,0,1,0,0],
                 [1,1,0,1,1,0],
                 [1,0,1,1,0,1]])

imp = 4*np.array([[0,0,0,1,0,0],
                 [0,0,0,1,1,0],
                 [0,0,0,1,0,1]])

day1_s = np.einsum('ij,jk->ik',model.fit['gamma_1'][:,1,:],day1.T)
imp_s = np.einsum('ij,jk->ik',model.fit['gamma_1'][:,1,:],imp.T)

print "----------------------------------------"
print "pre-test improvement (in odds) for each year of musical experience"
print ss.coef_stats(100*(1-np.exp(-np.mean(day1_s,axis=1))))
