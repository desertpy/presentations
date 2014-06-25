def _sum(data):
    total = 0
    for d in data:
        total += d
    return total

def mean(data):
    n = len(data)
    return _sum(data) / n
