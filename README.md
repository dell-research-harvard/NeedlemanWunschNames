
# Needleman Wunsch Names

[![Example Jupyter
Notebook](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/dell-research-harvard/NeedlemanWunschNames/master?filepath=example.ipynb)

This repo provides code to apply the Needleman-Wunsch algorithm to match ordered sequences of strings (Japanese company names were the original use case, hence the repo's name) using Levenshtein distance as a scoring metric.

# Example
To run the algorithm from bash use:

```bash 
python3 align-company-names.py data/index-example.csv \
	data/book-example.csv \
	data/output-example.csv \
	--index_col text --book_col "company_name" --nrows 10
```


A static example notebook is available [here.](example.ipynb) Alternatively, use the binder link above.

Much of the code found here was generously made available by [The Wilke Lab](https://wilkelab.org/) and modified during the author's time working for [Melissa Dell.](https://scholar.harvard.edu/dell)
