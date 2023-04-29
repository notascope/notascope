import { promises as fs } from "fs";
import * as path from "path";
import { JSDOM } from "jsdom";
import nodeHtmlToImage from "node-html-to-image";

const [_, __, input, output] = process.argv;

const { chart } = await import("./" + input);

function withJsdom(run) {
  return async () => {
    const jsdom = new JSDOM("");
    global.window = jsdom.window;
    global.document = jsdom.window.document;
    global.navigator = jsdom.window.navigator;
    global.Event = jsdom.window.Event;
    global.Node = jsdom.window.Node;
    global.NodeList = jsdom.window.NodeList;
    global.HTMLCollection = jsdom.window.HTMLCollection;
    global.fetch = async (href) => new Response(path.resolve("./test", href));
    try {
      return await run();
    } finally {
      delete global.window;
      delete global.document;
      delete global.navigator;
      delete global.Event;
      delete global.Node;
      delete global.NodeList;
      delete global.HTMLCollection;
      delete global.fetch;
    }
  };
}

class Response {
  constructor(href) {
    this._href = href;
    this.ok = true;
    this.status = 200;
  }
  async text() {
    return fs.readFile(this._href, { encoding: "utf-8" });
  }
  async json() {
    return JSON.parse(await this.text());
  }
}

const root = await withJsdom(chart)();
for (const svg of root.tagName === "svg"
  ? [root]
  : root.querySelectorAll("svg")) {
  svg.setAttributeNS(
    "http://www.w3.org/2000/xmlns/",
    "xmlns",
    "http://www.w3.org/2000/svg"
  );
  svg.setAttributeNS(
    "http://www.w3.org/2000/xmlns/",
    "xmlns:xlink",
    "http://www.w3.org/1999/xlink"
  );
}

nodeHtmlToImage({ output: output, html: root.outerHTML });
