library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_bar(aes(y = 1, fill = `MPAA Rating`))
