library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_line(aes(x = `Production Budget`), stat = "bin")
