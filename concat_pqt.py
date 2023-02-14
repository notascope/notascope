import sys
import pandas as pd

pd.concat([pd.read_parquet(f) for f in sys.argv[2:]]).to_parquet(sys.argv[1])
