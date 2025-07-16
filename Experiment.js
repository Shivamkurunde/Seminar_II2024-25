// Remove sidebar cart code and only show a single alert when adding to cart

let alertActive = false;
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".add-to-cart-icon").forEach(button => {
        button.addEventListener("click", function(e) {
            e.preventDefault();
            if (alertActive) return;
            alertActive = true;
            // Get food_item_id and food_name from data attributes on the button
            const food_item_id = this.getAttribute("data-food-item-id");
            const food_name = this.getAttribute("data-food-name") || "Item";
            if (!food_item_id) {
                alert("Food item ID not found!");
                alertActive = false;
                return;
            }
            fetch("/api/cart/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ food_item_id, quantity: 1 })
            })
            .then(res => res.json())
            .then(data => {
                if (data.message) {
                    alert(food_name + " added to cart!");
                } else {
                    alert("Error adding item to cart: " + (data.error || "Unknown error"));
                }
                alertActive = false;
            })
            .catch(() => {
                alert("Error adding to cart");
                alertActive = false;
            });
        });
    });
});