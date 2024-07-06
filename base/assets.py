
database_password = "AdZ_rox190"

allergies = ["nut", "soy", "dairy", "seafood", "gluten"]
time = ["Lunch", "Meryenda", "Dinner", "Snack"]

command = """
SELECT food_details.food_id, 
		food_details.name, 
        food_details.serving_size, 
        food_details.price, 
        food_details.rating, 
        food_details.nutritional_value,
        food_details.price_rating_nutrition,
        time.food_time,
        food_details.food_type, 
        preference.nutritional_preference,
        macronutrient.macronutrients,
        allergen.allergen,
        food.ingredients_id,
        food.stall_id
FROM food_details
JOIN time 
  ON food_details.food_id = time.food_id
JOIN preference
  ON food_details.food_id = preference.food_id AND food_details.stall_id = preference.stall_id
JOIN macronutrient
  ON food_details.food_id = macronutrient.food_id AND food_details.stall_id = macronutrient.stall_id
JOIN allergen
  ON food_details.food_id = allergen.food_id AND food_details.stall_id = allergen.stall_id
JOIN food
  ON food_details.food_id = food.food_id;
"""