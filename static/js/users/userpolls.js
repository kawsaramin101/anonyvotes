function closePoll(element, url) {
    const isConfirmed = confirm("You can't open the poll again if you close it. Are you sure you want to close this poll?")
    if (isConfirmed) {
        const closePollStatus = element.parentElement;
        const clearLoading = showLoading(closePollStatus);
        
        axios.post(url, {},
            {
                headers: {
                    'X-CSRFToken': csrftoken
                }
            }).then(function(response) {
                clearLoading()
                closePollStatus.innerHTML = response.data;
            }).catch(function(error) {
                clearLoading()
                if (error.response) {
                    if (error.response.status >= 500) {
                        closePollStatus.innerHTML = "Server error occurred.";
                    } else {
                        closePollStatus.innerHTML = error.response.data.message;
                    }
                    return;
                }
                closePollStatus.innerHTML = "Some error occurred. Try again later.";
            });
    } else {
        return
    }
}