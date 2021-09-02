def getThePrice(arrayOfPrices, method = "avg"):
    method = method.lower()
    if method == "avg":
        finalPrice = 0
        for coinKey in arrayOfPrices.keys():
            finalPrice += arrayOfPrices[coinKey]
        finalPrice = finalPrice / len(arrayOfPrices.keys())
    elif method == "max":
        finalPrice = 0
        for coinKey in arrayOfPrices.keys():
            finalPrice = max(finalPrice, arrayOfPrices[coinKey])
    elif method == "min":
        finalPrice = float('inf')
        for coinKey in arrayOfPrices.keys():
            finalPrice = min(finalPrice, arrayOfPrices[coinKey])

    return round(finalPrice, 6)

