document.addEventListener("DOMContentLoaded", function () {

    const btnNext1 = document.getElementById("btnNext1");
    const btnBack1 = document.getElementById("btnBack1");

    const step1 = document.getElementById("step1");
    const step2 = document.getElementById("step2");

    const indicator1 = document.getElementById("indicator1");
    const indicator2 = document.getElementById("indicator2");

    if (btnNext1) {
        btnNext1.addEventListener("click", function () {

            const name = document.getElementById("customer_name_input").value.trim();
            const email = document.getElementById("email_input").value.trim();
            const phone = document.getElementById("phone_input").value.trim();
            const identity = document.getElementById("identity_input").value.trim();

            if (!name || !email || !phone) {
                alert("Vui lòng nhập đầy đủ Họ và tên, Email và Số điện thoại.");
                return;
            }

            document.getElementById("customer_name").value = name;
            document.getElementById("email").value = email;
            document.getElementById("phone").value = phone;
            document.getElementById("identity").value = identity;

            const delivery = document.querySelector(
                'input[name="delivery"]:checked'
            );

            if (delivery) {
                document.getElementById("delivery").value = delivery.value;
            }

            step1.style.display = "none";

            step2.style.display = "block";

            indicator1.classList.remove("active");
            indicator2.classList.add("active");
        });
    }

    if (btnBack1) {
        btnBack1.addEventListener("click", function () {

            step2.style.display = "none";
            step1.style.display = "block";

            indicator2.classList.remove("active");
            indicator1.classList.add("active");
        });
    }

});