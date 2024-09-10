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
    inputString:
    ip:
    

Function subsetOfThree(input, start, subset):
    If Length of subset == 3
        Print subset
        Return
    If start >= Length of elements
        Return
    For i from start to length of input-1
        Call subsetOfThree(input, i+1, subset+ [input[i]])
    
"""

def subsetOfThree(ip, start, subset):
    
    """
    - ip: list of elements to choose sets of 3 subsets from
    
    - start: index from which we start considering elements
    
    - subset: the subset being constructed
    
    """
    n=len(ip) 
    subset_length= len(subset)
    
    # if there is a subset of exactly 3 elemets, print it 
    
    if subset_length == 3: 
        print(tuple(subset)) # Convert the list to a tuple
        return
    
    # if  we don't have enough elements left to pick from 
    
    if start >= n:
        return
    
    # Loop through the remaining elements 
    
    for i in range (start, n):
        subsetOfThree(ip, i+1, subset+[ip[i]])

def main():
    inputString =input("Enter the elements of the list")
    
    try:
        # Convert the input to a list of integers
        ip= list(map(int, inputString.split()))
        
    except ValueError:
        
        print('Invalid Input')
        return
    
    n= len(ip)
    
    # Check if the list has atleast 3 elements 
    if n>=3:
        subsetOfThree(ip, 0, [])
    else:
        print('Not enough elements')

if __name__== "__main__":
    main()
        
    
        