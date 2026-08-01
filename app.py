from flask import Flask
from dotenv import load_dotenv
from config import Config

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def home():
    return "Job Tracker is alive!"

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])