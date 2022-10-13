
const questionForm = document.querySelector("#question_form");
const questionBox = document.querySelector("#question_box");
const questionStatus = document.querySelector("#question_status");

questionForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const questionStatus = document.querySelector("#question_status");
    questionStatus.innerText = "Loading..";

    const questionBox = document.querySelector("#question_box");

    axios.post('/add_question/', {
        question: questionBox.value
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function (response) {
        questionStatus.innerText = "Question created.";
        sessionStorage.setItem("questionID", response.data.secondary_id);
    })
    .catch(function (error) {
        questionStatus.innerText = "Some error occurred. Try again later.";
    });
});

const addMoreOptionBtn = document.querySelector("#add_more_option");
const insertAdjacentHTMLBeforeMe = document.querySelector("#insertAdjacentHTMLBeforeMe");

sessionStorage.setItem("totalOptions", 2);

addMoreOptionBtn.addEventListener("click", function() {
    const optionNumber = parseInt(sessionStorage.getItem("totalOptions")) + 1;
    insertAdjacentHTMLBeforeMe.insertAdjacentHTML("beforebegin", `<label for="option${optionNumber}">Option${optionNumber}:</label><br><input type="text" name="option${optionNumber}"/><br/>`);
    sessionStorage.setItem("totalOptions", optionNumber);
});

const optionsForm = document.querySelector("#options_form_container");
const optionStatus = document.querySelector('#option_status');


optionsForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const questionID = sessionStorage.getItem("questionID");
    if (!questionID) {
        optionStatus.innerText = "Please add a question first.";
        return;
    }
    optionStatus.innerText = "Loading..";

    const formData = new FormData(event.target);
    const formProps = Object.fromEntries(formData);
   
    const options = Object.values(formProps);
    axios.post("/add_option/", {
        options: options
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function(response) {
        console.log(response);
        if (response.status===201) {
            sessionStorage.removeItem("questionID");
            window.location.href = `/vote/${questionID}/`;
        } else {
            console.log(response.data);
            optionsForm.innerHTML = response.data;
        }
    }).catch(function(error) {
        console.log(error)
        if (error.response) {
            optionStatus.innerText = error.response.data.message;
        } else {
            optionStatus.innerText = "Some error occurred. Try again later.";
        }
    });
});
/*
const optionForm = document.querySelector("#option_form");
const optionStatus = document.querySelector('#option_status');

optionForm.addEventListener("submit", function(event) {
    event.preventDefault();
    const questionID = sessionStorage.getItem("questionID");
    if (!questionID) {
        optionStatus.innerText = "Please add a question first.";
        return;
    }
    optionStatus.innerText = "Loading..";

    const formData = new FormData(event.target);
    const formProps = Object.fromEntries(formData);
   
    const options = Object.values(formProps);
    axios.post("/add_option/", {
        options: options
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function(response) {
        sessionStorage.removeItem("questionID");
        window.location.href = `/vote/${questionID}/`;
    }).catch(function(error) {
        if (error.response) {
            optionStatus.innerText = error.response.data.message;
        } else {
            optionStatus.innerText = "Some error occurred. Try again later.";
        }
    });
});*/