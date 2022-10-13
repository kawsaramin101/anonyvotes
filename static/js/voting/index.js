/* Question creation script */
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

const optionsFormContainer = document.querySelector("#options_form_container");
const optionForm = document.querySelectorAll(".option_form");
const addMoreOptionButton = document.querySelector("#add_more_option_button");
const totalForms = document.querySelector("#id_form-TOTAL_FORMS");

/* More option form adding scripts */
let formNum = optionForm.length - 1;
addMoreOptionButton.addEventListener('click', function(event) {
    event.preventDefault();

    const newForm = optionForm[0].cloneNode(true); //Clone the option form
    let formRegex = RegExp(`form-(\\d){1}-`,'g'); //Regex to find all instances of the form number

    formNum++; //Increment the form number
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`);//Update the new form to have the correct form number
    optionsFormContainer.insertBefore(newForm, addMoreOptionButton); //Insert the new form at the end of the list of forms

    totalForms.setAttribute('value', `${formNum+1}`); //Increment the number of total forms in the management form
});

/* Option creating scripts */
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
 
    axios.post("/add_option/", {
        options: formProps
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function(response) {
        if (response.status === 201) {
            sessionStorage.removeItem("questionID");
            window.location.href = `/vote/${questionID}/`;
        } else {
            optionsForm.innerHTML = response.data;
            optionStatus.innerText = "";
        }
    }).catch(function(error) {
        if (error.response) {
            optionStatus.innerText = error.response.data.message;
        } else {
            optionStatus.innerText = "Some error occurred. Try again later.";
        }
    });
});