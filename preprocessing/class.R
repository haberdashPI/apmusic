library(dplyr)
library(tidyr)
# long-active, active-passive, short-active and passive
regimens = c("LA","AP","SA","P")

########################################
## load all data files into a single data frame
data = NULL
dir = file.path("data","classification")

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

########################################
## cleanup the data
data = data %>%
  mutate(regimen = relevel(factor(regimen),"P"),
         sid = factor(sid),
         day = 4,
         correct = response_label == stimulus_label) %>%
  arrange(as.character(date))

fn = file.path("preprocessing","data",
                 paste("class_",Sys.Date(),".csv",sep=""))
write.csv(data,fn)
cat('Created ')
cat(fn)
cat('\n')
cat('Please manually update preprocessing/files.txt\n')
