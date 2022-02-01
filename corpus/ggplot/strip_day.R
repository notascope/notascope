library(ggplot2)
library(reshape2)

p <- ggplot(tips, aes(x=total_bill, y=factor(day), color=factor(day)))
p = p + geom_jitter()
