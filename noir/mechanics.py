from .dice import noir_roll

def difficulty(value):
    r = noir_roll()
    total = r["tärningssumma"] + value
    success = total >= 20
    return r, total, success

def opposition(v1, v2):
    r1 = noir_roll()
    r2 = noir_roll()

    total1 = r1["tärningssumma"] + v1
    total2 = r2["tärningssumma"] + v2

    return (r1, total1), (r2, total2)

def initiative(values):
    results = []

    for i, v in enumerate(values):
        r = noir_roll()
        total = r["tärningssumma"] + v
        results.append((i+1, total, r))

    return sorted(results, key=lambda x: x[1], reverse=True)