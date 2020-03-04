# NeedlemanWunschNames
This repo provides code to apply the Needleman-Wunsch algorithm to sequences of names using Levenshtein distance as a scoring metric.

# Example

```bash 
python3 align-company-names.py data/index-example.csv \
	data/book-example.csv \
	data/output-example.csv \
	--index_col text --book_col "company_name" --nrows 10
```
