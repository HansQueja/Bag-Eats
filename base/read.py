import sqlite3

def inputData():

    food_list = {}

    conn = sqlite3.connect('food.db') 
    cur = conn.cursor() 
    print("here")
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
        food_time = row[8].split(',')
        food_item["Food_Time"] = food_time
        dietary_restrictions = row[9].split(',')
        food_item["Dietary_Restriction"] = dietary_restrictions
        allergen_avoidance = row[10].split(',')
        food_item["Allergen_Avoidance"] = allergen_avoidance
        nutritional_preference = row[11].split(',')
        food_item["Nutritional_Preference"] = nutritional_preference
        macronutrients = row[12].split(',')
        food_item["Macronutrients"] = macronutrients
        food_item["Food_Type"] = row[13]

        food_list[row[0]] = food_item

    conn.close()
    return food_list

def filterData(food_list, max_budget, meal_type, dietary_restrictions, allergen_avoidance, nutritional_preference):

    valid_foods = []
    value = []
    weight = []
    #print(food_list)
    for i in range(1, len(food_list) - 1):
        #print("Check 1")
        if food_list[i]["Price"] > int(max_budget):
            continue
        elif not meal_type in food_list[i]["Food_Time"]:
            print("here meal type")
            continue
        
        invalid = False
        #print("Check 2")
        # check for dietary restrictions
        if dietary_restrictions != "none":
            for restrictions in dietary_restrictions:
                print(restrictions)
                if restrictions not in food_list[i]["Dietary_Restriction"]:
                    invalid = True
                    break
                
        if invalid == True:
            continue
        #print("Check 3")
        # check for allergen avoidance
        if allergen_avoidance != "none":

            for allergen in allergen_avoidance:
                if allergen not in food_list[i]["Allergen_Avoidance"]:
                    invalid = True
                    break
                
        if invalid == True:
            continue

        #print("Check 4")
        # check for nutritional preference

        if nutritional_preference != "none":

            for preference in nutritional_preference:
                if preference in food_list[i]["Nutritional_Preference"]:
                    food_list[i]["Rating"] += 2
                    print(food_list[i]["Rating"])

        #print(food_list[i])

        valid_foods.append(food_list[i]["Food_ID"])
        value.append(food_list[i]["Rating"])
        weight.append(food_list[i]["Price"])
    
    return valid_foods, value, weight
