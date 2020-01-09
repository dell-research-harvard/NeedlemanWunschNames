import pandas as pd
import numpy as np
import time
import string
import regex
import argparse
from NW_Company_Names.NW_company_names import create_nw_df 





def NW_align_names(index_csv, book_csv, output_csv, data_source_type = "firm"):
    """
    Aligns two sequences of company names using edit distance as a cost metric and the
    Needleman-Wunsch .algorithm
    
    Arguments:
        index_csv {str} -- csv with index names - must be labelled "text". 
        book_csv {str} -- csv with book names - must be labelled "company name"
        output_csv {str} -- Output csv path
    
    Keyword Arguments:
        data_source_type {str} -- which data source type to match (firms from
        index, bank, supplement etc.) (default: {"firm"})
    
    Returns:
        [Pandas DataFrame] -- Pandas DF with matched sequences and respective
        indices.
    """
    index_df = pd.read_csv(index_csv)
    book_df = pd.read_csv(book_csv)

    subset_index_df = index_df[index_df["data_source_type"] == data_source_type]
    subset_book_df = book_df[book_df["companyid"].str.contains(data_source_type)]

    subset_index_df = subset_index_df.reset_index()
    subset_book_df = subset_book_df.reset_index()

    # Removing digits
    subset_index_df["clean_text"] = subset_index_df["text"].str.replace(r"\d+", "")
    # Removing Latin Characters
    subset_index_df["clean_text"] = subset_index_df["clean_text"].apply(lambda x: regex.sub(r"\p{Latin}", u"", str(x)))
    # Removing punctuation
    subset_index_df["clean_text"] = subset_index_df["clean_text"].apply(lambda x: regex.sub(r"\p{Punct}", u"", str(x)))
    subset_index_df["clean_text"] = subset_index_df["clean_text"].apply(lambda x: regex.sub(r"\|", u"", str(x)))
    
    # Arranging by companyid MUST BE ZERO PADDED OR WON'T BE IN ORDER
    subset_book_df = subset_book_df.sort_values(by = ["companyid"])

    # Run algo
    matched_df =  create_nw_df(
        subset_book_df,
        subset_index_df,
        "company name",
        "clean_text"
        )
    matched_df.to_csv(output_csv)
    return matched_df


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Match sequences of company names.")
    parser.add_argument("index_csv", type = argparse.FileType("r"), help = "CSV with index name data")
    parser.add_argument("book_csv", type = argparse.FileType("r"), help = "CSV with company name data")
    parser.add_argument("output_csv", type = argparse.FileType("w"), help = "Output name")
    parser.add_argument("--data_source_type", type = str, help = "data source type (defaults to firm)", default="firm")
    args = parser.parse_args()

    # Timing
    start = time.time()
    init_df = NW_align_names(
        args.index_csv,
        args.book_csv,
        args.output_csv,
        args.data_source_type
    )
    end = time.time()
print(init_df[["sequence_1", "sequence_2", "sequence_text_x", "sequence_text_y"]])
print("Time Taken:", end - start)