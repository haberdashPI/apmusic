require(boot)
source(file.path('preprocessing','files.txt'))

data = read.csv(file.path('preprocessing','data',fig2C_data))

means = aggregate(experience ~ regimen + sid,data,mean)

m = lm(experience ~ C(regimen,sum),means)
cat("Does the amount of musical experience differ across the training regimens?\n")
cat("----------------------------------------\n")
cat("ANOVA (validation fails)\n")
print(shapiro.test(residuals(m)))
print(anova(m))

cat("----------------------------------------\n")
cat("Non-parametric test")
print(kruskal.test(experience ~ regimen,means))
