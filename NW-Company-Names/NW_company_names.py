import numpy as np
import time
import editdistance
import pandas as pd
from math import isnan


def match_score(alpha, beta, gap_penalty = -1):
    if alpha == '------' or beta == '------':
        return gap_penalty
    else:
        # If GCV skips a row it returns nan in pandas which this catches
        # TODO: improve logic so that actual floats in company names (unlikely)
        # are handled
        if  isinstance(alpha, float):
            return 0
        # Normalise distance so lies in [0, 1]
        distance = editdistance.eval(alpha, beta) / max(len(alpha), len(beta))
        # Distance is a cost so times -1
        return -1 * distance



def match_score_df(alpha, beta, company_df, index_df, gap_penalty = -1):
    c_a = company_df.loc[alpha, "company name"]
    c_b = index_df.loc[beta, "text"]

    if c_a == '------' or c_b == '------':
        return gap_penalty
    else:
        # If GCV skips a row it returns nan in pandas which this catches
        # TODO: improve logic so that actual floats in company names (unlikely)
        # are handled
        if  isinstance(c_a, float):
            return 0
        # Normalise distance so lies in [0, 1]
        distance = editdistance.eval(c_a, c_b) / max(len(c_a), len(c_b))
        # Distance is a cost so times -1
        return -1 * distance





def needleman_wunsch_df(seq1, seq2, company_df, index_df,  gap_penalty = -1):
    
    # Store length of two sequences
    n = len(seq1)  
    m = len(seq2)
    
    # Generate matrix of zeros to store scores
    score = np.zeros((m+1, n+1))
   
    # Calculate score table
    
    # Fill out first column
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    
    # Fill out first row
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    
    # Fill out all other values in the score matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Calculate the score by checking the top, left, and diagonal cells
            match = score[i - 1][j - 1] + match_score_df(seq1[j-1], seq2[i-1], company_df, index_df)
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    # Create variables to store alignment
    align1 = []
    align2 = []
    
    # Start from the bottom right cell in matrix
    i = m
    j = n
    
    # We'll use i and j to keep track of where we are in the matrix, just like above
    while i > 0 and j > 0: # end touching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]
        
        # Check to figure out which cell the current score was calculated from,
        # then update i and j to correspond to that cell.
        if score_current == score_diagonal + match_score_df(seq1[j-1], seq2[i-1], company_df, index_df):
            align1 += [seq1[j-1]]
            align2 += [seq2[i-1]]
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += [seq1[j-1]]
            align2 += ['------']
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += ['------']
            align2 += [seq2[i-1]]
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += [seq1[j-1]]
        align2 += ['------']
        j -= 1
    while i > 0:
        align1 += ['------']
        align2 += [seq2[i-1]]
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    align1 = align1[::-1]
    align2 = align2[::-1]
    print("Scoring Matrix:")
    print(pd.DataFrame(score))

    align_df = pd.DataFrame()
    align_df["Sequence 1"] = align1
    align_df["Sequence 2"] = align2
    return(align_df)



if __name__ == "__main__":
    wide_df = pd.read_csv("tmo.csv")
    index_df = pd.read_csv("company-index-names-initial-experiment-ed.csv")
    wide_df["Sequence 1"] = np.arange(len(wide_df))
    index_df["Sequence 2"] = np.arange(len(index_df))
    start = time.time()
    
    
    company_alphas = wide_df["company name"].tolist()
    company_betas = index_df["text"].tolist()

    company_alphas = company_alphas[0:100]
    company_betas = company_betas[0:100]
       
    print(company_alphas)

    pd.options.display.max_rows = 200
    output1 = needleman_wunsch_df(wide_df["Sequence 1"], index_df["Sequence 2"], wide_df, index_df)


    joint_df = output1.merge(wide_df,
                             on = "Sequence 1",
                             how = "left")

    joint_df = joint_df.merge(index_df,
                              on = "Sequence 2",
                              how = "left")
    print(joint_df)

    end = time.time()
    print("Time Taken:", end - start)
    # print(output1)
    
    