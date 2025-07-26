"""
Mock implementations for Flask extensions when not available
"""

try:
    from flask_bcrypt import Bcrypt
except ImportError:
    class Bcrypt:
        def __init__(self):
            pass
        def init_app(self, app):
            pass
        def generate_password_hash(self, password):
            import hashlib
            return hashlib.sha256(password.encode()).hexdigest()
        def check_password_hash(self, hash, password):
            import hashlib
            return hash == hashlib.sha256(password.encode()).hexdigest()

try:
    from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
except ImportError:
    class LoginManager:
        def __init__(self):
            self.login_view = None
            self.login_message_category = None
        def init_app(self, app):
            pass
        def user_loader(self, func):
            return func
    
    class UserMixin:
        def is_authenticated(self):
            return True
        def is_active(self):
            return True
        def is_anonymous(self):
            return False
        def get_id(self):
            return str(self.id)
    
    def login_user(user, remember=False):
        pass
    
    def logout_user():
        pass
    
    def login_required(func):
        return func
    
    class MockUser:
        def is_authenticated(self):
            return False
        
        @property 
        def is_authenticated(self):
            return False
        
        def is_active(self):
            return False
        def is_anonymous(self):
            return True
        def get_id(self):
            return None
    
    current_user = MockUser()

try:
    from flask_mail import Mail
except ImportError:
    class Mail:
        def __init__(self):
            pass
        def init_app(self, app):
            pass

try:
    from flask_wtf import FlaskForm
    from wtforms import StringField, TextAreaField, PasswordField, SubmitField, BooleanField, SelectField
    from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
except ImportError:
    class FlaskForm:
        def __init__(self):
            pass
        def validate_on_submit(self):
            return False
        def hidden_tag(self):
            return ""
    
    class StringField:
        def __init__(self, *args, **kwargs):
            pass
    
    class TextAreaField:
        def __init__(self, *args, **kwargs):
            pass
    
    class PasswordField:
        def __init__(self, *args, **kwargs):
            pass
    
    class SubmitField:
        def __init__(self, *args, **kwargs):
            pass
    
    class BooleanField:
        def __init__(self, *args, **kwargs):
            pass
    
    class SelectField:
        def __init__(self, *args, **kwargs):
            pass
    
    class DataRequired:
        def __init__(self, *args, **kwargs):
            pass
    
    class Length:
        def __init__(self, *args, **kwargs):
            pass
    
    class Email:
        def __init__(self, *args, **kwargs):
            pass
    
    class EqualTo:
        def __init__(self, *args, **kwargs):
            pass
    
    class ValidationError(Exception):
        pass