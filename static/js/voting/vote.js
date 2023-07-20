/* Listen when request starts and ends to show Loading and stop loading */
const pollStatus = document.querySelector('#vote_status');
const pollDetails = document.querySelector('#poll_details');

document.body.addEventListener('htmx:beforeRequest', function(evt) {
    const clearLoading = showLoading(pollStatus);
    document.body.addEventListener('htmx:beforeSwap', function(evt) {
        clearLoading();
    });
});

document.body.addEventListener('htmx:configRequest', function(evt) {
    evt.detail.headers['X-CSRFToken'] = csrftoken
});

/* Show error */
document.body.addEventListener("htmx:responseError", function(evt) {
    pollStatus.innerHTML = `Request failed.<br/>${evt.detail.xhr.responseText}<br/>${evt.detail.xhr.status}`;
});


/* Copy to clipboard codes */
const clickToCopy = document.querySelector("#click-to-copy");
const failedToCopy = document.querySelector("#failed-to-copy");
let clipboard = new ClipboardJS("#click-to-copy");
clipboard.on("success", function(e) {
    clickToCopy.innerText = "Copied";
});
clipboard.on("error", function(e) {
    failedToCopy.innerText = "Failed to copy. Please copy from the address bar.";
});