from flask import render_template, redirect, session
from flask_app import (
    app,
    db,
    User,
    Topic,
    Post,
    TopicForm,
    PostForm,
)

# Создание темы
@app.route('/create_topic', methods=['GET', 'POST'])
def create_topic():
    form = TopicForm()
    if form.validate_on_submit():
        topic = Topic(title=form.title.data)
        db.session.add(topic)
        db.session.commit()
        flash('Тема успешно создана!', 'success')
        return redirect(url_for('index'))
    return render_template('create_topic.html', form=form)

# Просмотр темы с постами
@app.route('/topic/<int:topic_id>')
def view_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    posts = Post.query.filter_by(topic_id=topic_id, post_id=None).all()  # Только основные посты (не ответы)
    return render_template('view_topic.html', topic=topic, posts=posts)

# Создание поста
@app.route('/topic/<int:topic_id>/create_post', methods=['GET', 'POST'])
def create_post(topic_id):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, user_id=1, topic_id=topic_id)  # user_id=1 для примера
        db.session.add(post)
        db.session.commit()
        flash('Пост успешно создан!', 'success')
        return redirect(url_for('view_topic', topic_id=topic_id))
    return render_template('create_thread.html', form=form)

# Ответ на пост
@app.route('/post/<int:post_id>/reply', methods=['GET', 'POST'])
def reply_post(post_id):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, user_id=1, topic_id=1, post_id=post_id)  # user_id=1 для примера
        db.session.add(post)
        db.session.commit()
        flash('Ответ успешно добавлен!', 'success')
        return redirect(url_for('view_topic', topic_id=1))  # topic_id=1 для примера
    return render_template('create_post.html', form=form)

# Редактирование темы
@app.route('/topic/<int:topic_id>/edit', methods=['GET', 'POST'])
def edit_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    form = TopicForm()
    if form.validate_on_submit():
        topic.title = form.title.data
        db.session.commit()
        flash('Тема успешно обновлена!', 'success')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.title.data = topic.title
    return render_template('edit_topic.html', form=form)

# Удаление темы
@app.route('/topic/<int:topic_id>/delete', methods=['POST'])
def delete_topic(topic_id):
    topic = Topic.query.get_or_404(topic_id)
    db.session.delete(topic)
    db.session.commit()
    flash('Тема успешно удалена!', 'success')
    return redirect(url_for('index'))

# Редактирование поста
@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.content = form.content.data
        db.session.commit()
        flash('Пост успешно обновлен!', 'success')
        return redirect(url_for('view_topic', topic_id=post.topic_id))
    elif request.method == 'GET':
        form.content.data = post.content
    return render_template('edit_post.html', form=form)

# Удаление поста
@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Пост успешно удален!', 'success')
    return redirect(url_for('view_topic', topic_id=post.topic_id))