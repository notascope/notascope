library(ggplot2)
library(reshape2)

ggplot(tips, aes(x = total_bill, y = factor(time), color = factor(time))) +
  geom_jitter()
