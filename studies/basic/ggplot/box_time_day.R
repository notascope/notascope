library(ggplot2)
library(reshape2)

ggplot(tips, aes(x = total_bill, y = factor(day), fill = factor(day))) +
  geom_boxplot() +
  facet_grid(cols = vars(time))
