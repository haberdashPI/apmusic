library(dplyr)
library(tidyr)
# long-active, active-passive, short-active and passive
regimens = c("LA","AP","SA","P")

########################################
## load all data files into a single data frame
data = NULL
dir = file.path("data","discrimination")

for (subdir in regimens){
  files = list.files(file.path(dir,subdir),"*.dat")

  for(file in files){
    cat('.')
    d = read.table(file.path(dir,subdir,file),sep=",",header=TRUE)
    d$regimen = subdir
    data = rbind(data,d)
  }
}
cat('\n')

########################################
## a bit of setup...

## replaces NAs with a given value
na.replace = function(x,y){
  x[is.na(x)] = y
  x
}

## each stimulus has an index
labels = c()
labels[1:20] = "3rd" # the first 20 indices are 3rds
labels[21:39] = "4th" # the next 19 are 4ths
labels[40:56] = "5th" # the next 17 are 5ths
labels[57:71] = "6th" # the next 15 are 6ths

########################################
## add additional columns, inferred from the existing ones
data = data %>%
  mutate(regimen = relevel(factor(regimen),"P"),
         sid = factor(sid)) %>%
  arrange(as.character(date)) %>%

  group_by(sid) %>%
  # infer the training day and the correct response and the label of the
  # standard interval
  mutate(day = 1+cumsum(na.replace(lag(date) != date,0)),
         correct = response_interval == signal_interval,
         foil_label = labels[standard]) %>%

  # the pretest is the mean of the first two blocks on day one
  group_by(sid) %>%
  mutate(pretest = mean(correct[day == 1 & block_index < 3]))

fn = file.path("preprocessing","data",
               paste("discrim_",Sys.Date(),".csv",sep=""))
write.csv(data,fn)
cat('Created ')
cat(fn)
cat('\n')
cat('Please manually update preprocessing/files.txt\n')
