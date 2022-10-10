library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  geom_bar(aes(x = `Production Budget`, y = `Worldwide Gross`),
    stat = "summary_bin", fun = "mean"
  )
