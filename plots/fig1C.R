require(ggplot2)

source(file.path("util","plotstyle.R"))
source(file.path("preprocessing","files.txt"))

rdata = read.csv(file.path("preprocessing","data",fig2C_data))
rmodel = read.csv(file.path("preprocessing","data",fig2C_model))

p = ggplot(rmodel,aes(y=mean,x=experience)) +
  geom_ribbon(fill="gray",stat="identity",aes(ymin=lower,ymax=upper)) +
  geom_line() + ylab("% accuracy on day 1") +
  stat_summary(data=rdata,
               aes(x=experience,y=100*(correct/total),ymin=NULL,ymax=NULL,
                   group=sid),geom="point",size=2) +
  scale_x_continuous(breaks=0:15) +
  scale_y_continuous(breaks=seq(10,100,by=10),limits=c(40,100)) +
  coord_cartesian(xlim=c(-0.5,15.5),ylim=c(40,100),expand=FALSE)
p = p + theme_classic()
p = p + theme(axis.text.y = element_text(margin=margin(0,1,0,0,"lines")),
              axis.text.x = element_text(margin=margin(1,0,0,0,"lines")))
p = p + theme(
          axis.ticks.length=unit(-0.33,"char"),
          axis.line.x = element_line(size=0.5,linetype=1,color="black"),
          axis.line.y = element_line(size=0.5,linetype=1,color="black"),
          strip.text.x = element_blank(),
          strip.text.y = element_blank(),
          strip.background = element_blank())

p

file = file.path("plots","pdfs",paste("fig2C_",Sys.Date(),".pdf",sep=""))
ggsave(file,p,width=10,height=4,useDingbats=FALSE)

cat("Created file ")
cat(file)
cat("\n")
