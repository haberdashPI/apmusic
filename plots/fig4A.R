library(ggplot2)

source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig4A_data))
model = read.csv(file.path("preprocessing","data",fig4A_model))

pdodge = position_dodge(width=0.8)
pl = ggplot(model,aes(x=regimen,y=mean*100)) 
pl = pl + geom_bar(stat='identity',data=model,
                   position=pdodge,fill='lightgrey',width=0.6)
pl = pl + geom_linerange(data=model,position=pdodge,
                         aes(ymin=lower*100,ymax=upper*100))
pl = pl + geom_point(data=df,position=pdodge)
pl = pl + scale_y_continuous(breaks=seq(20,100,10))
pl = pl + geom_hline(yintercept=25,linetype=2)
pl = pl + xlim(c('AP','LA','SA','P'))
pl = pl + coord_cartesian(xlim=c(0.5,4.5),ylim=c(20,100),expand=F)
pl = pl + theme_classic()
pl = pl + xlab('% correct classification')


file = file.path('plots','pdfs',paste('fig4A_',Sys.Date(),'.pdf',sep=''))
ggsave(file,pl,width=8,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')


