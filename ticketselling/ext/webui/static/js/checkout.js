// STEP ELEMENTS
console.log("checkout.js loaded");

const step1 = document.getElementById("step1");
const step2 = document.getElementById("step2");
const step3 = document.getElementById("step3");

// Delivery option
const deliveryOptions = document.querySelectorAll(".delivery-option");

deliveryOptions.forEach(option => {

    option.addEventListener("click", function () {

        deliveryOptions.forEach(item => {
            item.classList.remove("active");
            item.querySelector("input[type='radio']").checked = false;
        });

        this.classList.add("active");
        this.querySelector("input[type='radio']").checked = true;

    });

});

// PAYMENT METHOD

const paymentOptions = document.querySelectorAll(".payment-item");

// default chosing VNPAY
paymentOptions[0].classList.add("active");
paymentOptions[0].querySelector("input").checked = true;

paymentOptions.forEach(option => {

    option.addEventListener("click", function () {

        paymentOptions.forEach(item => {

            item.classList.remove("active");
            item.querySelector("input[type='radio']").checked = false;

        });

        this.classList.add("active");
        this.querySelector("input[type='radio']").checked = true;

    });

});


// BUTTONS

const btnNext1 = document.getElementById("btnNext1");
const btnNext2 = document.getElementById("btnNext2");

const btnBack1 = document.getElementById("btnBack1");
const btnBack2 = document.getElementById("btnBack2");

const indicator1 = document.getElementById("indicator1");
const indicator2 = document.getElementById("indicator2");
const indicator3 = document.getElementById("indicator3");

function showStep(step) {

    step1.style.display = "none";
    step2.style.display = "none";
    step3.style.display = "none";

    indicator1.classList.remove("active");
    indicator2.classList.remove("active");
    indicator3.classList.remove("active");

    if (step === 1) {

        step1.style.display = "block";
        indicator1.classList.add("active");

    }

    if (step === 2) {

        step2.style.display = "block";

        indicator1.classList.add("active");
        indicator2.classList.add("active");

    }

    if (step === 3) {

        step3.style.display = "block";

        indicator1.classList.add("active");
        indicator2.classList.add("active");
        indicator3.classList.add("active");

    }

}

btnNext1.addEventListener("click", function (e) {

    e.preventDefault();

    showStep(2);

});

btnNext2.addEventListener("click", function (e) {

    e.preventDefault();

    showStep(3);

});

btnBack1.addEventListener("click", function (e) {

    e.preventDefault();

    showStep(1);

});

btnBack2.addEventListener("click", function (e) {

    e.preventDefault();

    showStep(2);

});

showStep(1);