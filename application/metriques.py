
from prometheus_client import Counter, Histogram

# Métriques Prometheus
http_requests = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
product_views = Counter('product_views_total', 'Total Product Views')
cart_operations = Counter('cart_operations_total', 'Cart Operations', ['operation'])
order_operations = Counter('order_operations_total', 'Order Operations', ['status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['endpoint'])