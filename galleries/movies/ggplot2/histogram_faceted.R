library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_histogram(aes(x = `Production Budget`, fill = `MPAA Rating`)) +
  facet_wrap(vars(`Major Genre`), ncol = 5)
