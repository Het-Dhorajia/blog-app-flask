let dark = document.getElementById("switchCheckDefault");


// apply saved theme on every page load
let savedTheme = localStorage.getItem("theme");

if (savedTheme === "dark") {

    document.body.classList.add("dark-mode");

    if (dark) {
        dark.checked = true;
    }

}


// dark mode switch (only exists on settings page)
if (dark) {

    dark.addEventListener("change", function () {

        if (dark.checked) {

            document.body.classList.add("dark-mode");

            localStorage.setItem("theme", "dark");

        } else {

            document.body.classList.remove("dark-mode");

            localStorage.setItem("theme", "light");

        }

    });

}