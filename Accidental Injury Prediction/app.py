import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the trained classifier model
classifier = pickle.load(open('classifier.pkl', 'rb'))

@app.route('/')
def home():
    # Render the home page with the input form
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    # API endpoint for predictions using JSON input
    try:
        data = request.json['data']
        data = np.array(data).reshape(1, -1)
        output = classifier.predict(data)
        return jsonify({'prediction': output[0]})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/predict', methods=['POST'])
def predict():
    # Collect input data from the form
    try:
        data = [float(x) for x in request.form.values()]
        data = np.array(data).reshape(1, -1)

        # Predict using the classifier
        output = classifier.predict(data)[0]

        # Debugging: Print prediction output
        print(f"Prediction Output: {output}")

        # Map numeric predictions to severity levels
        if output == 2:
            return render_template('medium.html')
        elif output == 1:
            return render_template('minor.html')
        elif output == 0:  # Assuming 0 corresponds to "Maximum"
            return render_template('maximum.html')
        else:
            return render_template('home.html', prediction_text="Unexpected prediction output.")
    except Exception as e:
        # Handle exceptions and return to the home page with an error message
        return render_template('home.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
