from flask import Flask
from routes import api  # Mengimpor blueprint dari routes.py

app = Flask(__name__)

# Registrasi blueprint tanpa prefix atau dengan prefix jika diinginkan
app.register_blueprint(api)

if __name__ == '__main__':
    app.run(debug=True)