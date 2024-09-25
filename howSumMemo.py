def howSum1(targetSum, numbers, memo=None):
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
        remainderResult = howSum1(remainder, numbers, memo)
        
        if remainderResult is not None:
            memo[targetSum]= remainderResult + [num]
            return memo[targetSum]
    memo[targetSum] = None
    return None


