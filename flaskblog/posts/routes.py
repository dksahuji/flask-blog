from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, Comment
from flaskblog.posts.forms import PostForm
from flaskblog.comments.forms import CommentForm
import markdown as markdown2
import bleach
posts = Blueprint('posts', __name__)

markdown_extensions = ['codehilite', 'fenced_code', 'toc', 'meta',  'md_in_html', 'def_list', 'attr_list']

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        content_original = form.content.data
        if form.type_select.data == 'markdown':
            content = markdown2.markdown(form.content.data, extensions=markdown_extensions)
        elif form.type_select.data == 'text':
            content = form.content.data
        form.content.data = content_original
        tags_life = 'life' in form.tags.data
        tags_inspiration = 'inspiration' in form.tags.data
        tags_philosophy = 'philosophy' in form.tags.data
        tags_personalfinance = 'personalfinance' in form.tags.data
        tags_ml = 'ml' in form.tags.data
        tags_quotes = 'quotes' in form.tags.data
        tags_technology = 'technology' in form.tags.data
        post = Post(title=form.title.data, content=content, author=current_user, content_original=content_original, type_select=form.type_select.data, tags_life=tags_life, tags_inspiration=tags_inspiration, tags_philosophy=tags_philosophy, tags_personalfinance=tags_personalfinance, tags_ml=tags_ml, tags_quotes=tags_quotes, tags_technology=tags_technology, tags=form.text_tags.data, abstract=markdown2.markdown(form.abstract.data, extensions=markdown_extensions))
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", 'success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")

'''
@posts.route("/post/<int:post_id>")
def post(post_id):
    html_file = 'post.html'
    #html_file = 'post_w_comments.html'
    post = Post.query.get_or_404(post_id)
    #comments = post.comments
    if form == None:
        return render_template(html_file, title=post.title, post=post)
    else:
        return render_template(html_file, title=post.title, post=post, form=form)
'''

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content_original = form.content.data
        if form.type_select.data == 'markdown':
            content = markdown2.markdown(form.content.data, extensions=markdown_extensions)
        elif form.type_select.data == 'text':
            content = form.content.data
        post.content = content    
        post.tags_life = 'life' in form.tags.data
        post.tags_inspiration = 'inspiration' in form.tags.data
        post.tags_philosophy = 'philosophy' in form.tags.data
        post.tags_personalfinance = 'personalfinance' in form.tags.data
        post.tags_ml = 'ml' in form.tags.data
        post.tags_quotes = 'quotes' in form.tags.data
        post.tags_technology = 'technology' in form.tags.data
        post.tags = form.text_tags.data
        post.abstract = markdown2.markdown(form.abstract.data, extensions=markdown_extensions)
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.abstract.data = post.abstract
        form.content.data = post.content_original
        form.type_select.data = post.type_select
        form.text_tags.data = post.tags
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")
    

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments
    if post.author != current_user:
        abort(403)
    #db.session.delete(comments)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

@posts.route("/post/<int:post_id>/add_comment", methods=["POST"])
@posts.route("/post/<int:post_id>", methods=["POST", "GET"])
def post(post_id):
    html_file = 'post.html'
    #html_file = 'post_w_comments.html'
    post = Post.query.get_or_404(post_id)
    tags_list = []
    if post.tags_life:
        tags_list = tags_list + ['life']
    if post.tags_philosophy:
        tags_list = tags_list + ['philosophy']
    if post.tags_inspiration:
        tags_list = tags_list + ['inspiration']
    if post.tags_personalfinance:
        tags_list = tags_list + ['personalfinance']
    if post.tags_ml:
        tags_list = tags_list + ['ml']
    if post.tags_quotes:
        tags_list = tags_list + ['quotes']
    if post.tags_technology:
        tags_list = tags_list + ['technology']
    if post.tags:
       tags_list = tags_list + [post.tags]
    comments = post.comments #Post.query.all()
    comments = sorted(comments, key=lambda x: x.date_posted, reverse=True)
    form = CommentForm()
    if form.validate_on_submit():
        if post.author == current_user:
            comment = Comment(email=post.author.email, content=form.content.data, username=post.author.username, post_id=post_id, user_id=post.user_id)
        else:
            comment = Comment(email=form.email.data, content=form.content.data, username=form.username.data, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been posted!", 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        if post.author == current_user:
            form.email.data = post.author.email
            form.username.data = post.author.username
        else:
            form.email.data = "email@domain.com"
            form.username.data = "Anonymous"
        form.content.data = "Write Comment Here!!"
    else:
        flash("Your comment had Validation Errors! Please post with proper email and non-empty username and email.", 'danger')
        return redirect(url_for('posts.post', post_id=post.id))
    return render_template(html_file, title=post.title, post=post, form=form, comments=comments, tags_list=tags_list)

