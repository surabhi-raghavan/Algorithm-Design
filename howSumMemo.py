def howSum_memo(targetSum, numbers, memo=None):
    if memo is None:
        memo = {}
    if targetSum in memo:
        return memo[targetSum]
    if targetSum == 0:
        return []
    if targetSum < 0:
        return None
    
    for num in numbers:
        remainder = targetSum - num
        remainderResult = howSum_memo(remainder, numbers, memo)
        if remainderResult is not None:
            memo[targetSum] = remainderResult + [num]
            return memo[targetSum]
    
    memo[targetSum] = None
    return None


if __name__ == "__main__":
    targetSum= int(input("Enter the Target Sum\n"))
    numbers = list(map(int, input("Enter numbers in the array with a space inbetween\n").split()))
    print(howSum_memo(targetSum, numbers))