library(tibble)

df <- tribble(
  ~Contestant, ~Fruit, ~`Number Eaten`,
  "Alex", "Apples", 2,
  "Alex", "Oranges", 1,
  "Alex", "Bananas", 3,
  "Jordan", "Apples", 1,
  "Jordan", "Oranges", 3,
  "Jordan", "Bananas", 2
)

data <- with(df, tapply(`Number Eaten`, list(Contestant, Fruit), FUN = sum))
barplot(data, col = c("darkblue", "red"), legend = TRUE)
