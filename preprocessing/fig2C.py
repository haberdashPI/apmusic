import os.path as op
execfile(op.join('util','header.py'))
execfile(op.join('preprocessing','files.txt'))

model = sl.load_slopes_model('standard_model',
                             op.join("preprocessing","data",sample_file))
model.init.df['mcorrect'] = ((model.init.df.correct.astype('float64')+0.5) /
                             (model.init.df.total+1))
# goal, we want to make a plot that shows
# mean differences across regimen along with
# individual variations (in terms of starting
# performance vs. amount leanred)

# first step: individual variation in starting performance vs. learning
# is represented by the individual-level correlation matrix.
# To represent this visually, we're going to plot the first
# principle component of the correlation matrix,
# offset by the coefficient for each group.
# This should draw a straight line through the
# individual-level coefficients when plotted in logit space.

# An additional complication is that the model also accounts for potential
# differences in the data across foils. So we first have to find the average
# across the three foils.  That is, we don't want to plot a 6 dimensional data
# set, we want to plot a 2 dimensional data set: intercept (x) and slope (y) of
# individual learning curves.

# note: this computation is a little unintutive because the coefficients
# for the 5th and 6th foil are represented in terms of a difference
# (hence 1 1/3 1/3 instead of 1/3 1/3 1/3 to find an average) *AND*
# because the 'intercept' as plotted is actually the value
# at x = 1, since the first day is 1 not 0.
foil_average = np.array([[1, 1.0/3, 1.0/3, 1, 1.0/3, 1.0/3],
                         [0, 0, 0, 1, 1.0/3, 1.0/3]]).T

# now find the slope of the principle eigen vector
# of this correlation matrix (this is what we'll use
# to plot slopes and errors for each regimen).
eigval,eigvec = np.linalg.eigh(model.fit['Sigma_beta_2'])
eigvec_avg = np.einsum('ijk,hl -> ilk',eigvec,foil_average)
slope = np.median(eigvec[:,1,5] / eigvec[:,0,5],axis=0)

# now compute the average intercept and slope offset
# so we can give this slope the right intercept
regimen_offsets = np.dot(model.fit['beta_1'],foil_average)

# create a lite for each group
xs = np.linspace(0.49,0.9)
x_offset = regimen_offsets[np.newaxis,:,:,0]
intercept = regimen_offsets[np.newaxis,:,:,1]
ys = ((logit(xs[:,np.newaxis,np.newaxis]) - x_offset)*slope + intercept)

p = []
for r in range(4):
  b = ss.mean_bounds(ys[:,:,r].T,alpha=0.318)
  p.append(pd.DataFrame({'x': xs, 'y': np.median(ys[:,:,r],axis=1),
                         'ymin': b.lower, 'ymax': b.upper,
                         'regimen': model.init.group_keys[0].regimen[r]}))
rmodel = pd.concat(p)

old approach, uses model slope and intercept
# to compute the final data points we need to sum the individual offsets with
# the offset for each individual's regimen; to do this we need to know what regimen
# the individual was run on, so figure that out...
sid_to_regimen = model.init.gdf[1].reset_index().regimen

regimens = np.zeros(sid_to_regimen.size,'int_')
for i in range(sid_to_regimen.size):
  regimens[i] = np.where(sid_to_regimen[i] == model.init.group_keys[0])[0]

points = np.median(np.dot(model.fit['beta_2'] +
                          model.fit['beta_1'][:,regimens,:],
                          foil_average),axis=0)
rdata = pd.DataFrame({'intercept': ilogit(points[:,0]),
                      'logit_slope': points[:,1],
                      'sid': model.init.gdf[1].sid,
                      'regimen': model.init.gdf[1].regimen})

# rdata = (model.init.df.groupby(['sid','regimen','day']).
#          mcorrect.mean().unstack('day').
#          drop(columns=[2,3]).
#          rename(columns={1: 'day1',4: 'day4'}).
#          reset_index())

dt = datetime.date.today().strftime("%Y-%m-%d")

data_file = op.join("preprocessing","data","fig2C_data_"+dt+".csv")
rdata.to_csv(data_file,header=True)
print "Created "+data_file

model_file = op.join("preprocessing","data","fig2C_model_"+dt+".csv")
rmodel.to_csv(model_file,header=True)
print "Created "+model_file

print "Please manually update preprocessing/files.txt"
