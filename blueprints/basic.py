from flask import Blueprint

bp = Blueprint('basic', __name__, url_prefix='/')

@bp.route('/')
def index():
    return '主页面'