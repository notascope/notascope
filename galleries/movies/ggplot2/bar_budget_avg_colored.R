library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_bar(aes(
    x = `Major Genre`, y = `Production Budget`,
    fill = `MPAA Rating`
  ),
  position = "dodge", stat = "summary", fun = "mean"
  )
