library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  stat_summary(aes(y = `Major Genre`, x = `Production Budget`))
