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
matplot(data, col = c("darkblue", "red", "green"), type = "l", lty = 1, xaxt = "n")
axis(1, tick = FALSE, at = c(1, 2), labels = row.names(data))
legend("topright", legend = colnames(data), col = 1:3, lty = 1)
