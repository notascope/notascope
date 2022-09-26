library(tidyverse)
library(lubridate)

df <- read_csv("data/movies.csv") |>
  mutate(`Release Date` = year(`Release Date`))
ggplot(df) +
  geom_area(aes(
    x = `Release Date`,
    y = `Worldwide Gross`,
    fill = `MPAA Rating`
  ), stat = "summary", fun = "sum", position = "fill")
