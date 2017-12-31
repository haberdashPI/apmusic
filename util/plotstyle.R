require(ggplot2)
require(Hmisc)

style = function(pl){
  pl = pl + theme_classic()
  pl = pl + scale_fill_manual(values=c("white","gray","gray","black"),
                            limits=c("P","SA","LA","AP"))
  pl = pl + scale_shape_manual(limits=c("P","SA", "LA", "AP"),
                             values=c(21,21,22,22))
  pl = pl + scale_linetype_manual(limits=c("P","SA", "LA", "AP"),
                                values=c(3,2,1,1))
  pl = pl + theme(axis.ticks.length=unit(-0.2,"cm"),
                  axis.text.y = element_text(margin=margin(0,1,0,0,"lines")),
                  axis.text.x = element_text(margin=margin(1,0,0,0,"lines")),
                  axis.line.x = element_line(size=0.5),
                  axis.line.y = element_line(size=0.5))
  pl
}

style.id_label = function(pl){
  pl = pl + theme_classic()
  pl = pl + scale_fill_manual(values=c("white","black","lightgray","darkgray"),
                            limits=c("3rd","4th","5th","6th"))
  pl = pl + scale_shape_manual(limits=c("3rd","4th","5th","6th"),
                             values=c(21,22,23,21))
  pl = pl + scale_linetype_manual(limits=c("3rd","4th", "5th", "6th"),
                                values=c(1,1,2,3))
  pl = pl + theme(axis.ticks.length=unit(-0.2,"cm"),
                  axis.text.y = element_text(margin=margin(0,1,0,0,"lines")),
                  axis.text.x = element_text(margin=margin(1,0,0,0,"lines")),
                  axis.line.x = element_line(size=0.5),
                  axis.line.y = element_line(size=0.5))
  pl
}
