library(tidyverse)

df <- read_csv("data/movies.csv")
ggplot(df) +
  stat_summary(aes(y = `Major Genre`, x = `Production Budget`),
    fun.min = function(z) {
      quantile(z, 0.25)
    },
    fun.max = function(z) {
      quantile(z, 0.75)
    },
    fun = median
  )
