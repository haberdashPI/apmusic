import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))

day1 = np.array([[1,0,0,1,0,0],
                 [1,1,0,1,1,0],
                 [1,0,1,1,0,1]])

cov = np.einsum('ij,kjh,hl->kil',day1,model.fit['Sigma_beta_2'],day1.T)
sds = np.sqrt(np.einsum('ijj->ij',cov))
cor = np.einsum('ij,ijk,ik->ijk',1./sds,cov,1./sds)

mu = np.mean(cor,axis=0)
se = np.std(cor,axis=0)
p = ss.p_value(cor,axis=0)

df = pd.DataFrame({'name': ['3rd v 5th', '5th v 6th', '6th v 3rd'],
                   'mean': [mu[0,1],mu[1,2],mu[2,0]],
                   'SE': [se[0,1],se[1,2],se[2,0]],
                   'mean > 0 (p)': [p[0,1],p[1,2],p[2,0]]},
                  columns=['name','mean','SE','mean > 0 (p)'])

print "----------------------------------------"
print "Pearson corelations (r) in starting value by foil:"
print df
