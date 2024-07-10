def calculate_beverage_balance(nutrients):
    def score_nutrient(value, ideal_range):
        if value == -1:  # No data provided
            return None
        low, high = ideal_range
        if low <= value <= high:
            return 1
        elif value < low:
            return value / low
        else:
            return max(0, 1 - (value - high) / high)

    ideal_ranges_beverage = {
        'calories': (0, 150),
        'total_fat': (0, 3),
        'saturated_fat': (0, 1),
        'trans_fat': (0, 0.5),
        'sodium': (0, 100),
        'total_carbs': (0, 20),
        'sugars': (0, 10),
        'protein': (0, 10),
        'vitamin_c': (0, 100),
        'calcium': (0, 30),
        'potassium': (0, 500)
    }

    scores = {}
    total_nutrients = len(ideal_ranges_beverage)
    nutrients_with_data = 0

    for nutrient, value in nutrients.items():
        if nutrient in ideal_ranges_beverage:
            if value != -1:  # Check if data is provided
                score = score_nutrient(value, ideal_ranges_beverage[nutrient])
                if score is not None:
                    scores[nutrient] = score
                    nutrients_with_data += 1

    if not scores:
        return 0, 0

    balance_score = sum(scores.values()) / len(scores)
    completeness = nutrients_with_data / total_nutrients

    return balance_score * 100, completeness * 100

# Example usage for a beverage
# IF DATA IS NOT AVAILABLE, enter -1
beverage_item = {
    'calories': 96,
    'total_fat': 3,
    'saturated_fat': 1,
    'trans_fat': -1, 
    'sodium': 30,
    'total_carbs': 25,
    'sugars': 23,
    'protein': 3,
    'vitamin_c': -1,  
    'calcium': 2,
    'potassium': 21
}

beverage_balance, beverage_completeness = calculate_beverage_balance(beverage_item)
print(f"\nBeverage Nutritional Balance Score: {beverage_balance:.2f}")
print(f"Beverage Data Completeness: {beverage_completeness:.2f}%")