library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_boxplot(aes(x = `Major Genre`, y = `Production Budget`, fill = `MPAA Rating`))
