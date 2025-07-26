"""
Review Routes for Flask Blog
"""
from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
try:
    from flask_login import current_user, login_required
except ImportError:
    from flaskblog.mock_extensions import current_user, login_required
from flaskblog import db
from flaskblog.models import Review, Post
from flaskblog.reviews.forms import ReviewForm

reviews = Blueprint('reviews', __name__)

@reviews.route("/post/<int:post_id>/review", methods=['GET', 'POST'])
@login_required
def add_review(post_id):
    """Add a review to a post"""
    post = Post.query.get_or_404(post_id)
    
    # Check if user already reviewed this post
    existing_review = Review.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing_review:
        flash('You have already reviewed this post. You can edit your existing review.', 'info')
        return redirect(url_for('posts.post', post_id=post_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            rating=form.rating.data,
            comment=form.comment.data,
            reviewer=current_user,
            post=post
        )
        db.session.add(review)
        db.session.commit()
        flash('Your review has been added successfully!', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    
    return render_template('reviews/review_form.html', 
                         title='Add Review', 
                         form=form, 
                         post=post,
                         legend='Add Review')

@reviews.route("/review/<int:review_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    """Edit an existing review"""
    review = Review.query.get_or_404(review_id)
    
    # Check if current user is the reviewer
    if review.reviewer != current_user:
        flash('You can only edit your own reviews.', 'error')
        return redirect(url_for('posts.post', post_id=review.post_id))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review.rating = form.rating.data
        review.comment = form.comment.data
        db.session.commit()
        flash('Your review has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=review.post_id))
    elif request.method == 'GET':
        form.rating.data = str(review.rating)
        form.comment.data = review.comment
    
    return render_template('reviews/review_form.html', 
                         title='Edit Review', 
                         form=form, 
                         post=review.post,
                         legend='Edit Review')

@reviews.route("/review/<int:review_id>/delete", methods=['POST'])
@login_required
def delete_review(review_id):
    """Delete a review"""
    review = Review.query.get_or_404(review_id)
    
    # Check if current user is the reviewer or post author
    if review.reviewer != current_user and review.post.author != current_user:
        flash('You can only delete your own reviews.', 'error')
        return redirect(url_for('posts.post', post_id=review.post_id))
    
    post_id = review.post_id
    db.session.delete(review)
    db.session.commit()
    flash('Review has been deleted.', 'success')
    return redirect(url_for('posts.post', post_id=post_id))

@reviews.route("/review/<int:review_id>/like", methods=['POST'])
@login_required
def like_review(review_id):
    """Like a review (AJAX endpoint)"""
    review = Review.query.get_or_404(review_id)
    review.likes += 1
    db.session.commit()
    
    return jsonify({
        'success': True,
        'likes': review.likes,
        'dislikes': review.dislikes
    })

@reviews.route("/review/<int:review_id>/dislike", methods=['POST'])
@login_required
def dislike_review(review_id):
    """Dislike a review (AJAX endpoint)"""
    review = Review.query.get_or_404(review_id)
    review.dislikes += 1
    db.session.commit()
    
    return jsonify({
        'success': True,
        'likes': review.likes,
        'dislikes': review.dislikes
    })