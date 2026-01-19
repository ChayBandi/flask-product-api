from flask import Flask
from flask_restx import Api
import psycopg2
import os
from dotenv import load_dotenv
from db_config import get_connection, release_connection
load_dotenv()
from routes.product_routes import product_ns

app = Flask(__name__)

api = Api(
    app,
    title="Product Management API",
    version="1.0",
    description="CRUD API for Products"
)

api.add_namespace(product_ns)

@app.route("/")
def home():
    return "Product API Running"

if __name__ == "__main__":
    app.run(debug=True)

