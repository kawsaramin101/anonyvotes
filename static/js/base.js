function showLoading(element) {
    element.innerHTML = "Loading";
    dots = document.createElement("span");
    dots.innerHTML = ".";
    element.appendChild(dots);
    const intervalID = setInterval(function() {
        if (dots.innerHTML.length > 3) {
            dots.innerHTML = "";
            element.appendChild(dots);
        } else {
            dots.innerHTML += ".";
            element.appendChild(dots);
        }
    }, 200);
    function clearAll() {
        clearInterval(intervalID);
        element.innerHTML = "";
    }
    return clearAll
}