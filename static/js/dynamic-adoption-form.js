function addFormsetField(fieldId) {
    const prefix = fieldId.split('-')[0].split('_').slice(1).join('_');
    const fieldName = fieldId.split('-').pop();
    const formsetContainer = document.querySelector('.formset-container');
    const formInput = document.getElementById(fieldId);
    const totalForms = formsetContainer.children.length;
    let newField = formInput.cloneNode(true);
    newField.name = `${prefix}-${totalForms}-${fieldName}`;
    newField.id = `id_${prefix}-${totalForms}-${fieldName}`;
    newField.value = '';


    let crossIcon = document.createElement('i');
    crossIcon.className = "fas fa-times";
    crossIcon.onclick = deleteQuestionField;
    let newParagraph = document.createElement('p');
    newParagraph.appendChild(newField);
    newParagraph.appendChild(crossIcon);
    formsetContainer.appendChild(newParagraph);
}

// function addQuestionField() {
//     const questionsContainer = document.querySelector('.questions-container');
//     const questionInput = document.getElementById(`id_form-0-question`);
//     const totalForms = questionsContainer.children.length;
//     let newField = questionInput.cloneNode(true);
//     newField.name = `form-${totalForms}-question`;
//     newField.id = `id_form-${totalForms}-question`;
//     newField.value = '';
//
//
//     let crossIcon = document.createElement('i');
//     crossIcon.className = "fas fa-times";
//     crossIcon.onclick = deleteQuestionField;
//     let newParagraph = document.createElement('p');
//     newParagraph.appendChild(newField);
//     newParagraph.appendChild(crossIcon);
//     questionsContainer.appendChild(newParagraph);
// }

function deleteQuestionField() {
    const fieldParagraph = this.parentNode;
    fieldParagraph.remove();
}

function updateTotalForms(fieldId) {
    const prefix = fieldId.split('-')[0].split('_').slice(1).join('_');
    const formsetContainer = document.querySelector('.formset-container');
    const totalForms = formsetContainer.children.length;
    const totalFormsInput = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
    totalFormsInput.value = totalForms;
}
