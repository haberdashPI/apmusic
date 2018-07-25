require(ggplot2)
source(file.path("preprocessing","files.txt"))
rmodel = read.csv(file.path("preprocessing","data",fig2A_model))
rdata = read.csv(file.path("preprocessing","data",fig2A_data))

pl = ggplot(rmodel,aes(y=mean,x=foil_label))
pl = pl + geom_bar(stat='identity',fill='gray')
pl = pl + geom_linerange(aes(ymin=lower,ymax=upper))
pl = pl + geom_point(data=rdata,mapping=aes(y=(correct+0.5)/(total+1)),
                     position=position_jitter(width=0.05))
pl = pl + xlim(c('3rd','5th','6th')) + xlab('Foil')
pl = pl + theme_classic()
pl = pl + scale_y_continuous(name="Day 1 % Correct",
                             breaks=seq(0.4,1,0.1),
                             labels=100*seq(0.4,1,0.1))
pl = pl + coord_cartesian(ylim=c(0.4,1))

file = file.path('plots','pdfs',paste('fig2A_',Sys.Date(),'.pdf',sep=''))
ggsave(file,pl,width=5.5,height=3.5,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')
