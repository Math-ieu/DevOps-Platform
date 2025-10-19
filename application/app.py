from flask import Flask
from config import Config
from models import db
from routes import register_routes
from metriques import http_requests,request_duration
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        from init_db import init_sample_data
        init_sample_data()
    
    register_routes(app)
    
    @app.before_request
    def before_request():
        from flask import request
        from datetime import datetime
        request.start_time = datetime.now()
    
    @app.after_request
    def after_request(response):
        from flask import request
        from datetime import datetime
        
        if hasattr(request, 'start_time'):
            duration = (datetime.now() - request.start_time).total_seconds()
            request_duration.labels(endpoint=request.endpoint or 'unknown').observe(duration)
        
        http_requests.labels(
            method=request.method,
            endpoint=request.endpoint or 'unknown',
            status=response.status_code
        ).inc()
        
        return response
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)