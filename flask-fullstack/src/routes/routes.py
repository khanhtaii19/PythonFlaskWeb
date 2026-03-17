from flask import Blueprint
from src.controllers.auth_controller import register, login, get_me, get_users
from src.controllers.product_controller import (
    get_products, get_product_by_id, create_product, update_product, delete_product
)
from src.controllers.order_controller import get_orders, create_order, update_order_status
from src.controllers.blog_controller import get_blog_posts, get_blog_post_by_id, create_blog_post
from src.controllers.misc_controller import get_categories, get_coupons

# ── Auth ──────────────────────────────────────────────────────────────────────
auth_bp = Blueprint('auth', __name__)

auth_bp.add_url_rule('/register', view_func=register,  methods=['POST'])
auth_bp.add_url_rule('/login',    view_func=login,     methods=['POST'])
auth_bp.add_url_rule('/me',       view_func=get_me,    methods=['GET'])
auth_bp.add_url_rule('/users',    view_func=get_users, methods=['GET'])

# ── Products ──────────────────────────────────────────────────────────────────
product_bp = Blueprint('products', __name__)

product_bp.add_url_rule('/',      view_func=get_products,      methods=['GET'])
product_bp.add_url_rule('/<product_id>', view_func=get_product_by_id, methods=['GET'])
product_bp.add_url_rule('/',      view_func=create_product,    methods=['POST'])
product_bp.add_url_rule('/<product_id>', view_func=update_product,    methods=['PUT'])
product_bp.add_url_rule('/<product_id>', view_func=delete_product,    methods=['DELETE'])

# ── Orders ────────────────────────────────────────────────────────────────────
order_bp = Blueprint('orders', __name__)

order_bp.add_url_rule('/',             view_func=get_orders,    methods=['GET'])
order_bp.add_url_rule('/',             view_func=create_order,  methods=['POST'])
order_bp.add_url_rule('/<order_id>/status', view_func=update_order_status, methods=['PUT'])

# ── Blog ──────────────────────────────────────────────────────────────────────
blog_bp = Blueprint('blog', __name__)

blog_bp.add_url_rule('/',         view_func=get_blog_posts,      methods=['GET'])
blog_bp.add_url_rule('/<post_id>', view_func=get_blog_post_by_id, methods=['GET'])
blog_bp.add_url_rule('/',         view_func=create_blog_post,    methods=['POST'])

# ── Categories & Coupons ──────────────────────────────────────────────────────
category_bp = Blueprint('categories', __name__)
category_bp.add_url_rule('/', view_func=get_categories, methods=['GET'])

coupon_bp = Blueprint('coupons', __name__)
coupon_bp.add_url_rule('/', view_func=get_coupons, methods=['GET'])

def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/products")
    app.register_blueprint(order_bp, url_prefix="/api/orders")
    app.register_blueprint(blog_bp, url_prefix="/api/blog")
    app.register_blueprint(category_bp, url_prefix="/api/categories")
    app.register_blueprint(coupon_bp, url_prefix="/api/coupons")