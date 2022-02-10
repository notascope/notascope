library(ggplot2)
library(reshape2)

ggplot(tips, aes(x=total_bill, y=factor(day), color=factor(day))) +
  geom_jitter()
