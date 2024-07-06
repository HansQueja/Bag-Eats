from django.shortcuts import render
from base.read import inputData, filterData
from base.knapsack import knapsack

# Create your views here.
food_list = inputData()

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def form(request):

    if request.method == "POST":
        print(list(request.POST.items()))
        max_budget = request.POST.get('max-budget')
        meal_type = request.POST.get('meal-type')
        dietary_restrictions = request.POST.getlist('dietary-restrictions')

        if not dietary_restrictions:
            dietary_restrictions = "none"

        allergen_avoidance = request.POST.getlist('allergen-avoidance')

        if not allergen_avoidance:
            allergen_avoidance = "none"

        nutritional_preference = request.POST.getlist('nutritional-preferences')

        if not nutritional_preference:
            nutritional_preference = "none"

        filtered_id, value, weight = filterData(food_list, max_budget, meal_type, dietary_restrictions, allergen_avoidance, nutritional_preference)
        id_result = knapsack(int(max_budget), filtered_id, weight, value, len(filtered_id))
        results_food = []
        results_drinks = []
        total_price = 0

        for id in id_result:
            if food_list[id]["Food_Type"] == "drinks":
                results_drinks.append(food_list[id])
            else:
                results_food.append(food_list[id])

            total_price += food_list[id]["Price"]
            
        return render(request, 'combination.html', {"foods": results_food, "drinks": results_drinks, "total_price": total_price})

    return render(request, 'form.html')

def description(request, Food_ID):
    print("HERE DESC")
    food = food_list[Food_ID]
    return render(request, 'description.html', {"food": food})
    
def moreinfo(request):
    return render(request, 'moreinfo.html')

def profile(request):
    return render(request, 'profile.html')