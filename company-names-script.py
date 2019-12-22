import pandas as pd
import numpy as np
import time
from NW_Company_Names.NW_company_names import create_nw_df 


N = 2000
pd.options.display.max_rows = int(round(N * 1.1))



index_df = pd.read_csv("summarised_PR1954_index.csv")
wide_df = pd.read_csv("PR1954_clean_wide_numeric_pipeline.csv")

firm_wide_df = wide_df[wide_df["companyid"].str.contains("firm")]
firm_index_df = index_df[index_df["data_source_type"] == "firm"]
firm_index_df = firm_index_df.reset_index()
firm_wide_df = firm_wide_df.reset_index()
firm_wide_df = firm_wide_df.sort_values(by = ["companyid"])
print(firm_index_df.head())
print(firm_wide_df.head())
start = time.time()

init_df = create_nw_df(
    firm_wide_df[0:N],
    firm_index_df[0:(N+100)],
    "company name",
    "text"
)


end = time.time()
print(init_df[["sequence_1", "sequence_2", "sequence_text_x", "sequence_text_y"]])
print("Time Taken:", end - start)










