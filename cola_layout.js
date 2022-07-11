const cytoscape = require("cytoscape");
const cola = require("cytoscape-cola");
const elements = require("./results/vega-lite/vega-lite/net.json");
const styles = [
  {
    selector: "node",
    style: {
      width: 100,
      height: 100,
      shape: "rectangle",
      "background-fit": "cover",
      "background-image": "data(url)",
      label: "data(label)",
      "border-color": "grey",
      "border-width": 1,
      "text-outline-color": "white",
      "text-outline-width": "2",
      "text-margin-y": "20",
    },
  },
  {
    selector: "edge",
    style: {
      "line-color": "grey",
      "curve-style": "bezier",
      "target-arrow-color": "grey",
      "control-point-weight": 0.6,
      "target-arrow-shape": "triangle-backcurve",
      "arrow-scale": 2,
      label: "data(length)",
      "font-size": "24px",
      "text-outline-color": "white",
      "text-outline-width": "3",
    },
  },
  {
    selector: ".bidir",
    style: {
      "source-arrow-color": "grey",
      "source-arrow-shape": "triangle-backcurve",
    },
  },
  {
    selector: ".selected",
    style: {
      "source-arrow-color": "red",
      "target-arrow-color": "red",
      "line-color": "red",
      "border-color": "red",
      "border-width": 5,
    },
  },
  {
    selector: ".inserted",
    style: { "line-style": "dashed" },
  },
];

cytoscape.use(cola); // register extension

const cy = cytoscape({
  container: null,
  elements,
  headless: true,
  styleEnabled: true,
  styles: styles,
  animate: null,
});

const layout = cy
  .layout({
    name: "cola",
    animate: false,
    refresh: 10000,
    maxSimulationTime: 4000,
    fit: false,
    convergenceThreshold: 100,
  })
  .run();

result = [];
cy.nodes().map((node) => {
  const pos = node.position();
  result.push({
    data: node.data(),
    position: {
      x: 2 * pos.x,
      y: 2 * pos.y,
    },
    classes: "",
  });
});
cy.edges().map((edge) => {
  result.push({ data: edge.data(), classes: "" });
});
console.log(JSON.stringify(result));
process.exit();
