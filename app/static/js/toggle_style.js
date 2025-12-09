window.addEventListener("load", function () {
    console.log("toggle_style.js loaded");

    const btn = document.getElementById("toggle-style");
    console.log("Button found:", btn);

    if (btn) {
        btn.onclick = function () {
            console.log("Button clicked → switching style");
            window.location.href = "/toggle-style";
        };
    }
});
