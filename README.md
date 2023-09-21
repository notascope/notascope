## NotaScope

NotaScope is open-source software, created to support the research to be presented at [VIS 2023](https://ieeevis.org/year/2023/welcome) in the paper entitled [Metrics-Based Evaluation and Comparison of Visualization Notations](https://arxiv.org/abs/2308.16353) by [Nicolas Kruchten](https://nicolas.kruchten.com/), [Andrew M. McNutt](https://www.mcnutt.in/) and [Michael J. McGuffin](https://www.michaelmcguffin.com/).

The NotaScope [source code is on Github](https://github.com/notascope) and a [running demo is available](https://app.notascope.io/). A [walkthrough video of the user interface is on YouTube](https://www.youtube.com/watch?v=PXwVhaU-8b4).

### Local Setup

To get started you'll need [`git`](https://git-scm.com/) and [`conda`](https://docs.conda.io/) (or `miniconda` or `mamba` or similar) installed:

```bash
$ git clone git@github.com:nicolaskruchten/notascope.git
$ cd notascope
$ git submodule init
$ git submodule update
$ conda env create -f environment.yml
$ conda activate env
$ yarn install
$ make app.py
$ python app.py
```
