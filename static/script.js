window.onload = function () {
    // Fetch products from the backend
    axios.get('http://localhost:5000/products')
        .then(function (productsResponse) {
            // Handle success for products
            const products = productsResponse.data;
            console.log('Received products:', products); // Log received products to console

            // Process and display products
            displayProducts(products);
        })
        .catch(function (error) {
            // Handle error for products
            console.error('Error fetching products:', error);
        });

    // Fetch orders from the backend
    axios.get('http://localhost:5000/orders')
        .then(function (ordersResponse) {
            // Handle success for orders
            const orders = ordersResponse.data;
            console.log('Received orders:', orders); // Log received orders to console

            // Process and display orders
            displayOrders(orders);
        })
        .catch(function (error) {
            // Handle error for orders
            console.error('Error fetching orders:', error);
        });

};

function displayProducts(products) {
    const productList = document.getElementById('product-list');

    // Clear existing product list
    productList.innerHTML = '';

    // Display products
    products.forEach(function (product) {
        const li = document.createElement('li');
        li.textContent = `Item: ${product.name} - Price: ${product.price}`;
        productList.appendChild(li);
    });
}

function displayOrders(orders) {
    const orderList = document.getElementById('order-list');

    // Clear existing order list
    orderList.innerHTML = '';

    // Check if orders are available
    if (orders.length > 0) {
        // Display orders
        orders.forEach(function (order) {
            const li = document.createElement('li');
            li.textContent = `Order ID: ${order.id}, Product ID: ${order.product_id}, Quantity: ${order.quantity}`;
            orderList.appendChild(li);
        });
    } else {
        // Display message indicating no orders
        const li = document.createElement('li');
        li.textContent = 'No orders placed';
        orderList.appendChild(li);
    }
}
