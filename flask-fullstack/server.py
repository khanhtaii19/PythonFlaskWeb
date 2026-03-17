from flask import Flask, render_template, redirect, url_for
from flask_cors import CORS
from src.config.database import init_db
from src.routes.routes import register_routes

app = Flask(__name__)
CORS(app)

# ── Init DB ─────────────────────────────────────────────────────────────────
with app.app_context():
    init_db()

# ── Register all API routes ──────────────────────────────────────────────────
register_routes(app)

# ═══════════════════════════════════════════════════════════════════════════════
#  Frontend page routes
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/products')
def products():
    return render_template('pages/products.html')

@app.route('/products/<int:product_id>')
def product_detail(product_id):
    return render_template('pages/product_detail.html')

@app.route('/blog')
def blog():
    return render_template('pages/blog.html')

@app.route('/blog/<int:post_id>')
def blog_detail(post_id):
    return render_template('pages/blog_detail.html')

@app.route('/login')
def login():
    return render_template('pages/login.html')

@app.route('/register')
def register():
    return render_template('pages/register.html')

@app.route('/checkout')
def checkout():
    return render_template('pages/checkout.html')

@app.route('/orders')
def orders():
    return render_template('pages/orders.html')

@app.route('/profile')
def profile():
    return render_template('pages/profile.html')

@app.route('/admin')
def admin():
    return render_template('pages/admin.html')

# ── Health check ─────────────────────────────────────────────────────────────
@app.route('/health')
def health():
    return {'status': 'ok', 'mode': 'fullstack'}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
