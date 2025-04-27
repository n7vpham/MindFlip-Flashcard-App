from flask import Blueprint, render_template, session, redirect, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def show_index():
    if session.get('user_id'):
        return redirect(url_for('flashcards.get_all_users_sets_home'))
    return render_template('index.html')

@main_bp.route('/index.html')
def show_index_html():
    return redirect(url_for('main.show_index'))