import pandas as pd
import numpy as np
import time
import string
import regex
from NW_Company_Names.NW_company_names import create_nw_df 


N = 2000
pd.options.display.max_rows = int(round(N * 1.5))



index_df = pd.read_csv("summarised_PR1954_index.csv")
wide_df = pd.read_csv("PR1954_clean_wide_numeric_pipeline.csv")

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
    firm_wide_df[0:N],
    firm_index_df[0:int(round(N * 1.1))],
    "company name",
    "clean_text"
)


end = time.time()

init_df.to_csv("PR1954_matched_index_df.csv")

print(init_df[["sequence_1", "sequence_2", "sequence_text_x", "sequence_text_y"]])
print("Time Taken:", end - start)