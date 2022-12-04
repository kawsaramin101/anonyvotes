const pollStatus = document.querySelector('#vote_status');
const pollDetails = document.querySelector('#poll_details');


// From end code
//  {% if poll.is_open %} onclick="vote(event, '{{option.secondary_id}}')" {% endif %}


function vote(event, optionSecondaryID) {
    event.preventDefault();
    const clearLoading = showLoading(pollStatus);
        
    axios.post(window.location.pathname, {
        option_secondary_id: optionSecondaryID
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function(response) {
        clearLoading();
        
        const parser = new DOMParser();
        const parsedDocument = parser.parseFromString(response.data, "text/html");

        pollDetails.replaceChild(parsedDocument, pollDetails.firstChild);
        pollStatus.innerText = "Voted. Click to change vote.";
    }).catch(function(error) {
        clearLoading();
        if (error.response) {
            if (error.response.status>=500) {
                optionStatus.innerText = "Server error occurred.";
            } else {
            optionStatus.innerText = error.response.data.message;
            }
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