from flask import Flask
from flask_cors import CORS   # 👈 add this

def create_app():
    app = Flask(__name__)

    # ✅ Enable CORS for frontend requests
    CORS(app)

    # Import and register your blueprint
    from app.routes import main
    app.register_blueprint(main)

    return app


# ✅ Optional: allow running directly with `python app.py`
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
