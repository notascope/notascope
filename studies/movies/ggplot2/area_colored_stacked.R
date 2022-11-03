library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_area(aes(
    x = `Release Date`,
    y = `Worldwide Gross`,
    fill = `MPAA Rating`
  ), stat = "summary_bin", fun = "sum", binwidth = 365, position = "fill")
