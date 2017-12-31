require(ggplot2)
source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig3B_data))
model = read.csv(file.path("preprocessing","data",fig3B_model))

pl = ggplot(df,aes(x=trained,y=untrained))
pl = pl + geom_smooth(stat='identity',data=model,aes(y=mean,ymin=lower,ymax=upper),color='black')
pl = pl + geom_point(aes(shape=regimen,fill=regimen))
pl = pl + theme_classic()
pl = pl + xlab('Trained Stimulus')
pl = pl + ylab('Untrained Stimulus')
pl = pl + coord_cartesian(ylim=c(0.2,1.2),xlim=c(0.4,1),expand=FALSE)
pl = pl + scale_y_continuous(breaks=5:10/10,labels=5:10*10)
pl = pl + scale_x_continuous(breaks=5:10/10,labels=5:10*10)

file = file.path('plots','pdfs',paste('fig3B_',Sys.Date(),'.pdf',sep=''))
ggsave(file,pl,width=8,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')

