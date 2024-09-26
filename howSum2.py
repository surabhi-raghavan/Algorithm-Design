def howSumTab(targetSum, numbers):

    table = [None] * (targetSum + 1)
    table[0] = []


    for currentSum in range(targetSum + 1):

        if table[currentSum] is not None:
            for num in numbers:
                nextSum = currentSum + num
                if nextSum <= targetSum and table[nextSum] is None:
                    table[nextSum] = table[currentSum] + [num]
    
    return table[targetSum]


