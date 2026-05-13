// =========================
// CSRF TOKEN
// =========================

function getCSRFToken() {

    return document.querySelector(
        '[name=csrfmiddlewaretoken]'
    ).value;

}



// =========================
// CUSTOM POPUP
// =========================

function showPopup(message, callback = null) {

    const popup =
        document.getElementById('custom-popup');

    const popupMessage =
        document.getElementById(
            'custom-popup-message'
        );

    const popupButton =
        document.getElementById(
            'custom-popup-ok'
        );

    popupMessage.innerText = message;

    popup.style.display = 'flex';

    popupButton.onclick = function () {

        popup.style.display = 'none';

        if (callback) {
            callback();
        }

    };

}



// =========================
// ADD TO CART
// =========================
// =========================
// ADD TO CART
// =========================

function addToCart(foodId) {

    fetch(`/add-to-cart/${foodId}/`, {

        method: 'POST',

        headers: {

            'Content-Type': 'application/json',

            'X-CSRFToken': getCSRFToken()

        }

    })

    .then(response => response.json())

    .then(data => {

        if (data.success) {

            showPopup(
                "Item added to cart successfully!"
            );

        } else {

            showPopup(
                data.message ||
                "Failed to add item."
            );

        }

    })

    .catch(error => {

        console.error(error);

        showPopup(
            "Something went wrong."
        );

    });

}



// =========================
// CHANGE QUANTITY
// =========================

function changeQuantity(cartId, change) {

    const quantityInput =
        document.getElementById(
            `qty-${cartId}`
        );

    let currentQuantity =
        parseInt(quantityInput.value);

    currentQuantity += change;

    if (currentQuantity < 1) {
        currentQuantity = 1;
    }

    quantityInput.value = currentQuantity;

    updateQuantity(
        cartId,
        currentQuantity
    );

}



// =========================
// DELETE CART ITEM
// =========================

// =========================
// DELETE CART ITEM
// =========================

function deleteCartItem(cartId) {

    const popup =
        document.getElementById(
            'custom-popup'
        );

    const message =
        document.getElementById(
            'custom-popup-message'
        );

    const okButton =
        document.getElementById(
            'custom-popup-ok'
        );



    popup.style.display = 'flex';

    message.innerText =
        'Remove item from cart?';



    okButton.onclick = function () {

        fetch(`/delete-cart-item/${cartId}/`, {

            method: 'POST',

            headers: {

                'X-CSRFToken':
                    getCSRFToken(),

                'Content-Type':
                    'application/json'

            }

        })

        .then(response => response.json())

        .then(data => {

            if (data.success) {

                window.location.reload();

            } else {

                alert(
                    'Failed to remove item.'
                );

            }

        })

        .catch(error => {

            console.error(error);

            alert(
                'Something went wrong.'
            );

        });

    };

}


// =========================
// DELETE ORDER
// =========================

function deleteOrder(orderId) {

    showPopup(
        "Delete this order history?",
        function () {

            fetch(
                `/delete-order/${orderId}/`,
                {

                    method: 'POST',

                    headers: {

                        'X-CSRFToken':
                            getCSRFToken()

                    }

                }
            )

            .then(response => response.json())

            .then(data => {

                showPopup(
                    data.message ||
                    "Order deleted!",
                    function () {

                        location.reload();

                    }
                );

            })

            .catch(error => {

                console.error(error);

                showPopup(
                    "Failed to delete order."
                );

            });

        }
    );

}



// =========================
// DELETE ADDRESS
// =========================

function deleteAddress(addressId) {

    showPopup(
        "Delete this address?",
        function () {

            fetch(
                `/delete-address/${addressId}/`,
                {

                    method: 'POST',

                    headers: {

                        'X-CSRFToken':
                            getCSRFToken()

                    }

                }
            )

            .then(response => response.json())

            .then(data => {

                showPopup(
                    data.message,
                    function () {

                        if (data.success) {

                            location.reload();

                        }

                    }
                );

            })

            .catch(error => {

                console.error(error);

                showPopup(
                    "Failed to delete address."
                );

            });

        }
    );

}



// =========================
// ONLINE PAYMENT
// =========================

function startStripeCheckout() {

    fetch('/create-checkout-session/', {

        method: 'POST',

        headers: {

            'X-CSRFToken':
                getCSRFToken(),

            'Content-Type':
                'application/json'

        }

    })

    .then(response => response.json())

    .then(data => {

        if (data.session_url) {

            window.location.href =
                data.session_url;

        } else {

            showPopup(
                data.message ||
                "Unable to start payment."
            );

        }

    })

    .catch(error => {

        console.error(error);

        showPopup(
            "Payment failed."
        );

    });

}



// =========================
// LOADING EFFECT
// =========================

window.addEventListener('load', function () {

    document.body.classList.add(
        'loaded'
    );

});



// =========================
// SCROLL NAVBAR EFFECT
// =========================

window.addEventListener('scroll', function () {

    const navbar =
        document.querySelector('.navbar');

    if (window.scrollY > 50) {

        navbar.classList.add('scrolled');

    } else {

        navbar.classList.remove('scrolled');

    }

});



// =========================
// SEARCH ANIMATION
// =========================

const searchInput =
    document.querySelector('.search-box input');

if (searchInput) {

    searchInput.addEventListener(
        'focus',
        function () {

            this.parentElement.classList.add(
                'active-search'
            );

        }
    );



    searchInput.addEventListener(
        'blur',
        function () {

            this.parentElement.classList.remove(
                'active-search'
            );

        }
    );

}

// =========================
// PLACE ORDER
// =========================

function submitOrder(paymentMethod) {

    fetch('/place-order/', {

        method: 'POST',

        headers: {

            'Content-Type': 'application/json',

            'X-CSRFToken': getCSRFToken()

        },

        body: JSON.stringify({

            payment_method: paymentMethod

        })

    })

    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`HTTP Error: ${response.status} - ${text}`);
            });
        }
        return response.json();
    })

    .then(data => {

        if (data.success) {

            showPopup(
                "Order placed successfully!",
                function () {

                    window.location.href =
                        data.redirect_url;

                }
            );

        } else {

            showPopup(
                data.message ||
                "Failed to place order."
            );

        }

    })

    .catch(error => {

        console.error("Order error:", error);

        showPopup(
            "Order error: " + (error.message || "Something went wrong")
        );

    });

}

