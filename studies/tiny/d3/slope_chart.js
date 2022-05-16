const plot = function (args) {
  const d3 = args.d3;
  const subgroups = ["Alex", "Jordan"];
  const data = [
    { Fruit: "Apples", Alex: "2", Jordan: "1" },
    { Fruit: "Bananas", Alex: "3", Jordan: "2" },
    { Fruit: "Oranges", Alex: "1", Jordan: "3" },
  ];
  const margin = { top: 10, right: 30, bottom: 20, left: 50 },
    width = args.dimensions.width - margin.left - margin.right,
    height = args.dimensions.height - margin.top - margin.bottom;

  const svg = args.svg
    .style("background", "white")
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  const x = d3.scaleOrdinal().domain(subgroups).range([0, width]);
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0));

  const y = d3.scaleLinear().domain([1, 3]).range([height, 0]);
  svg.append("g").call(d3.axisLeft(y));

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  svg
    .selectAll()
    .data(data)
    .enter()
    .append("path")
    .attr("stroke", function (d) {
      return color(d.Fruit);
    })
    .attr("stroke-width", 1.5)
    .attr("d", function (d) {
      return d3.line()([
        [x("Alex"), y(d.Alex)],
        [x("Jordan"), y(d.Jordan)],
      ]);
    });
};

module.exports = plot;
