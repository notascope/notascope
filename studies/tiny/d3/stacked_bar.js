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

  const groups = ["Apples", "Bananas", "Oranges"];

  const x = d3.scaleBand().domain(groups).range([0, width]).padding([0.2]);
  svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).tickSize(0));

  const y = d3.scaleLinear().domain([0, 6]).range([height, 0]);
  svg.append("g").call(d3.axisLeft(y));

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const stackedData = d3.stack().keys(subgroups)(data);

  svg
    .append("g")
    .selectAll("g")
    .data(stackedData)
    .enter()
    .append("g")
    .attr("fill", function (d) {
      return color(d.key);
    })
    .selectAll("rect")
    .data(function (d) {
      return d;
    })
    .enter()
    .append("rect")
    .attr("x", function (d) {
      return x(d.data.Fruit);
    })
    .attr("y", function (d) {
      return y(d[1]);
    })
    .attr("width", x.bandwidth())
    .attr("height", function (d) {
      return y(d[0]) - y(d[1]);
    });
};

module.exports = plot;
