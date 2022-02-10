library(ggplot2)
library(reshape2)

ggplot(tips, aes(x=total_bill, y=1)) +
  geom_jitter()
