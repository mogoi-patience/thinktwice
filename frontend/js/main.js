const API = 'http://127.0.0.1:5000';

// Load products on homepage
async function loadProducts() {
  const grid = document.getElementById('products-grid');
  if (!grid) return;
  try {
    const res = await fetch(`${API}/api/products`);
    const data = await res.json();
    if (data.products.length === 0) {
      grid.innerHTML = '<p class="loading">No products yet. Check back soon!</p>';
      return;
    }
    grid.innerHTML = data.products.map(p => `
      <div class="product-card">
        ${p.image_url
          ? `<img src="${p.image_url}" alt="${p.name}" />`
          : `<div class="product-img-placeholder">👗</div>`}
        <div class="product-info">
          ${p.is_on_offer ? '<span class="product-badge">ON OFFER</span>' : ''}
          <div class="product-name">${p.name}</div>
          ${p.is_on_offer
            ? `<div class="product-price offer">KSh ${p.offer_price.toLocaleString()}</div>
               <div class="product-old-price">KSh ${p.price.toLocaleString()}</div>`
            : `<div class="product-price">KSh ${p.price.toLocaleString()}</div>`}
          ${p.stock_quantity <= 3 ? '<div class="low-stock">⚠️ Only a few left!</div>' : ''}
          <button class="add-to-cart" onclick="addToCart(${p.id}, '${p.name}', ${p.is_on_offer ? p.offer_price : p.price})">
            Add to Cart
          </button>
        </div>
      </div>
    `).join('');
  } catch (err) {
    grid.innerHTML = '<p class="loading">Could not load products.</p>';
  }
}

// Cart
function getCart() {
  return JSON.parse(localStorage.getItem('tt_cart') || '[]');
}
function saveCart(cart) {
  localStorage.setItem('tt_cart', JSON.stringify(cart));
  updateCartCount();
}
function updateCartCount() {
  const count = document.getElementById('cart-count');
  if (count) count.textContent = getCart().length;
}
function addToCart(id, name, price) {
  const cart = getCart();
  cart.push({ id, name, price });
  saveCart(cart);
  alert(`${name} added to cart!`);
}

// Subscribe
async function subscribe() {
  const email = document.getElementById('sub-email').value;
  const phone = document.getElementById('sub-phone').value;
  const msg = document.getElementById('sub-message');
  if (!email) { msg.textContent = 'Please enter your email.'; msg.style.color = 'red'; return; }
  try {
    const res = await fetch(`${API}/api/subscribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, phone })
    });
    const data = await res.json();
    msg.textContent = '✅ Subscribed! You will be notified of new stock and offers.';
    msg.style.color = 'green';
  } catch (err) {
    msg.textContent = 'Something went wrong. Try again.';
    msg.style.color = 'red';
  }
}

// Init
updateCartCount();
loadProducts();
