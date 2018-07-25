require(ggplot2)
library(cowplot)
source(file.path("preprocessing","files.txt"))

rdata = read.csv(file.path("preprocessing","data",fig2B_data))
rmodel = read.csv(file.path("preprocessing","data",fig2B_model))

p = function(xf,yf){
  pl = ggplot(rdata,aes_string(x=paste("X",xf,sep=""),y=paste("X",yf,sep="")))

  pl = pl + geom_point(shape=20,fill="black")

  pl = pl + theme_classic() +
    coord_cartesian(xlim=c(40,100),ylim=c(40,100),expand=FALSE)
  pl = pl + scale_x_continuous(breaks=4:10*10)
  pl = pl + scale_y_continuous(breaks=4:10*10)
  pl = pl + geom_smooth(stat="identity",data=subset(rmodel,a==xf & b==yf),
                        aes(x=x*100,y=y*100,ymin=ymin*100,ymax=ymax*100))


  pl = pl + theme(axis.text.y = element_text(margin=margin(0,1,0,0,"lines")),
                  axis.text.x = element_text(margin=margin(1,0,0,0,"lines")))
  pl = pl + theme(
              axis.ticks.length=unit(-0.33,"char"),
              axis.line.x = element_line(size=0.5,linetype=1,color="black"),
              axis.line.y = element_line(size=0.5,linetype=1,color="black"),
              strip.text.x = element_blank(),
              strip.text.y = element_blank(),
              strip.background = element_blank())


  pl
}
gr = plot_grid(p("3rd","5th"),p("5th","6th"),p("6th","3rd"),align="h",ncol=3)
file = file.path("plots","pdfs",paste("fig2B_",Sys.Date(),".pdf",sep=""))
save_plot(file,gr,base_aspect_ratio=1,ncol=3)

cat("Created file ")
cat(file)
cat("\n")
