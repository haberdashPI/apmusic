library(cowplot)
library(dplyr)
library(ggplot2)
source(file.path('preprocessing','files.txt'))

## df = read.csv(file.path("preprocessing","data",fig2B_data))
## model = read.csv(file.path("preprocessing","data",fig2B_model))

## dfplot = df %>%
##   group_by(sid) %>%
##   mutate(pretest = mcorrect[day == 1]) %>%
##   filter(day == 4)

## pl = ggplot(dfplot,aes(y=mcorrect,x=pretest,shape=regimen,color=regimen)) +
##   geom_point() +
##   ## facet_grid(~regimen) +
##   geom_abline(slope = 1,intercept = 0) +
##   geom_smooth(method='lm',level=0) +
##   ylab('Day 4 (proportion correct)') + xlab('Day 1 (proportion correct)')

## file = file.path('plots','pdfs',paste('fig2C_',Sys.Date(),'.pdf',sep=''))
## save_plot(file,pl,base_aspect_ratio=1.3,ncol=1,nrow=1)
## file = file.path('plots','pdfs',paste('fig2C_',Sys.Date(),'.png',sep=''))
## save_plot(file,pl,base_aspect_ratio=1.3,ncol=1,nrow=1)

## pl = ggplot(dfplot,aes(y=mcorrect,x=pretest,shape=regimen,color=regimen)) +
##   geom_point() +
##   ## facet_grid(~regimen) +
##   geom_abline(slope = 1,intercept = 0) +
##   geom_smooth(method='lm',level=0.682) +
##   ylab('Day 4 (proportion correct)') + xlab('Day 1 (proportion correct)')

## cat('Created file ')
## cat(file)
## cat('\n')

odds = function(p){1/(1/((p+0.005)/1.01) - 1)}
logit = function(p){
    pa = (p + 0.005) / 1.01
    log(pa/(1.0-pa))
}

df = read.csv(file.path("preprocessing","data",fig2C_data))
model = read.csv(file.path("preprocessing","data",fig2C_model))

learn_p = read.csv(file.path("preprocessing","data",fig2B_model)) %>%
  group_by(regimen,sid) %>% summarize(p_imp = unique(p_imp))

df = df %>% inner_join(learn_p,by=c('regimen','sid'))

y_breaks = c(0.5,1,3,9)
ggplot(df,aes(x=day1,y=logit(day4)-logit(day1))) +
    ## geom_ribbon(aes(x,y,ymin=ymin,ymax=ymax,group=regimen),model,
                ## fill='gray',alpha=0.5) +
  ## geom_line(aes(x,y,linetype=regimen),model) +
  geom_smooth(method='lm',aes(color=regimen),level=0) +
  geom_point(aes(shape=regimen,fill=regimen),color='black',size=4) +
  scale_shape_manual(values=c(22,23,21,24)) +
  scale_x_continuous(breaks=5:10/10,labels=5:10*10) +
  scale_y_continuous(breaks=log(y_breaks),labels=y_breaks) +
  ## scale_y_continuous(breaks=5:10/10,labels=5:10*10) +
  ## scale_fill_manual(values=c('gray','black')) +
  xlab('Day 1 (% Correct)') +
  ylab('Day 4 (% Correct)')

file = file.path('plots','pdfs',paste('fig2C_',Sys.Date(),'.pdf',sep=''))
ggsave(file,width=10,height=6,useDingbats=FALSE)

cat('Created file ')
cat(file)
cat('\n')

file = file.path('plots','pdfs',paste('fig2C_',Sys.Date(),'.png',sep=''))
ggsave(file,width=10,height=6)
