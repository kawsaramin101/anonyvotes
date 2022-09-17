const pollStatus = document.querySelector('#vote_status');
const pollDetails = document.querySelector('#poll_details');

function vote(event, optionSecondaryID) {
    event.preventDefault();
    pollStatus.innerText = "Loading..";

    axios.post(window.location.pathname, {
        option_secondary_id: optionSecondaryID
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function(response) {
        pollDetails.innerHTML = response.data;
        pollStatus.innerText = "Voted. Click to change vote.";
    }).catch(function(error) {
        if (error.response) {
            optionStatus.innerText = error.response.data.message;
            return;
        }
        optionStatus.innerText = "Some error occurred. Try again later.";
    });
}

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