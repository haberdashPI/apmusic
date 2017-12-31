library(ggplot2)
require(Hmisc)

source(file.path('preprocessing','files.txt'))

df = read.csv(file.path("preprocessing","data",fig2A_data))
model = read.csv(file.path("preprocessing","data",fig2A_model))

pdodge = position_dodge(width=0.2)
p = ggplot(df,aes(x=day,y=mean,group=regimen,shape=regimen,fill=regimen)) 
p = p + geom_smooth(data=model,stat='identity',aes(ymin=cilower,ymax=ciupper,linetype=regimen),
                    fill='grey',color='black')
p = p + stat_summary(fun.data='mean_cl_boot',position=pdodge,
                     fun.args=list(conf.int=0.682))
p = p + theme_classic()
p = p + scale_fill_manual(values=c("white","gray","gray","black"),
                          limits=c("P","SA","LA","AP"))
p = p + scale_shape_manual(limits=c("P","SA", "LA", "AP"),
                           values=c(21,21,22,22))
p = p + scale_linetype_manual(limits=c("P","SA", "LA", "AP"),
                              values=c(3,2,1,1))
p

file = file.path('plots','pdfs',paste('fig2A_',Sys.Date(),'.pdf',sep=''))
ggsave(file,p,width=8,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')
