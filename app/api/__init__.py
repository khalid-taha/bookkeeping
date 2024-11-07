# app/api/__init__.py

from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, version='1.0', title='Bookkeeping API',
          description='APIs for Internal Module Communication')

# Import API modules
from .accounts_api import accounts_ns
from .transactions_api import transactions_ns
from .auth_api import auth_ns

# Add Namespaces to the API
api.add_namespace(accounts_ns)
api.add_namespace(transactions_ns)
api.add_namespace(auth_ns)