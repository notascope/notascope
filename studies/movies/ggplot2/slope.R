library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_line(aes(
    x = `Major Genre`,
    y = `Production Budget`,
    color = `MPAA Rating`,
    group = `MPAA Rating`
  ),
  stat = "summary", fun = "mean"
  )
