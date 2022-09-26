library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  aes(x = `Production Budget`, y = `Worldwide Gross`) +
  geom_point(aes(color = `MPAA Rating`)) +
  geom_smooth(method = "lm", se = FALSE)
