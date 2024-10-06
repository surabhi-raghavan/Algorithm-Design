def ala_carte_multiplication(multiplicand, multiplier):
    
    sign = -1 if (multiplicand < 0) ^ (multiplier < 0) else 1
    multiplicand, multiplier = abs(multiplicand), abs(multiplier)
    multiplicand_str = str(multiplicand)
    multiplier_str = str(multiplier)
    multiplicand_str = multiplicand_str[::-1]
    multiplier_str = multiplier_str[::-1]
    partial_sums = [0] * (len(multiplicand_str) + len(multiplier_str))

    for i in range(len(multiplicand_str)):
        for j in range(len(multiplier_str)):
            digit_mul = int(multiplicand_str[i]) * int(multiplier_str[j])
            partial_sums[i + j] += digit_mul

            partial_sums[i + j + 1] += partial_sums[i + j] // 10
            partial_sums[i + j] %= 10

    while len(partial_sums) > 1 and partial_sums[-1] == 0:
        partial_sums.pop()
    
    result_str = ''.join(map(str, partial_sums[::-1]))
    result = int(result_str) * sign
    
    return result

print(ala_carte_multiplication(-45952456856498465985 ,-98654651986546519856))