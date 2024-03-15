from flask import Flask
from home.views import home

app = Flask(__name__,static_folder=None)

app.register_blueprint(home)

if __name__ == '__main__':
    app.run(debug=True)
