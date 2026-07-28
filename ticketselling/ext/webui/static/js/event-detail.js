document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("ticketForm");

    const quantityInputs =
        document.querySelectorAll(".ticket-quantity");

    const ticketCount =
        document.getElementById("ticketCount");

    const subtotalElement =
        document.getElementById("subtotal");

    const ticketError =
        document.getElementById("ticketError");


    function formatMoney(value) {
        return new Intl.NumberFormat("vi-VN").format(value) + "đ";
    }


    function updateTotal() {
        let totalQuantity = 0;
        let subtotal = 0;

        quantityInputs.forEach(function (input) {
            const quantity = Number(input.value);
            const price = Number(input.dataset.price);

            totalQuantity += quantity;
            subtotal += quantity * price;
        });

        ticketCount.textContent =
            "Tạm tính (" + totalQuantity + " vé)";

        subtotalElement.textContent =
            formatMoney(subtotal);

        if (totalQuantity > 0) {
            ticketError.classList.add("d-none");
        }
    }


    document
        .querySelectorAll(".plus, .minus")
        .forEach(function (button) {
            button.addEventListener("click", function () {
                const input = document.getElementById(
                    button.dataset.target
                );

                let quantity = Number(input.value);
                const maximum = Number(input.max);

                if (
                    button.classList.contains("plus") &&
                    quantity < maximum
                ) {
                    quantity += 1;
                }

                if (
                    button.classList.contains("minus") &&
                    quantity > 0
                ) {
                    quantity -= 1;
                }

                input.value = quantity;
                updateTotal();
            });
        });


    form.addEventListener("submit", function (event) {
        let totalQuantity = 0;

        quantityInputs.forEach(function (input) {
            totalQuantity += Number(input.value);
        });

        if (totalQuantity === 0) {
            event.preventDefault();
            ticketError.classList.remove("d-none");
        }
    });


    updateTotal();
});