library(tidyverse)
library(lubridate)

df <- read_csv("data/movies.csv") |>
  mutate(`Release Date` = year(`Release Date`))
ggplot(df) +
  geom_line(aes(
    x = `Release Date`,
    y = `Worldwide Gross`
  ), stat = "summary", fun = "sum")
