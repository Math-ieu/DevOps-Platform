// ==================== Cart Management ====================
let cart = [];

// Load cart from memory on page load
function loadCart() {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
    }
    updateCartUI();
}

// Save cart to memory
function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Add item to cart
function addToCart(productId, productName, productPrice) {
    const item = {
        id: productId,
        name: productName,
        price: parseFloat(productPrice)
    };
    
    cart.push(item);
    saveCart();
    updateCartUI();
    
    // Show notification
    showNotification('Produit ajouté au panier', 'success');
}

// Remove item from cart by index
function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    updateCartUI();
    showNotification('Produit retiré du panier', 'info');
}

// Clear entire cart
function clearCart() {
    cart = [];
    saveCart();
    updateCartUI();
}

// Update cart UI
function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    if (cartCount) {
        cartCount.textContent = cart.length;
    }
    
    if (cartItems) {
        if (cart.length === 0) {
            cartItems.innerHTML = `
                <div class="empty-state" style="padding: 2rem; text-align: center;">
                    <i class="fas fa-shopping-cart" style="font-size: 3rem; color: var(--text-secondary); margin-bottom: 1rem;"></i>
                    <p style="color: var(--text-secondary);">Votre panier est vide</p>
                </div>
            `;
        } else {
            // Group items by ID
            const groupedItems = {};
            cart.forEach((item, index) => {
                if (!groupedItems[item.id]) {
                    groupedItems[item.id] = {
                        ...item,
                        quantity: 0,
                        indices: []
                    };
                }
                groupedItems[item.id].quantity++;
                groupedItems[item.id].indices.push(index);
            });
            
            cartItems.innerHTML = Object.values(groupedItems).map(item => `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <h4>${item.name}</h4>
                        <span class="cart-item-price">${item.price.toFixed(2)} DH x ${item.quantity}</span>
                    </div>
                    <button class="remove-item" onclick="removeFromCart(${item.indices[0]})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `).join('');
        }
    }
    
    if (cartTotal) {
        const total = cart.reduce((sum, item) => sum + item.price, 0);
        cartTotal.textContent = `${total.toFixed(2)} DH`;
    }
}

// ==================== Cart Sidebar ====================
document.addEventListener('DOMContentLoaded', function() {
    loadCart();
    
    const cartBtn = document.getElementById('cartBtn');
    const cartSidebar = document.getElementById('cartSidebar');
    const cartOverlay = document.getElementById('cartOverlay');
    const closeCart = document.getElementById('closeCart');
    const checkoutBtn = document.getElementById('checkoutBtn');
    
    // Open cart
    if (cartBtn) {
        cartBtn.addEventListener('click', function(e) {
            e.preventDefault();
            cartSidebar.classList.add('active');
            cartOverlay.classList.add('active');
        });
    }
    
    // Close cart
    if (closeCart) {
        closeCart.addEventListener('click', function() {
            cartSidebar.classList.remove('active');
            cartOverlay.classList.remove('active');
        });
    }
    
    if (cartOverlay) {
        cartOverlay.addEventListener('click', function() {
            cartSidebar.classList.remove('active');
            cartOverlay.classList.remove('active');
        });
    }
    
    // Checkout button
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            if (cart.length === 0) {
                showNotification('Votre panier est vide', 'warning');
                return;
            }
            window.location.href = '/checkout';
        });
    }
    
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.id;
            const productName = this.dataset.name;
            const productPrice = this.dataset.price;
            
            addToCart(productId, productName, productPrice);
        });
    });
});

// Make addToCart available globally for product detail page
window.addToCart = addToCart;

// ==================== Notifications ====================
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? 'var(--success-color)' : type === 'warning' ? 'var(--warning-color)' : 'var(--primary-color)'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: var(--shadow-lg);
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ==================== Smooth Scroll ====================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// ==================== Active Link Highlighting ====================
function updateActiveLinks() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkPath = new URL(link.href).pathname;
        if (linkPath === currentPath) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

updateActiveLinks();

// ==================== Form Validation ====================
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = 'var(--danger-color)';
            } else {
                field.style.borderColor = 'var(--border-color)';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showNotification('Veuillez remplir tous les champs obligatoires', 'warning');
        }
    });
});

// ==================== Lazy Loading Images ====================
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                    img.removeAttribute('data-src');
                    observer.unobserve(img);
                }
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}

// ==================== Back to Top Button ====================
const backToTopButton = document.createElement('button');
backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopButton.className = 'back-to-top';
backToTopButton.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    background: var(--primary-color);
    color: white;
    border: none;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    display: none;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: var(--shadow-lg);
    z-index: 999;
    transition: all 0.3s ease;
`;

document.body.appendChild(backToTopButton);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        backToTopButton.style.display = 'flex';
    } else {
        backToTopButton.style.display = 'none';
    }
});

backToTopButton.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

backToTopButton.addEventListener('mouseenter', function() {
    this.style.transform = 'scale(1.1)';
});

backToTopButton.addEventListener('mouseleave', function() {
    this.style.transform = 'scale(1)';
});

// ==================== Loading State ====================
function showLoading() {
    const loader = document.createElement('div');
    loader.id = 'loader';
    loader.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    loader.innerHTML = `
        <div style="text-align: center;">
            <i class="fas fa-spinner fa-spin" style="font-size: 3rem; color: var(--primary-color);"></i>
            <p style="color: white; margin-top: 1rem;">Chargement...</p>
        </div>
    `;
    document.body.appendChild(loader);
}

function hideLoading() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.remove();
    }
}

// Export functions for use in other scripts
window.showLoading = showLoading;
window.hideLoading = hideLoading;
window.showNotification = showNotification;

// ==================== Console Welcome Message ====================
console.log('%cTechShop 🛍️', 'color: #2563eb; font-size: 2rem; font-weight: bold;');
console.log('%cBienvenue sur notre boutique en ligne!', 'color: #64748b; font-size: 1rem;');
console.log('%cVersion: 1.0.0', 'color: #94a3b8;');