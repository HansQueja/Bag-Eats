import sqlite3

def inputData():

    food_list = {}

    conn = sqlite3.connect('food.db') 
    cur = conn.cursor() 
    cur.execute("SELECT * FROM food_list")

    result = cur.fetchall()

    for row in result:
        food_item = {}

        food_item["Food_ID"] = row[0]
        food_item["Stall_Name"] = row[1]
        food_item["Food_Name"] = row[2]
        ingredients = row[3].split(',')
        food_item["Ingredients"] = ingredients
        health_benefits = row[4].split(',')
        food_item["Health_Benefits"] = health_benefits
        food_item["Serving"] = row[5]
        food_item["Price"] = row[6]
        food_item["Rating"] = row[7]
        food_item["Nutritional_Rating"] = row[8]
        food_item["Overall_Rating"] = row[9]
        food_time = row[10].split(',')
        food_item["Food_Time"] = food_time

        try:
            dietary_restrictions = row[11].split(',')
            food_item["Dietary_Restriction"] = dietary_restrictions
        except AttributeError:
            food_item["Dietary_Restriction"] = row[11]
            
        try:
            allergen_avoidance = row[12].split(',')
            food_item["Allergen_Avoidance"] = allergen_avoidance
        except AttributeError:
            food_item["Allergen_Avoidance"] = row[12]

        try:
            nutritional_preference = row[13].split(',')
            food_item["Nutritional_Preference"] = nutritional_preference
        except AttributeError:
            food_item["Nutritional_Preference"] = row[13]

        try:
            macronutrients = row[14].split(',')
            food_item["Macronutrients"] = macronutrients
        except AttributeError:
            food_item["Macronutrients"] = row[14]

        food_item["Food_Type"] = row[15]
        food_item["Stall_ID"] = row[16]
        food_item["Calories"] = row[17]
        food_item["URL"] = row[18]

        food_list[row[0]] = food_item

    conn.close()
    return food_list

def filterData(food_list, max_budget, meal_type, dietary_restrictions, allergen_avoidance, nutritional_preference):

    valid_foods = []
    valid_drinks = []
    
    for i in range(1, len(food_list) - 1):
        
        if food_list[i]["Price"] > int(max_budget):
            continue
        
        invalid = False
        
        # check for dietary restrictions
        if dietary_restrictions != "none":
            for restrictions in dietary_restrictions:
                if restrictions not in food_list[i]["Dietary_Restriction"]:
                    invalid = True
                    break
                
        if invalid == True:
            continue
        
        # check for allergen avoidance
        if allergen_avoidance != "none":
            for allergen in allergen_avoidance:
                if allergen not in food_list[i]["Allergen_Avoidance"]:
                    invalid = True
                    break
                
        if invalid == True:
            continue

        # check for nutritional preference
        if nutritional_preference != "none":
            for preference in nutritional_preference:
                if preference in food_list[i]["Nutritional_Preference"]:
                    food_list[i]["Rating"] += 10


        if not meal_type in food_list[i]["Food_Time"]:
            if food_list[i]["Food_Time"][0] in ("FruitDrinks","Beverages"):
                valid_drinks.append(food_list[i])
            continue

        valid_foods.append(food_list[i])
    
    return valid_foods, valid_drinks


def extract(valid_list):
    
    filtered_id = []
    weight = []
    value = []
    food_type = []
    calories = []

    for i in range(1, len(valid_list) - 1):
        filtered_id.append(valid_list[i]["Food_ID"])
        weight.append(valid_list[i]["Price"])
        value.append(valid_list[i]["Overall_Rating"])
        food_type.append(valid_list[i]["Food_Type"])
        calories.append(valid_list[i]["Calories"])

    return filtered_id, weight, value, food_type, calories