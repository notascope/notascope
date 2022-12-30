library(tidyverse)
library(lubridate)

df <- read_csv("data/movies.csv") |>
  group_by(year(`Release Date`)) |>
  summarize_at(vars(`Production Budget`, `Worldwide Gross`), ~ sum(.x, na.rm = TRUE))

ggplot(df) +
  aes(
    x = `Production Budget`, y = `Worldwide Gross`
  ) +
  geom_point() +
  geom_path()
