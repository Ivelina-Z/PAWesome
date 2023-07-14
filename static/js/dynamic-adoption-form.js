function addQuestionField() {
    const questionsContainer = document.querySelector('.questions-container');
    const questionInput = document.getElementById(`id_form-0-question`);
    const totalForms = questionsContainer.children.length;
    let newField = questionInput.cloneNode(true);
    newField.name = `form-${totalForms}-question`;
    newField.id = `id_form-${totalForms}-question`;
    newField.value = '';


    let crossIcon = document.createElement('i');
    crossIcon.className = "fas fa-times";
    crossIcon.onclick = deleteQuestionField;
    let newParagraph = document.createElement('p');
    newParagraph.appendChild(newField);
    newParagraph.appendChild(crossIcon);
    questionsContainer.appendChild(newParagraph);
}

function deleteQuestionField() {
    const fieldParagraph = this.parentNode;
    fieldParagraph.remove();
}

function updateTotalForms() {
    const questionsContainer = document.querySelector('.questions-container');
    const totalForms = questionsContainer.children.length;
    const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');
    totalFormsInput.value = totalForms;
    console.log(totalFormsInput);
}
