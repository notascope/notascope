library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_bar(aes(
    x = `Release Date`,
    y = stage(start = `Production Budget`, after_stat = 1),
    fill = after_stat(y)
  ), stat = "summary_bin", fun = "sum", binwidth = 365)
