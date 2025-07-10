from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# In-memory user session storage
user_sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    user_id = data.get("user_id", "Guest")

    if not message:
        return jsonify({"reply": "Please enter a message."})

    # Initialize session if not exists
    if user_id not in user_sessions:
        user_sessions[user_id] = {}

    session = user_sessions[user_id]

    # Personal thank you response using username
    if message.lower() in ["thank you", "thanks"]:
        reply = (f"You're welcome, {user_id}! Have a nice day. You can ask me again if you want to explore more options.\n"
                 "\nChoose an option:\n1. Know about TechBrew\n2. Coffee Info\n3. Calculate BMI & Get Diet/Coffee Suggestion")
        return jsonify({"reply": reply})

    if message == "1":
        reply = "Welcome to TechBrew Cafe! Enjoy your coffee with passion and energy."

    elif message == "2":
        reply = "We offer various coffee items including the Black Cappuccino made with Brazilian beans!"

    elif message == "3":
        session.clear()
        session["step"] = "awaiting_height_weight"
        reply = "Let's calculate your BMI. Please tell me your height and weight in centimeters and kilograms (format: 170 65)."

    elif session.get("step") == "awaiting_height_weight":
        try:
            height_cm, weight_kg = map(float, message.split())
            height_m = height_cm / 100
            bmi = weight_kg / (height_m ** 2)
            session["bmi"] = bmi
            session["height_cm"] = height_cm
            session["weight_kg"] = weight_kg
            session["step"] = "awaiting_diet_or_coffee"
            reply = f"Your BMI is {bmi:.2f}. Would you like a diet chart or coffee suggestion? Please type 'diet' or 'coffee'."
        except:
            reply = "Please enter height and weight correctly (format: 170 65)."

    elif session.get("step") == "awaiting_diet_or_coffee":
        bmi = session.get("bmi")

        if message.lower() == "diet":
            if bmi < 18.5:
                diet_info = "You are underweight. Aim for a high-calorie balanced diet including nuts, dairy, and lean protein."
            elif 18.5 <= bmi < 24.9:
                diet_info = "You have a normal weight. Maintain a balanced diet with plenty of vegetables and moderate carbs."
            elif 25 <= bmi < 29.9:
                diet_info = "You are overweight. Focus on low-calorie, high-fiber foods, and reduce sugary snacks."
            else:
                diet_info = "You are obese. Consult a dietitian, focus on low-calorie foods, and increase physical activity."

            reply = diet_info + "\nYou can type 'diet', 'coffee', 'calorie', or 'caffeine' for more advice."

        elif message.lower() == "coffee":
            if bmi < 18.5:
                coffee_suggestion = "Try creamy lattes or cappuccinos to add some calories while enjoying coffee."
            elif 18.5 <= bmi < 24.9:
                coffee_suggestion = "Enjoy black or green coffee to maintain your health."
            elif 25 <= bmi < 29.9:
                coffee_suggestion = "Switch to low-calorie options like black coffee. Avoid added sugar."
            else:
                coffee_suggestion = "Prefer plain black coffee and avoid sugary coffee drinks."

            reply = coffee_suggestion + "\nYou can type 'diet', 'coffee', 'calorie', or 'caffeine' for more advice."

        elif message.lower() == "calorie":
            session["step"] = "awaiting_age_gender"
            reply = "Please enter your age and gender (M/F), like this: 25 M"

        elif message.lower() == "caffeine":
            bmi = session.get("bmi")
            if bmi is None:
                reply = "Please calculate your BMI first by typing 3."
            else:
                if bmi < 18.5:
                    caffeine_msg = "You can consume about 300-400 mg of caffeine daily, which is about 3-4 cups of coffee."
                elif 18.5 <= bmi < 24.9:
                    caffeine_msg = "You can safely consume 300-400 mg of caffeine per day, around 3-4 cups of brewed coffee."
                elif 25 <= bmi < 29.9:
                    caffeine_msg = "Limit your caffeine intake to 200-300 mg/day (2-3 cups of black coffee). Avoid sugary coffee."
                else:
                    caffeine_msg = "Stick to no more than 200 mg/day of caffeine. Black coffee is best without sugar or cream."

                session["step"] = "awaiting_specific_coffee"
                reply = caffeine_msg + "\nWould you like to know which specific coffee item suits your caffeine limit? Type 'yes' or 'no'."

        else:
            reply = "Please type 'diet', 'coffee', 'calorie', or 'caffeine'."

    elif session.get("step") == "awaiting_specific_coffee":
        if message.lower() == "yes":
            bmi = session.get("bmi")
            if bmi < 18.5:
                reply = "Try mocha or creamy cappuccino for extra calories and flavor."
            elif 18.5 <= bmi < 24.9:
                reply = "Green coffee or Americano fits your healthy lifestyle."
            elif 25 <= bmi < 29.9:
                reply = "Go for black coffee or cold brew with no sugar."
            else:
                reply = "Choose plain black coffee or espresso. Avoid cream and sugar."
            session["step"] = "awaiting_diet_or_coffee"
        elif message.lower() == "no":
            reply = "Okay! Let me know if you need any other help."
            session["step"] = "awaiting_diet_or_coffee"
        else:
            reply = "Please type 'yes' or 'no'."

    elif session.get("step") == "awaiting_age_gender":
        try:
            age_str, gender = message.split()
            age = int(age_str)
            gender = gender.upper()
            height_cm = session.get("height_cm")
            weight_kg = session.get("weight_kg")

            if not height_cm or not weight_kg:
                reply = "Sorry, I need your height and weight first. Please type 3 to restart."
            else:
                if gender == "M":
                    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
                elif gender == "F":
                    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
                else:
                    reply = "Please enter gender as M or F."
                    return jsonify({"reply": reply})

                reply = (f"Your estimated BMR is {bmr:.0f} calories/day.\n"
                         f"To maintain weight: ~{bmr:.0f} kcal/day.\n"
                         f"To lose weight: ~{bmr - 500:.0f} kcal/day.\n"
                         f"To gain weight: ~{bmr + 500:.0f} kcal/day.\n"
                         f"You can also ask me how much caffeine is suitable for your BMI by typing 'caffeine'.")

                session["step"] = "awaiting_diet_or_coffee"
        except:
            reply = "Please enter your age and gender in the correct format: 25 M or 22 F"

    else:
        reply = ("Hi! \U0001F44B If you want to know about this website or have any queries, feel free to ask.\n\n"
                 "Choose an option:\n1. Know about TechBrew\n2. Coffee Info\n3. Calculate BMI & Get Diet/Coffee Suggestion")

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
