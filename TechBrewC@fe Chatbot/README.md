ID: C223226
ID: C223228
ID: C223229
                                 **Project Name:☕ TechBrew Cafe – Smart Café Website with AI Chatbot**



**TechBrew Cafe** is a dynamic, user-friendly web-based café management system built using PHP, MySQL, Bootstrap, and integrated with a Python-based AI chatbot using OpenAI's GPT API.

It simulates a real-world café experience with online ordering, membership listings, and a smart chatbot that can answer questions, share coffee facts, and even calculate your BMI.

---

 🚀 Features

- 🛒 **Product Catalog** – Browse coffees, machines, and sweets.
- 📦 **Order Now** – Add items to cart and simulate purchases.
- 👥 **Membership List** – View registered café members from MySQL.
- 📧 **Contact Form** – Send messages directly to the café.
- 
- 🤖 **AI Chatbot (TechBrew Bot)** – 
  - Explains café info
  - Shares coffee knowledge
  - Calculates BMI & gives personalized coffee/diet suggestions
- 🎥 **Hero Video Background** – Engaging landing section with autoplay video.



🛠 Technologies Used

 Frontend:
- HTML5, CSS3, JavaScript
- Bootstrap 5
- Bootstrap Icons

Backend:
- PHP 8+
- MySQL (via phpMyAdmin or XAMPP)

 AI Chatbot:
- Python 3 (Flask)
- OpenAI GPT (via `openai` library)
- `curl` or Postman for API testing

---

🧠 AI Chatbot Workflow

- **Frontend (JavaScript)** calls Flask `/chat` API with user input.
- **Flask Backend**:
  - Option 1: Returns TechBrew info.
  - Option 2: Returns coffee facts.
  - Option 3: Starts BMI calculator flow.
  - Uses OpenAI GPT if user input doesn't match known options.
- **Optional Logging**: `save_chat.php` stores chats in MySQL.

---

 💬 Example Chat



You: 1
Bot: TechBrew Cafe is a cozy digital cafe where coffee meets creativity...

You: 3
Bot: Great! Enter your height and weight (e.g., 170 65)

You: 170 65
Bot: Your BMI is 22.5 – considered normal. Enjoy a light roast americano!



---

 ⚙ Setup Instructions

 ## 1. PHP + MySQL
- Install [XAMPP](https://www.apachefriends.org/index.html)
- Place project files in `htdocs/techbrew`
- Create database `techbrew` and import table structures (members, orders, etc.)

  
 ## 2. Python AI Backend
- Install Python 3.x
- Install packages:
- bash
- pip install flask openai

* Run chatbot backend:

  bash
  
  python techbrew_bot.py

  python test_flask.py
  

### 3. .env Setup (Optional)

* Save your OpenAI key:

  bash
  OPENAI_API_KEY=your-key-here.
---

## 📬 Contact

Created with ☕ by **TechBrew Team**
For help or contributions, email us at: [info@techbrewcafe.com](mailto:info@techbrewcafe.com)

## 📝 License

This project is open-source and free to use for learning and educational purposes.

```
