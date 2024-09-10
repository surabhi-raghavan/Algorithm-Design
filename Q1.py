"""
PSEUDOCODE: 
Input: A list of integers 
Output: All subsets of 3 elements
Variables
    n: length of list
    subset_length: length of the subset being created 
    start: 
    subset: 
    i: 

Function subsetOfThree(input, start, subset):
    If Length of subset == 3
        Print subset
        Return
    If start >= Length of elements
        Return
    For i from start to length of input-1
        Call subsetOfThree(input, i+1, subset+ [input[i]])
    
"""

def subsetOfThree(input, start, subset):
    n=len(input)
    subset_length= len(subset)
    
    if subset_length == 3:
        print(tuple(subset))
        return
    if start >= n:
        return
    
    for i in range (start, n):
        