from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.sessions.backends.db import SessionStore
from django.contrib import messages
from django.shortcuts import redirect

from base.read import inputData, filterData, extract
from base.knapsack import knapsack
import sqlite3

# Create your views here.
food_list = inputData()

def home(request):
    if 'user_id' in request.session:
        name = request.session['name']
        return render(request, 'home.html', {"name":name})
    else:
        return redirect('login')

def about(request):
    if 'user_id' in request.session:
        name = request.session['name']
        return render(request, 'about.html', {"name":name})
    else:
        return redirect('login')

def profile(request):
    if 'user_id' in request.session:
        name = request.session['name']
        return render(request, 'profile.html', {"name":name})
    else:
        return redirect('login')

def login(request):
    if request.method == "POST":

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        email = request.POST.get("login-email")
        password = request.POST.get("login-password")

        cur.execute("SELECT * FROM users WHERE email = (?)", (email,))
        account = cur.fetchone()

        if account and check_password(password, account[7]):
            
            s = SessionStore()
            s['user_id'] = account[0]
            s['name'] = account[1]
            s['email'] = account[2]
            s['age'] = account[3]
            s['height'] = account[4]
            s['weight'] = account[5]
        
            request.session = s
            print(request.session)
            conn.close()

            return redirect('home')
        elif account:
            messages.error(request, "Your password is incorrect. Please check your credentials.")
            return render(request, "login.html")
        
    return render(request, 'login.html')

def register(request):

    if request.method == "POST":

        conn = sqlite3.connect('users.db')
        cur = conn.cursor()

        full_name = request.POST.get("reg-name")
        email = request.POST.get("reg-email")
        password1 = request.POST.get("reg-password")
        password2 = request.POST.get("reg-cpassword")
        age = request.POST.get("reg-age")
        height = request.POST.get("reg-height")
        weight = request.POST.get("reg-weight")

        if full_name == None:
            return redirect('register')
        
        cur.execute("SELECT email FROM users")
        db_email = [email[0] for email in cur.fetchall()]
        
        cur.execute("SELECT COUNT(*) FROM users")
        db_count = cur.fetchall()
        count = db_count[0][0]

        if int(age) <= 0:
            messages.error(request, "Enter a valid age.")
            return render(request, "register.html")
        
        if int(height) <= 0:
            messages.error(request, "Enter a valid height in centimeters")
            return render(request, "register.html")
        
        if int(weight) <= 0:
            messages.error(request, "Enter a valid weight in kilograms")
            return render(request, "register.html")

        if email in db_email:
            print("email problem")
            messages.error(request, "The email you've entered is already in use. Try a new email.")
            return render(request, "register.html")

        if password1 != password2:
            print("password problem")
            messages.error(request, "The passwords don't match. Please try again.")
            return render(request, "register.html")
        
        meter_height = int(height) / 100.0
        bmi = round(float(weight) / (meter_height * meter_height), 2)

        cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (count + 1, full_name, email, 
                                                                 age, height, weight, bmi, make_password(password1),))
        
        print("executed")
        conn.commit()
        conn.close()
        return render(request, "login.html")

    return render(request, "register.html")

def logout(request):
    request.session.flush()
    return redirect('login')

def form(request):

    if request.method == "POST":
        #print(list(request.POST.items()))
        max_budget = int(request.POST.get('max-budget'))
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

        drink_budget = 0
        total_calories = 0

        if max_budget >= 70 and meal_type != "Drinks":
            drink_budget = 20
            max_budget -= drink_budget
            
        valid_foods, valid_drinks = filterData(food_list, max_budget, meal_type, dietary_restrictions, allergen_avoidance, nutritional_preference)

        filtered_id, weight, value, food_type, calories = extract(valid_foods)

        id_result, calories, total_price, spare_money = knapsack(int(max_budget), filtered_id, weight, value, food_type, calories, len(filtered_id))
        drink_budget += spare_money
        total_calories += calories
        #print(drink_budget)

        results_food = []
        results_drinks = []

        for i in id_result:
            if food_list[i]["Food_Type"] == "drinks":
                results_drinks.append(food_list[i])
            else:
                results_food.append(food_list[i])

        if meal_type != "Drinks":
            filtered_id, weight, value, food_type, calories = extract(valid_drinks)
            id_result, calories, total_price_drinks, spare_money = knapsack(int(drink_budget), filtered_id, weight, value, food_type, calories, len(filtered_id))
            for i in id_result:
                results_drinks.append(food_list[i])
            
            total_calories += calories
            total_price += total_price_drinks
        
        return render(request, 'combination.html', {"foods": results_food, "drinks": results_drinks, "total_price": total_price, "total_calories": total_calories})

    return render(request, 'form.html')

def description(request, Food_ID):
    print("HERE DESC")
    food = food_list[Food_ID]
    return render(request, 'description.html', {"food": food})
    
def moreinfo(request):
    return render(request, 'moreinfo.html')