import * as Plot from "@observablehq/plot";

export async function chart() {
  const data = [
    { Fruit: "Apples", Contestant: "Alex", "Number Eaten": 2 },
    { Fruit: "Oranges", Contestant: "Alex", "Number Eaten": 1 },
    { Fruit: "Bananas", Contestant: "Alex", "Number Eaten": 3 },
    { Fruit: "Apples", Contestant: "Jordan", "Number Eaten": 1 },
    { Fruit: "Oranges", Contestant: "Jordan", "Number Eaten": 3 },
    { Fruit: "Bananas", Contestant: "Jordan", "Number Eaten": 2 },
  ];

  return Plot.auto(data, {
    x: "Fruit",
    y: "Number Eaten",
    mark: "bar",
    color: "Contestant",
  }).plot({ color: { legend: true } });
}
