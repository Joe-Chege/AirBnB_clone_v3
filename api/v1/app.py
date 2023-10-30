#!/usr/bin/python3
""" Flask Application """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)

# Set the database connection URL from environment variables
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqldb://{os.getenv('HBNB_MYSQL_USER', 'hbnb_dev')}:"
    f"{os.getenv('HBNB_MYSQL_PWD', 'hbnb_dev_pwd')}@"
    f"{os.getenv('HBNB_MYSQL_HOST', 'localhost')}/"
    f"{os.getenv('HBNB_MYSQL_DB', 'hbnb_dev_db')}"
)

# Close database connection after each request
@app.teardown_appcontext
def teardown_db(error):
    storage.close()

# Handle 404 errors
@app.errorhandler(404)
def handle_404(error):
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
