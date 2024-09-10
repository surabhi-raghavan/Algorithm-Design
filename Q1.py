"""
PSEUDOCODE: 
Input: A list of integers 
Output: All subsets of 3 elements
Variables
    n: length of list
    

Function subsetOfThree(input, start, subset):
    If Length of subset == 3
        Print subset
        Return
    If start >= Length of elements
        Return
    For i from start to length of input-1
        Call subsetOfThree(input, i+1, subset+ [input[i]])
    
"""
