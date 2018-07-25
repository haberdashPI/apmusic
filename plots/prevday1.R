# this is an auxilarly analysis, unreporeted in the paper: it compares day1
# (all blocks) and pre-test (1st 2 blocks).  it doesn't look like there's much
# different between these two so there's not much to say here

library(dplyr)
library(ggplot2)
library(tidyr)

source(file.path('preprocessing','files.txt'))
df = read.csv(file.path('preprocessing','data',discrim_data))

means = df %>% filter(day == 1) %>%
  group_by(sid,regimen) %>%
  summarize(day1 = mean(signal_interval == response_interval),
            pre = mean(pretest)) %>%
  gather(period,mean,day1,pre)

ggplot(means,aes(x=period,y=mean)) + geom_line(aes(group=sid)) +
  geom_point() + facet_wrap(~regimen)

df %>% group_by(sid,regimen) %>%
  summarize(start = min(as.Date(date))) %>%
  print(n=28)
