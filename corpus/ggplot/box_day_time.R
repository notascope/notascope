library(ggplot2)
library(reshape2)

ggplot(tips, aes(x=total_bill, y=factor(time), fill=factor(time))) +
geom_boxplot() +
facet_grid(cols=vars(day))
