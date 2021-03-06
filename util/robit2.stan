data{
  int<lower=1> n; // number of observations
  int<lower=0> k; // number of predictors
  real y[n]; // outcomes
  matrix[n,k] A; // predictiors
  real prediction_error_prior;
  real fixed_mean_prior;
  real r_prior;
}
parameters{
  vector[k] alpha;
  real<lower=0,upper=0.1> r;
  real<lower=0> scale;
  // real<lower=0,upper=0.1> r;
}
model{
  scale ~ normal(0,prediction_error_prior);
  r ~ normal(0,r_prior);
  alpha ~ cauchy(0,fixed_mean_prior);
  for(i in 1:n){
    real p;
    p = inv_logit(A[i]*alpha);
    r/2 + y[i]*(1-r) ~ beta(p*scale,(1-p)*scale);
    target += log(fabs(1-r));
  }
}
