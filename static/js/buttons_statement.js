var buttons = document.querySelectorAll(".animated-like-btn");

    buttons.forEach(function(button) {
        button.addEventListener("click", function() {
            lordIcon = button.querySelector(".lord-icon-inactive")
            lordIcon.src = "https://cdn.lordicon.com/ulnswmkk.json"
        });
    });