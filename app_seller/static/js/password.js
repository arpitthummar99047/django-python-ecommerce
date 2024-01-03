document.addEventListener("DOMContentLoaded", function () {
  var form = document.querySelector(".aside-content");

  form.addEventListener("submit", function (event) {
    var emailInput = document.getElementById("registerUserEmailInput");
    var passwordInput = document.getElementById("registerPasswordInput");
    var confirmPasswordInput = document.getElementById("confirmPasswordInput");
    var passwordError = document.getElementById("passwordError");
    var emailError = document.getElementById("emailError");

    // Email validation regex
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Validate email
    if (!emailRegex.test(emailInput.value)) {
      emailError.textContent = "Invalid email format";
      event.preventDefault(); // Prevent form submission
    } else {
      emailError.textContent = ""; // Clear the error message
    }

    // Validate password
    if (passwordInput.value !== confirmPasswordInput.value) {
      passwordError.textContent = "Passwords do not match";
      event.preventDefault(); // Prevent form submission
    } else {
      passwordError.textContent = ""; // Clear the error message
    }
  });
});
