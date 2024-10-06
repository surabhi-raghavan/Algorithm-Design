def rectanglemultiplication(multiplicand, multiplier):
    
    sign = -1 if (multiplicand < 0) ^ (multiplier < 0) else 1

    x, y = abs(multiplicand), abs(multiplier)

    x_str = str(x)
    y_str = str(y)

    max_len = max(len(x_str), len(y_str))

    k = max_len // 2
    
    if k == 0:
        return (x * y) * sign

    a = x // (10 ** k)
    b = x % (10 ** k)
    c = y // (10 ** k)
    d = y % (10 ** k)
    
    ac = rectanglemultiplication(a, c)
    ad = rectanglemultiplication(a, d)
    bc = rectanglemultiplication(b, c)
    bd = rectanglemultiplication(b, d)

    product = (ac * (10 ** (2 * k))) + ((ad + bc) * (10 ** k)) + bd
    
    return product * sign

print(rectanglemultiplication(-45952456856498465985, -98654651986546519856))