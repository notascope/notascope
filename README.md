## NotaScope

To get started you'll need [`git`](https://git-scm.com/), [`conda`](https://docs.conda.io/) and [Firefox](https://firefox.com/) installed.

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
