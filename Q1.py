"""
PSEUDOCODE: 
Input: A list of integers 
Output: All subsets of 3 elements
Variables:
    n (int): length of list
    subset_length (int): length of the subset being created 
    start (int): index from which we start considering elements
    subset (list): the subset being constructed
    i (int): loop viariable
    inputString (String): Input variable 
    ip (list): convert string to list integer
    

Function subsetOfThree(input, start, subset):
    If Length of subset == 3
        Print subset
        Return
    If start >= Length of elements
        Return
    For i from start to length of input-1
        Call subsetOfThree(input, i+1, subset+ [input[i]])
    
"""

def subsetOfThree(ip, start, subset, unique_subsets):
    
    """
    - ip: list of elements to choose sets of 3 subsets from
    
    - start: index from which we start considering elements
    
    - subset: the subset being constructed
    
    """
    n=len(ip) 
    subset_length= len(subset)
    
    # if there is a subset of exactly 3 elemets, print it 
    
    if subset_length == 3: 
        unique_subsets.add(tuple(sorted(subset)))
        return
    
    # if  we don't have enough elements left to pick from 
    
    if start >= n:
        return
    
    # Loop through the remaining elements 
    
    for i in range (start, n):
        subsetOfThree(ip, i+1, subset+[ip[i]], unique_subsets)

def main():
    inputString =input("Enter the elements of the list\n")
    
    try:
        # Convert the input to a list of integers
        ip= list(map(int, inputString.split(',')))
        
    except ValueError:
        
        print('Invalid Input')
        return
    
    n= len(ip)
    
    # Check if the list has atleast 3 elements 
    if n>=3:
        unique_subsets= set()
        subsetOfThree(ip, 0, [], unique_subsets)
        for subset in unique_subsets:
            print(subset)
    else:
        print('Not enough elements')

if __name__== "__main__":
    main()
        
    
        