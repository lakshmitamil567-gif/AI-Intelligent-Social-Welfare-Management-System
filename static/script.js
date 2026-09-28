// AI Intelligent Social Welfare Management System

document.addEventListener("DOMContentLoaded", function () {

    // Button click message
    const buttons = document.querySelectorAll("button");

    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            console.log("Button clicked: " + button.innerText);
        });
    });

    // Form validation
    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {

            const inputs = form.querySelectorAll("input, select");

            let valid = true;

            inputs.forEach(function (input) {
                if (input.hasAttribute("required") && input.value.trim() === "") {
                    valid = false;
                }
            });

            if (!valid) {
                event.preventDefault();
                alert("Please fill all required fields.");
            }
        });
    });

    // Welcome message
    console.log("AI Intelligent Social Welfare Management System loaded successfully.");
});