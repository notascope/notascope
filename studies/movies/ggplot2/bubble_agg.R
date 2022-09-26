library(tidyverse)

df <- read_csv("/Users/nicolas/ets/notascope/data/movies.csv") |>
  group_by(`MPAA Rating`) |>
  summarize(
    `Production Budget` = mean(`Production Budget`, na.rm = TRUE),
    `Worldwide Gross` = mean(`Worldwide Gross`, na.rm = TRUE),
    `IMDB Rating` = mean(`IMDB Rating`, na.rm = TRUE)
  )

ggplot(df) +
  geom_point(aes(
    x = `Production Budget`, y = `Worldwide Gross`,
    color = `MPAA Rating`, size = `IMDB Rating`
  ))
