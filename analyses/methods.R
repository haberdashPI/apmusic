library(tidyr)
library(dplyr)
library(ggplot2)
require(Hmisc)

source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig2A_data))

df = df %>%
  select(regimen,sid,mean,day) %>%
  filter(day %in% c(1,4)) %>%
  spread(day,mean) %>%
  rename(day1 = '1',day4 = '4')


