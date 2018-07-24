library(ggplot2)
source(file.path("preprocessing","files.txt"))

df = read.csv(file.path("preprocessing","data",fig3B_data))
model = read.csv(file.path("preprocessing","data",fig3B_model))

pl = ggplot(df,aes(x=day,y=mcorrect,group=sid)) + facet_wrap(~regimen,ncol=4)
pl = pl + geom_ribbon(data=model,fill="gray",alpha=0.5,
                      mapping=aes(ymin=mean-SE,ymax=mean+SE,y=mean))
pl = pl + geom_line(data=model,size=1,alpha=0.8,
                    mapping=aes(y=mean,color=p_imp < 0.05))
pl = pl + geom_line(linetype=3,size=0.5)
pl = pl + geom_point(size=1.3)
pl = pl + geom_text(data=subset(model,day == 4),
                    aes(label=round(imp,1),y=mean,group=sid),
                    hjust=-0.25,position=position_dodge(width=0.5),size=3)
pl = pl + coord_cartesian(xlim=c(0.75,5))
pl = pl + scale_y_continuous(breaks=5:10/10,labels=5:10*10)
pl = pl + scale_color_brewer(palette="Set1")
pl = pl + theme_classic()

file = file.path("plots","pdfs",paste("fig3B_",Sys.Date(),".pdf",sep=""))
ggsave(file,pl,width=10,height=6,useDingbats=FALSE)

cat("Created file ")
cat(file)
cat("\n")
