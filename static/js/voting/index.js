/* Question creation script */
const questionForm = document.querySelector("#question_form");
const questionBox = document.querySelector("#question_box");
const questionStatus = document.querySelector("#question_status");

questionForm.addEventListener("submit", function(event) {
    event.preventDefault();

    const questionStatus = document.querySelector("#question_status");
    const clearLoading = showLoading(questionStatus);
        
    questionStatus.innerText = "Loading..";

    const questionBox = document.querySelector("#question_box");

    axios.post('/add_question/', {
        question: questionBox.value
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function (response) {
        clearLoading()
        questionStatus.innerText = "Question created.";
        sessionStorage.setItem("questionID", response.data.secondary_id);
    })
    .catch(function (error) {
        clearLoading()
        questionStatus.innerText = "Some error occurred. Try again later.";
    });
});

/* More option form adding scripts */
const addMoreOptionButton = document.querySelector("#add_more_option_button");

addMoreOptionButton.addEventListener('click', function(event) {
    event.preventDefault(); 
  
    const totalForms = document.querySelector("#id_form-TOTAL_FORMS");
    const formNum = parseInt(totalForms.value);
    
    const newForm = `
        <div class="option_form">
            <input type="hidden" name="form-${formNum}-id" id="id_form-${formNum}-id">
            <label for="id_form-${formNum}-text">Option ${formNum+1}:</label>
            <input type="text" name="form-${formNum}-text" maxlength="1000" id="id_form-${formNum}-text">
        </div>`;
    addMoreOptionButton.insertAdjacentHTML("beforebegin", newForm);
    totalForms.setAttribute('value', `${formNum+1}`); 
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
    const clearLoading = showLoading(optionStatus);
        
    const formData = new FormData(event.target);
    const formProps = Object.fromEntries(formData);
 
    axios.post("/add_option/", {
        options: formProps
    }, {
        headers: {
            'X-CSRFToken': csrftoken
        }
    }).then(function(response) {
        clearLoading();
        if (response.status === 201) {
            sessionStorage.removeItem("questionID");
            window.location.href = `/vote/${questionID}/`;
        } else {
            optionsForm.innerHTML = response.data;
            optionStatus.innerText = "";
        }
    }).catch(function(error) {
        clearLoading();
        if (error.response) {
            optionStatus.innerText = error.response.data.message;
        } else {
            optionStatus.innerText = "Some error occurred. Try again later.";
        }
    });
});