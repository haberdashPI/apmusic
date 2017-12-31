require(ggplot2)
source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig4C_data))
model = read.csv(file.path("preprocessing","data",fig4C_model))

pl = ggplot(model,aes(x=posttest*100,y=mean*100,group=stimulus_label))
pl = pl + geom_smooth(stat='identity',data=model,color='black',fill='lightgray',
                      aes(y=mean*100,ymin=lower*100,ymax=upper*100,linetype=stimulus_label))
pl = pl + geom_point(data=df,aes(shape=stimulus_label,fill=stimulus_label),size=1.5)
pl = pl + scale_color_brewer(palette='Set1')
pl = pl + xlab('% correct discrimination')
pl = pl + ylab('% correct classification')
pl = pl + scale_y_continuous(breaks=1:10*10)
pl = pl + scale_x_continuous(breaks=1:10*10)
pl = pl + coord_cartesian(xlim=c(45,100),ylim=c(0,100),expand=F)
pl = pl + theme_classic()

file = file.path('plots','pdfs',paste('fig4C_',Sys.Date(),'.pdf',sep=''))
ggsave(file,pl,width=8,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')


