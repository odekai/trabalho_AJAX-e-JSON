from flask import Flask, render_template, jsonify
from views import init_app

app = Flask(__name__)
init_app(app)




if __name__ == "__main__":
    app.run(debug=True)


