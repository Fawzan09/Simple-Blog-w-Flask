"""
Review Forms for Flask Blog
"""
try:
    from flask_wtf import FlaskForm
    from wtforms import TextAreaField, SelectField, SubmitField
    from wtforms.validators import DataRequired, Length, NumberRange
except ImportError:
    from flaskblog.mock_extensions import FlaskForm, TextAreaField, SelectField, SubmitField
    from flaskblog.mock_extensions import DataRequired, Length
    NumberRange = DataRequired

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', 
                        choices=[('5', '5 Stars - Excellent'), 
                                ('4', '4 Stars - Very Good'), 
                                ('3', '3 Stars - Good'), 
                                ('2', '2 Stars - Fair'), 
                                ('1', '1 Star - Poor')],
                        validators=[DataRequired()],
                        coerce=int)
    comment = TextAreaField('Review Comment', 
                          validators=[Length(min=10, max=500)],
                          render_kw={"placeholder": "Share your thoughts about this post..."})
    submit = SubmitField('Submit Review')