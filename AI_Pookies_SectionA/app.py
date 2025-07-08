from flask import Flask, request, render_template
import pickle

# Load trained model and vectorizer
model = pickle.load(open("fake_news_model.pkl", 'rb'))
vector = pickle.load(open("vectorizer.pkl", 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/Prediction', methods=['GET', 'POST'])
def Prediction():
    if request.method == "POST":
        news = request.form['news']
        prediction = model.predict(vector.transform([news]))
        print(prediction)
        # Pass the prediction result to the template
        return render_template("Prediction.html", Prediction_text=f"News headline is  {prediction[0]}")
    else:
        # For GET requests, no prediction yet, show a default message or blank
        return render_template("Prediction.html", Prediction_text="Please enter a news headline to predict.")

if __name__ == '__main__':
    app.run(debug=True)
