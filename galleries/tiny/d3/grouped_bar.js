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

  const y = d3.scaleLinear().domain([0, 3]).range([height, 0]);
  svg.append("g").call(d3.axisLeft(y));

  const color = d3.scaleOrdinal(d3.schemeCategory10);

  const xSubgroup = d3
    .scaleBand()
    .domain(subgroups)
    .range([0, x.bandwidth()])
    .padding([0.05]);

  svg
    .append("g")
    .selectAll("g")
    .data(data)
    .enter()
    .append("g")
    .attr("transform", function (d) {
      return "translate(" + x(d.Fruit) + ",0)";
    })
    .selectAll("rect")
    .data(function (d) {
      return subgroups.map(function (key) {
        return { key: key, value: d[key] };
      });
    })
    .enter()
    .append("rect")
    .attr("x", function (d) {
      return xSubgroup(d.key);
    })
    .attr("y", function (d) {
      return y(d.value);
    })
    .attr("width", xSubgroup.bandwidth())
    .attr("height", function (d) {
      return height - y(d.value);
    })
    .attr("fill", function (d) {
      return color(d.key);
    });
};

module.exports = plot;
