library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_point(aes(
    x = `Production Budget`, y = `Worldwide Gross`,
    color = `MPAA Rating`, size = `IMDB Rating`
  ))
