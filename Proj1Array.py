"""
Design and implement your own algorithm that takes the array A with size m+n as input where:
Subarray A[1], A[2],...A[m] sorted in ascending order
Subarray A[m+1], A[m+2],...A[n] sorted in ascending order
and merges the two subarrays using an auxiliary array Aux of size min {m, n} back into array A sorted in ascending order. You must design and implement your own sorting function. Use of sorting functions in libraries is not permitted. 
"""

def mergearray(A, m, n):
    if m == 0:
        return A
    if n == 0:
        return A
    
    size = min(m,n)
    aux = []
    
    if (m<=n): 
        aux = A[:m]
        i=0
        k=0
        j=m
        
        while i <m and j < m+n:
            if aux[i] <= A[j]:
                A[k] = aux[i]
                i+=1
            else:
                A[k] = A[j]
                j+=1
            k+=1 
        
        while i < m:
            A[k] =aux[i]
            i+=1
            k+=1
    else: 
        aux = A[m:m+n]
        i = m-1
        j= n-1
        k = m+n-1
        
        while i>=0 and j>=0:
            if A[i] > aux[j]:
                A[k] = A[i]
                i-=1
            else:
                A[k] = aux[j]
                j-=1
            k-=1
            
            while j>=0:
                A[k] =aux[j]
                j-=1
                k-=1
    return A
        
def main():
    first_input = input("Enter elements of the first sorted subarray (space-separated): ").strip()
    if first_input:
        first = list(map(int, first_input.split()))
    else:
        first = []
    m = len(first)

    # Input for the second sorted subarray
    second_input = input("Enter elements of the second sorted subarray (space-separated): ").strip()
    if second_input:
        second = list(map(int, second_input.split()))
    else:
        second = []
    n = len(second)

    # Combine the two subarrays into array A
    A = first + second
    print(f"\nCombined Array A before merging: {A}")

    # Merge the subarrays
    merged_A = mergearray(A, m, n)

    # Display the merged array
    print("\n=== Merged Sorted Array ===")
    print(merged_A)

if __name__ == "__main__":
    main()