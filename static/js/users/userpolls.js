function closePoll(element, url) {
    const isConfirmed = confirm("You can't open the poll again if you close it. Are you sure you want to close this poll?")
    if (isConfirmed) {
        const closePollStatus = document.querySelector("#close-poll-status");
        element.outerHTML = "Loading..";

        axios.post(url, {},
            {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).then(function(response) {
                closePollStatus.innerHTML = response.data;
            }).catch(function(error) {
                if (error.response) {
                    if (error.response.status >= 500) {
                        closePollStatus.innerHTML = "Server error occurred.";
                    } else {
                        closePollStatus.innerHTML = error.response.data.message;
                    }
                    return;
                }
                closePollStatus.innerText = "Some error occurred. Try again later.";
            });
    } else {
        return
    }
}