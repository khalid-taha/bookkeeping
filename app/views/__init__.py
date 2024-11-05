# app/views/__init__.py

from app.views.accounts import bp as accounts_bp
from app.views.transactions import bp as transactions_bp
from app.views.auth import bp as auth_bp

__all__ = ['accounts_bp', 'transactions_bp', 'auth_bp']
