library(ggplot2)
library(reshape2)

p <- ggplot(tips, aes(x=total_bill, y=1))
p = p + geom_jitter()
