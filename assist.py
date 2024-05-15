def remove_outlier(a):
    total_sum = sum(a)
    common_sign = (total_sum >= 0) 

    for i, num in enumerate(a):
        current_sign = (num >= 0)
        if current_sign != common_sign:
            print(f"Removing outlier: {num}")
            return [x for j, x in enumerate(a) if j != i]
    
    return a
