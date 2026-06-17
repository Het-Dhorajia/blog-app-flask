console.log("JS Connected");

let deleteBtns = document.querySelectorAll(".delete-btn");

console.log(deleteBtns);

deleteBtns.forEach(function(btn) {

    btn.addEventListener("click", function(event) {

        event.preventDefault();

        let ask = confirm("Are you sure you want to delete this post?");

        if (ask) {
            window.location.href = btn.href;
        }

    });

});