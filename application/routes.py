from flask import render_template, request, jsonify
from services import ProductService, OrderService
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from models import db
import logging

logger = logging.getLogger(__name__)

def register_routes(app):
     
    @app.route('/')
    def index():
        category = request.args.get('category')
        products = ProductService.get_all_products(category=category)
        categories = ProductService.get_categories()
        return render_template('index.html', 
                             products=products, 
                             categories=categories,
                             selected_category=category)
    
    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return "Produit introuvable", 404
        return render_template('product_detail.html', product=product)
    
    @app.route('/checkout')
    def checkout():
        return render_template('checkout.html')
    
    @app.route('/orders')
    def orders_list():
        orders = OrderService.get_all_orders()
        return render_template('orders.html', orders=orders)
    
    # API ENDPOINTS
    @app.route('/api/products', methods=['GET'])
    def api_get_products():
        category = request.args.get('category')
        products = ProductService.get_all_products(category=category)
        return jsonify({
            'success': True,
            'data': [p.to_dict() for p in products],
            'count': len(products)
        })
    
    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def api_get_product(product_id):
        product = ProductService.get_product_by_id(product_id)
        if not product:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
        return jsonify({'success': True, 'data': product.to_dict()})
    
    @app.route('/api/products', methods=['POST'])
    def api_create_product():
        data = request.get_json()
        required_fields = ['name', 'price', 'stock', 'category']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        product = ProductService.create_product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            stock=int(data['stock']),
            category=data['category'],
            image_url=data.get('image_url')
        )
        
        if not product:
            return jsonify({'success': False, 'error': 'Failed to create product'}), 500
        return jsonify({'success': True, 'data': product.to_dict()}), 201
    
    @app.route('/api/orders', methods=['POST'])
    def api_create_order():
        data = request.get_json()
        required_fields = ['customer_name', 'customer_email', 'items']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        order, error = OrderService.create_order(
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            items=data['items']
        )
        
        if error:
            return jsonify({'success': False, 'error': error}), 400
        return jsonify({'success': True, 'data': order.to_dict()}), 201
    
    @app.route('/api/orders/<int:order_id>', methods=['GET'])
    def api_get_order(order_id):
        order = OrderService.get_order_by_id(order_id)
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        return jsonify({'success': True, 'data': order.to_dict()})
    
    @app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
    def api_update_order_status(order_id):
        data = request.get_json()
        if 'status' not in data:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        success = OrderService.update_order_status(order_id, data['status'])
        if not success:
            return jsonify({'success': False, 'error': 'Failed to update order status'}), 400
        return jsonify({'success': True})
    
    # HEALTH & METRICS
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy', 'service': 'techshop-api'})
    
    @app.route('/ready')
    def ready():
        try:
            db.session.execute('SELECT 1')
            return jsonify({'status': 'ready', 'database': 'connected'})
        except Exception as e:
            logger.error(f"Readiness check failed: {str(e)}")
            return jsonify({'status': 'not_ready', 'error': str(e)}), 503
    
    @app.route('/metrics')
    def metrics():
        return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}
    
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': 'Not found'}), 404
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal error: {str(e)}")
        if request.path.startswith('/api/'):
            return jsonify({'success': False, 'error': 'Internal server error'}), 500
        return "Erreur interne du serveur", 500