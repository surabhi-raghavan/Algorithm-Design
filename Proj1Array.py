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
    if m <= n:
        Aux = A[:m]  
        i = 0        
        k = 0        
        j = m        

        while i < m and j < m + n:
            if Aux[i] <= A[j]:
                A[k] = Aux[i]
                i += 1
            else:
                A[k] = A[j]
                j += 1
            k += 1

        while i < m:
            A[k] = Aux[i]
            i += 1
            k += 1
    else:
        Aux = A[m:m+n]  
        i = m - 1       
        j = n - 1       
        k = m + n - 1   

        while i >= 0 and j >= 0:
            if A[i] > Aux[j]:
                A[k] = A[i]
                i -= 1
            else:
                A[k] = Aux[j]
                j -= 1
            k -= 1

        while j >= 0:
            A[k] = Aux[j]
            j -= 1
            k -= 1
    return A
        
def main():
    first_input = input("Enter elements of the first sorted subarray (space-separated): ").strip()
    if first_input:
        first = list(map(int, first_input.split()))
    else:
        first = []
    m = len(first)

    second_input = input("Enter elements of the second sorted subarray (space-separated): ").strip()
    if second_input:
        second = list(map(int, second_input.split()))
    else:
        second = []
    n = len(second)
    A = first + second

    merged_A = mergearray(A, m, n)

    print("\nMerged Sorted Array")
    print(merged_A)

if __name__ == "__main__":
    main()