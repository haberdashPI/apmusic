require(ggplot2)
require(Hmisc)

source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig3A_data))
model = read.csv(file.path("preprocessing","data",fig3A_model))

pdodge = position_dodge(width=0.8)
pl = ggplot(model,aes(x=regimen,y=mean*100,group=condition,fill=condition)) 
pl = pl + geom_bar(stat='identity',data=model,position=pdodge,width=0.6)
pl = pl + geom_linerange(data=model,position=pdodge,aes(ymin=lower*100,ymax=upper*100))
pl = pl + geom_point(data=df,position=pdodge,size=1.5)
pl = pl + coord_cartesian(ylim=c(40,100))
pl = pl + geom_abline(intercept=0.5,slope=0,linetype=2)
pl = pl + theme_classic()
pl = pl + xlim(c('AP','LA','SA','P'))
pl = pl + scale_fill_brewer(palette='Greys')

file = file.path('plots','pdfs',paste('fig3A_',Sys.Date(),'.pdf',sep=''))
ggsave(file,pl,width=8,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')

