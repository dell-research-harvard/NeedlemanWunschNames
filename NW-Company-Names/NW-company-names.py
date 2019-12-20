import numpy as np
from random import choice, choices, randrange
import string
import time
import editdistance
import pandas as pd
from math import isnan
wide_df = pd.read_csv("tmo.csv")
index_df = pd.read_csv("company-index-names-initial-experiment-ed.csv")

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(choice(letters) for i in range(stringLength))


def match_score(alpha, beta, gap_penalty = -1, match_award = 1, mismatch_penalty = -1):
    
#     company_alphas = [ # This is the index
#   "アース商會",                
#   "アイエ書店",                
#   "アイゼンベルグ商會",       
#   "アイデアル石鹸",          
#   "アイデン",                  
#   "アコマ醫科工業",            
#   "アサノコンクリート",       
#   "アサヒイブニングニュース祉",
#   "アサヒ藝能新聞社",          
#  "アサヒ商店"
#     ]

    company_alphas = wide_df["company name"].tolist()

#     company_betas = [ # This is the book
#           "アース商會",                
#   "アイエ書店",                
# #   "アイゼンベルグ商會", FAKING SKIPPED COMPANY - should skip digit 2       
#   "アイデアル石鹸",          
#   "アイデン",                  
#   "アコマ醫科工業",            
#   "アサノコンクリート",       
#   "アサヒイブニングニュース祉",
#   "アサヒ藝能新聞社",          
#  "アサヒ商店"

#     ]

    company_betas = index_df["text"].tolist()


    if alpha == '-' or beta == '-':
        return gap_penalty
    else:
        alpha = int(alpha)
        beta = int(beta)

        c_a = company_alphas[alpha]
        c_b = company_betas[beta]
        # print(c_a, "------", c_b)

        if  isinstance(c_a, float):
            return 0
        distance = editdistance.eval(c_a, c_b) / max(len(c_a), len(c_b))
        
        return -1 * distance






def needleman_wunsch(seq1, seq2, gap_penalty = -1, match_award = 1, mismatch_penalty = -1):
    
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
            match = score[i - 1][j - 1] + match_score(seq1[j-1], seq2[i-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            # Record the maximum score from the three possible scores calculated above
            score[i][j] = max(match, delete, insert)
    
    # Traceback and compute the alignment 
    
    # Create variables to store alignment
    align1 = ""
    align2 = ""
    
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
        if score_current == score_diagonal + match_score(seq1[j-1], seq2[i-1]):
            align1 += seq1[j-1]
            align2 += seq2[i-1]
            align1 += " "
            align2 += " "
            i -= 1
            j -= 1
        elif score_current == score_up + gap_penalty:
            align1 += seq1[j-1]
            align2 += '-'
            align1 += " "
            align2 += " "
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += '-'
            align2 += seq2[i-1]
            align1 += " "
            align2 += " "
            i -= 1

    # Finish tracing up to the top left cell
    while j > 0:
        align1 += seq1[j-1]
        align2 += '-'
        align1 += " "
        align2 += " "
        j -= 1
    while i > 0:
        align1 += '-'
        align2 += seq2[i-1]
        align1 += " "
        align2 += " "
        i -= 1
    
    # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
    # These two lines reverse the order of the characters in each sequence.
    # align1 = align1[::-1]
    # align2 = align2[::-1]
    print("Scoring Matrix:")
    print(pd.DataFrame(score))

    return(align1, align2)


if __name__ == "__main__":
    start = time.time()

    print(editdistance.eval('banana', 'bahama'))
    print(editdistance.eval('bahama', 'banana'))
       
    string_a = [str(x) for x in range(9, -1, -1)]  # randomString(200)
    

    string_b = [str(x) for x in range(9, -1, -1)] #randomString(200)

    output1, output2 = needleman_wunsch(string_a, string_b)
    end = time.time()
    print("Time Taken:", end - start)
    print("Book Sequence: ", output1)
    print("Index Sequence:", output2)
    
    print(wide_df.loc[0:9, "company name"])
    print(index_df.loc[0:9, "text"])
