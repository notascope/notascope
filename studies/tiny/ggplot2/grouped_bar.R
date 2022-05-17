library(tibble)
library(ggplot2)

df <- tribble(
  ~Contestant, ~Fruit, ~"Number Eaten",
  "Alex", "Apples", 2,
  "Alex", "Oranges", 1,
  "Alex", "Bananas", 3,
  "Jordan", "Apples", 1,
  "Jordan", "Oranges", 3,
  "Jordan", "Bananas", 2
)

ggplot(df, aes(x = factor(Fruit), y = `Number Eaten`, fill = factor(Contestant))) +
  geom_bar(stat = "identity", position = "dodge")
