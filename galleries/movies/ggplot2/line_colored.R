library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_line(aes(
    x = `Release Date`,
    y = `Worldwide Gross`,
    color = `MPAA Rating`
  ), stat = "summary_bin", fun = "sum", binwidth = 365)
