library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_bar(aes(
    x = `Release Date`,
    y = `Worldwide Gross`
  ), stat = "summary_bin", fun = "sum", binwidth = 365)
