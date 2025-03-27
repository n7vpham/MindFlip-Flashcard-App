from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

main_bp = Blueprint('main', __name__)

# Using flask blueprints. This route should in theory capture all the default routes. 
# Ex) 127.0.0.1:500/ Would just point to templates/index.html (I set that as the default in the route)
# If a user went to 127.0.0.1:500/dummy they would be rendered the "dummy.html" file we have in the templates folder
# and it would work like that for all
@main_bp.route('/', defaults={'page': 'index'})
@main_bp.route('/<page>')
def show(page):
    try:
        return render_template(f'{page}.html')
    except TemplateNotFound:
        abort(404)

