from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *

app_views.register_blueprint(index)
app_views.register_blueprint(states)
app_views.register_blueprint(cities)
