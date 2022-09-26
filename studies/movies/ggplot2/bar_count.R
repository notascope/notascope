library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_bar(aes(x = `Major Genre`))
