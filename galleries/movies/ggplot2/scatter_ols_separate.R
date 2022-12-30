library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  aes(x = `Production Budget`, y = `Worldwide Gross`, color = `MPAA Rating`) +
  geom_point() +
  geom_smooth(method = "lm", se = FALSE)
