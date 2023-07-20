function cnsl(text) {
    document.querySelector("cnsl").innerHTML += `${text}</br>`
}

const questionForm = document.querySelector("#question_form");

questionForm.addEventListener('htmx:beforeRequest', function(event) {
    const questionStatus = document.querySelector("#question_status");
    questionStatus.innerHTML = "";
    const clearLoading = showLoading(questionStatus);
    
    questionForm.addEventListener('htmx:beforeSwap', function(event) {
        const responseHTML = event.detail.xhr.response;
        const parser = new DOMParser();
        const parsedHTML = parser.parseFromString(responseHTML, "text/html");
        const questionSecondaryID = JSON.parse(parsedHTML.querySelector('#question_secondary_id').textContent);
        console.log(questionSecondaryID);
        sessionStorage.setItem("questionSecondaryID", questionSecondaryID);
        clearLoading();
    });
});

const optionsForm = document.querySelector("#options_form");

optionsForm.addEventListener("htmx:beforeRequest", function(event) {
    const optionStatus = document.querySelector('#option_status');
    const questionSecondaryID = sessionStorage.getItem("questionSecondaryID");
  
    if (!questionSecondaryID) {
        
        optionStatus.innerText = "Please add a question first.";
        htmx.trigger('#options_form', 'htmx:abort');
        return
    }
    optionStatus.innerHTML = "";
    const clearLoading = showLoading(optionStatus);
    
    optionsForm.addEventListener('htmx:beforeSwap', function(event) {
        clearLoading();
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
