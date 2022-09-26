library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_tile(aes(x = `Major Genre`, y = `MPAA Rating`, z = `Production Budget`),
    stat = "summary_2d", fun = "mean"
  )
