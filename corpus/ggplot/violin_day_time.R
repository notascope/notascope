library(ggplot2)
library(reshape2)

p <- ggplot(tips, aes(x=total_bill, y=factor(time), fill=factor(time)))
p = p + geom_violin()
p = p + facet_grid(cols=vars(day))
