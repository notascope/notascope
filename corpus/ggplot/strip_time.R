library(ggplot2)
library(reshape2)

p <- ggplot(tips, aes(x=total_bill, y=factor(time), color=factor(time)))
p = p + geom_jitter()
