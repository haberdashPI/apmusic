library(cowplot)
library(dplyr)
library(tidyr)
library(ggplot2)
source(file.path("preprocessing","files.txt"))

df = read.csv(file.path("preprocessing","data",fig3A_data))

df = df %>%
  select(regimen,sid,day,mean) %>%
  spread(day,mean) %>%
  rename(day1 = "1",day4 = "4") %>%
  select(regimen,sid,day1,day4)

ggplot(df,aes(x=day1,y=day4)) +
  geom_polygon(data=data.frame(x=c(0.45,1,1,0.45),y=c(0.45,1,0.45,0.45)),
               aes(x,y),alpha=0.5) +
  geom_smooth(method="lm",aes(color=regimen),level=0) +
  geom_point(aes(shape=regimen,fill=regimen),size=4) +
  scale_shape_manual(values=c(22,23,21,24)) +
  scale_x_continuous(breaks=5:10/10,labels=5:10*10) +
  scale_y_continuous(breaks=5:10/10,labels=5:10*10) +
  xlab("Day 1 (% Correct)") +
  ylab("Day 4 (% Correct)") +
  coord_fixed(xlim=c(0.45,1),ylim=c(0.45,1))

file = file.path("plots","pdfs",paste("fig3C_",Sys.Date(),".pdf",sep=""))
ggsave(file,width=8,height=6,useDingbats=FALSE)

cat("Created file ")
cat(file)
cat("\n")
