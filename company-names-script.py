import pandas as pd
import numpy as np
import time
import string
import regex
import argparse
from NW_Company_Names.NW_company_names import create_nw_df 



parser = argparse.ArgumentParser(description="Match sequences of company names.")
parser.add_argument("index_csv", type = argparse.FileType("r"), help = "CSV with index name data")
parser.add_argument("book_csv", type = argparse.FileType("r"), help = "CSV with company name data")
parser.add_argument("output_csv", type = argparse.FileType("w"), help = "Output name")
args = parser.parse_args()

index_df = pd.read_csv(args.index_csv)
wide_df = pd.read_csv(args.book_csv)

firm_wide_df = wide_df[wide_df["companyid"].str.contains("firm")]
firm_index_df = index_df[index_df["data_source_type"] == "firm"]
firm_index_df = firm_index_df.reset_index()
# Removing digits
firm_index_df["clean_text"] = firm_index_df["text"].str.replace(r"\d+", "")
# Removing Latin Characters
firm_index_df["clean_text"] = firm_index_df["clean_text"].apply(lambda x: regex.sub(r"\p{Latin}", u"", str(x)))
# Removing punctuation
firm_index_df["clean_text"] = firm_index_df["clean_text"].apply(lambda x: regex.sub(r"\p{Punct}", u"", str(x)))
firm_index_df["clean_text"] = firm_index_df["clean_text"].apply(lambda x: regex.sub(r"\|", u"", str(x)))
# Resetting index and sorting by companyid
firm_wide_df = firm_wide_df.reset_index()
firm_wide_df = firm_wide_df.sort_values(by = ["companyid"])


# Timing
start = time.time()
init_df = create_nw_df(
    firm_wide_df,
    firm_index_df,
    "company name",
    "clean_text"
)


end = time.time()

init_df.to_csv(args.output_csv)

print(init_df[["sequence_1", "sequence_2", "sequence_text_x", "sequence_text_y"]])
print("Time Taken:", end - start)