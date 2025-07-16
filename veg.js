document.addEventListener("DOMContentLoaded", () => {
    const cart = [];
    let cartVisible = false;

    // Create cart UI container
    const cartContainer = document.createElement("div");
    cartContainer.className = "border bg-white p-3 shadow";
    cartContainer.style.position = "fixed";
    cartContainer.style.top = "20px";
    cartContainer.style.right = "20px";
    cartContainer.style.width = "300px";
    cartContainer.style.zIndex = "1000";
    cartContainer.style.maxHeight = "80vh";
    cartContainer.style.overflowY = "auto";
    cartContainer.style.display = "none";

    cartContainer.innerHTML = `
        <div class="d-flex justify-content-between align-items-center mb-2">
            <h5>Your Cart</h5>
            <button id="close-cart" class="btn btn-sm btn-danger">X</button>
        </div>
        <div id="cart-items"></div>
        <hr />
        <p><strong>Total:</strong> <span id="cart-total">Rs. 0</span></p>
        <button class="btn btn-success w-100" id="buy-now">Buy Now</button>
    `;

    document.body.appendChild(cartContainer);

    const cartItemsContainer = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");

    function updateCartUI() {
        cartItemsContainer.innerHTML = '';
        let total = 0;

        cart.forEach(item => {
            const itemDiv = document.createElement("div");
            itemDiv.className = "border p-2 mb-2";
            itemDiv.innerHTML = `
                <div class="d-flex justify-content-between">
                    <div>
                        <strong>${item.name}</strong><br>
                        <small>${item.priceText}</small>
                    </div>
                    <div>
                        <button class="btn btn-sm btn-secondary minus">-</button>
                        <span class="mx-1">${item.quantity}</span>
                        <button class="btn btn-sm btn-secondary plus">+</button>
                        <button class="btn btn-sm btn-danger ml-2 remove">x</button>
                    </div>
                </div>
            `;

            itemDiv.querySelector(".plus").addEventListener("click", () => {
                item.quantity++;
                updateCartUI();
            });

            itemDiv.querySelector(".minus").addEventListener("click", () => {
                if (item.quantity > 1) {
                    item.quantity--;
                    updateCartUI();
                }
            });

            itemDiv.querySelector(".remove").addEventListener("click", () => {
                const index = cart.indexOf(item);
                if (index !== -1) {
                    cart.splice(index, 1);
                    updateCartUI();
                }
                if (cart.length === 0) {
                    cartContainer.style.display = "none";
                    cartVisible = false;
                }
            });

            cartItemsContainer.appendChild(itemDiv);
            total += item.price * item.quantity;
        });

        cartTotal.textContent = `Rs. ${total.toFixed(2)}`;
    }

    // Handle both the orange cart icon and any other add-to-cart buttons
    document.querySelectorAll(".add-to-cart-icon, .add-to-cart").forEach(button => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const card = button.closest(".menu-item-card");
            
            // If the button is inside a menu-item-card (for the orange icon)
            if (card) {
                const name = card.querySelector(".menu-card-title").textContent;
                const priceText = card.querySelector(".Dish-Price").textContent;
                const price = parseFloat(priceText.replace("Rs.", "").trim());

                const existingItem = cart.find(item => item.name === name);
                if (existingItem) {
                    alert("Item already in cart!");
                    return;
                }

                cart.push({
                    name,
                    priceText,
                    price,
                    quantity: 1
                });

                cartContainer.style.display = "block";
                cartVisible = true;
                updateCartUI();
            }
        });
    });

    document.getElementById("close-cart").addEventListener("click", () => {
        cartContainer.style.display = "none";
        cartVisible = false;
    });

    document.getElementById("buy-now").addEventListener("click", () => {
        if (cart.length === 0) {
            alert("Cart is empty.");
            return;
        }

        alert("Thank you for your purchase!");
        cart.length = 0;
        updateCartUI();
        cartContainer.style.display = "none";
        cartVisible = false;
    });

    // Add cart icon to all menu items that don't have it
    document.querySelectorAll(".menu-item-card").forEach(card => {
        if (!card.querySelector(".add-to-cart-icon")) {
            const orderNowLink = card.querySelector(".menu-item-link");
            if (orderNowLink) {
                const container = document.createElement("div");
                container.className = "d-flex justify-content-between align-items-center mt-2";
                
                // Clone the order now link to preserve its styling
                const clonedLink = orderNowLink.cloneNode(true);
                
                // Create the cart icon button
                const cartButton = document.createElement("button");
                cartButton.className = "btn add-to-cart-icon";
                cartButton.innerHTML = '<i class="fas fa-shopping-bag"></i>';
                
                container.appendChild(clonedLink);
                container.appendChild(cartButton);
                
                // Replace the old order now link with the new container
                orderNowLink.replaceWith(container);
                
                // Add event listener to the new button
                cartButton.addEventListener("click", (event) => {
                    event.preventDefault();
                    const name = card.querySelector(".menu-card-title").textContent;
                    const priceText = card.querySelector(".Dish-Price").textContent;
                    const price = parseFloat(priceText.replace("Rs.", "").trim());

                    const existingItem = cart.find(item => item.name === name);
                    if (existingItem) {
                        alert("Item already in cart!");
                        return;
                    }

                    cart.push({
                        name,
                        priceText,
                        price,
                        quantity: 1
                    });

                    cartContainer.style.display = "block";
                    cartVisible = true;
                    updateCartUI();
                });
            }
        }
    });
});