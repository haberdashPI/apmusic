require(ggplot2)
source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig4B_data))
model = read.csv(file.path("preprocessing","data",fig4B_model))

pl = ggplot(df,aes(x=posttest*100,y=mean*100))
pl = pl + geom_smooth(stat='identity',data=model,aes(y=mean*100,ymin=100*(mean-SE),ymax=100*(mean+SE)),color='black')
pl = pl + geom_point(aes(shape=regimen,fill=regimen))
pl = pl + theme_classic()
pl = pl + xlab('% correct discrimination')
pl = pl + ylab('% correct classification')
pl = pl + scale_y_continuous(breaks=1:10*10)
pl = pl + scale_x_continuous(breaks=1:10*10)
pl = pl + coord_cartesian(xlim=c(45,100),ylim=c(0,100),expand=F)
pl = pl + theme_classic()


file = file.path('plots','pdfs',paste('fig4B_',Sys.Date(),'.pdf',sep=''))
ggsave(file,pl,width=8,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')


