from models import db, Product, Order, OrderItem
from metriques import product_views, cart_operations, order_operations
import logging

logger = logging.getLogger(__name__)

class ProductService:
    @staticmethod
    def get_all_products(category=None):
        try:
            query = Product.query
            if category:
                query = query.filter_by(category=category)
            products = query.all()
            return products
        except Exception as e:
            logger.error(f"Error fetching products: {str(e)}")
            return []
    
    @staticmethod
    def get_product_by_id(product_id):
       
        try:
            product = Product.query.get(product_id)
            if product:
                product_views.inc()
            return product
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {str(e)}")
            return None
    
    @staticmethod
    def create_product(name, description, price, stock, category, image_url=None):
        try:
            product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category=category,
                image_url=image_url
            )
            db.session.add(product)
            db.session.commit()
            logger.info(f"Product created: {name}")
            return product
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating product: {str(e)}")
            return None
    
    @staticmethod
    def get_categories():
        try:
            categories = db.session.query(Product.category).distinct().all()
            return [c[0] for c in categories if c[0]]
        except Exception as e:
            logger.error(f"Error fetching categories: {str(e)}")
            return []


class OrderService:
    @staticmethod
    def create_order(customer_name, customer_email, items):
        
        try:
            total_amount = 0
            order_items = []
            
            for item in items:
                product = Product.query.get(item['product_id'])
                if not product:
                    return None, f"Produit {item['product_id']} introuvable"
                
                if product.stock < item['quantity']:
                    return None, f"Stock insuffisant pour {product.name}"
                
                total_amount += product.price * item['quantity']
                order_items.append({
                    'product': product,
                    'quantity': item['quantity'],
                    'price': product.price
                })
            
            order = Order(
                customer_name=customer_name,
                customer_email=customer_email,
                total_amount=total_amount,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()
            
            for item_data in order_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data['product'].id,
                    quantity=item_data['quantity'],
                    price=item_data['price']
                )
                db.session.add(order_item)
                item_data['product'].stock -= item_data['quantity']
            
            db.session.commit()
            cart_operations.labels(operation='checkout').inc()
            order_operations.labels(status='created').inc()
            logger.info(f"Order created: {order.id}")
            
            return order, None
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating order: {str(e)}")
            return None, str(e)
    
    @staticmethod
    def get_order_by_id(order_id):
        try:
            return Order.query.get(order_id)
        except Exception as e:
            logger.error(f"Error fetching order {order_id}: {str(e)}")
            return None
    
    @staticmethod
    def get_all_orders():
        try:
            orders = Order.query.order_by(Order.created_at.desc()).all()
            return orders
        except Exception as e:
            logger.error(f"Error fetching orders: {str(e)}")
            return []
    
    @staticmethod
    def update_order_status(order_id, status):
        
        valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
        if status not in valid_statuses:
            return False
        
        try:
            order = Order.query.get(order_id)
            if not order:
                return False
            
            order.status = status
            db.session.commit()
            order_operations.labels(status=status).inc()
            logger.info(f"Order {order_id} status updated to {status}")
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error updating order status: {str(e)}")
            return False