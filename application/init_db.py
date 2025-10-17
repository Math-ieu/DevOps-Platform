from models import db, Product
import logging

logger = logging.getLogger(__name__)

def init_sample_data():
    """Initialiser des données d'exemple si la base est vide"""
    try:
        if Product.query.count() == 0:
            sample_products = [
                Product(name="Laptop Pro 15\"", description="Ordinateur portable haute performance avec processeur dernière génération", 
                       price=1299.99, stock=15, category="Ordinateurs"),
                Product(name="Smartphone X", description="Smartphone 5G avec écran OLED et triple caméra", 
                       price=799.99, stock=25, category="Smartphones"),
                Product(name="Écouteurs Sans Fil", description="Écouteurs Bluetooth avec réduction de bruit active", 
                       price=199.99, stock=50, category="Audio"),
                Product(name="Montre Connectée", description="Montre intelligente avec suivi fitness et notifications", 
                       price=299.99, stock=30, category="Wearables"),
                Product(name="Tablette Pro", description="Tablette 11 pouces parfaite pour le travail et le divertissement", 
                       price=649.99, stock=20, category="Tablettes"),
                Product(name="Clavier Mécanique RGB", description="Clavier gaming avec switches mécaniques et éclairage RGB", 
                       price=129.99, stock=40, category="Accessoires"),
                Product(name="Souris Gaming", description="Souris ergonomique haute précision pour gamers", 
                       price=79.99, stock=60, category="Accessoires"),
                Product(name="Webcam HD", description="Webcam 1080p avec microphone intégré pour visioconférences", 
                       price=89.99, stock=35, category="Accessoires"),
            ]
            
            for product in sample_products:
                db.session.add(product)
            
            db.session.commit()
            logger.info("Sample data initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing sample data: {str(e)}")
        db.session.rollback()