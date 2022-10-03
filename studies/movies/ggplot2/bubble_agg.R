library(tidyverse)

df <- read_csv("data/movies.csv") |>
  group_by(`MPAA Rating`) |>
  summarize_all(~ mean(.x, na.rm = TRUE))

ggplot(df) +
  geom_point(aes(
    x = `Production Budget`, y = `Worldwide Gross`,
    color = `MPAA Rating`, size = `IMDB Rating`
  ))
