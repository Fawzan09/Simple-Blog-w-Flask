from flask import render_template, request, Blueprint
from flaskblog.models import Post
try:
    from flask_login import current_user
except ImportError:
    from flaskblog.mock_extensions import current_user
from sqlalchemy import or_

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page=request.args.get('page',1,type=int)
    search = request.args.get('search', '', type=str)
    
    if search:
        posts = Post.query.filter(
            or_(Post.title.contains(search),
                Post.content.contains(search))
        ).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    
    return render_template("home.html", posts=posts, current_user=current_user, search=search)

@main.route("/about")
def about():
    return render_template("about.html",title="About")

@main.route("/search")
def search():
    query = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    
    if query:
        posts = Post.query.filter(
            or_(Post.title.contains(query),
                Post.content.contains(query))
        ).order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    else:
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=10)
    
    return render_template("search.html", posts=posts, query=query, title="Search Results")


