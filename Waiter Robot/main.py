from flask import Flask, request, render_template
from flask_cors import CORS
from app import Algo

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/order", methods=["POST"])
def order():
    orders = request.json
    print(orders)
    algo = Algo()
    details = algo.get_details(orders)
    # sort the details according to time if time and cost are same then prefer the one with less path
    details.sort(key=lambda x: (x["time"], x["cost"], len(x["path"])))
    # print(details)
    if len(details) > 0:
        return {"details": details}
    else:
        # return internal server error with status code 500
        return {"error": "Internal Server Error"}, 500

# ADD THIS PART to actually run the app!
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
