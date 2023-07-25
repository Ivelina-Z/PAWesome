function addImageFormsetField() {
    let formsetContainer = document.querySelector('.formset-container');

    let formSet = document.querySelector('.formset');
    formSet.classList.remove('bg-blurred');

    const totalForms = formsetContainer.children.length;

    let formSetImage = document.querySelector('.hidden-field');
    formSetImage.style.display = 'block';
    let formSetImageFields = Array.from(formSetImage.children);
    formSetImageFields.forEach(field => {
        updateFieldsFormNumber(field, totalForms);
    })

    let newFormSet = formSet.cloneNode(true);
    let formSetDivs = Array.from(newFormSet.children);
    formSetDivs.forEach(element => {
        let formSetFields = Array.from  (element.children);
        formSetFields.forEach(field => {
            updateFieldsFormNumber(field, totalForms);
        })
    });

    let newCard = document.createElement('div');
    newCard.classList.add('card', 'bg-light', 'text-dark');

    newCard.appendChild(newFormSet);
    newCard.appendChild(formSetImage);

    formsetContainer.appendChild(newCard);
}

function addQuestionField() {
    let formsetContainer = document.querySelector('.formset-container');
    let form = document.querySelector('.form');

    let newQuestionForm = form.cloneNode(true);
    const totalForms = formsetContainer.children.length;
    let questionFormFields = Array.from(newQuestionForm.children);

    questionFormFields.forEach(field => {
        if (field.tagName === 'INPUT') {
            // field.value = '';
            updateFieldsFormNumber(field, totalForms);
        }
    });

    let deleteIcon = document.createElement('i');
    deleteIcon.className = 'fas fa-times';
    deleteIcon.onclick = deleteQuestionField;
    newQuestionForm.appendChild(deleteIcon);

    formsetContainer.appendChild(newQuestionForm);
}

function updateFieldsFormNumber(field, formNumber){
    if (field.tagName === 'INPUT') {
        const newInputId = field.getAttribute('id').replace('0', String(formNumber));
        field.setAttribute('id', newInputId);
        const newInputName = field.getAttribute('name').replace('0', String(formNumber));
        field.setAttribute('name', newInputName);
        field.value = '';
    } else if (field.tagName === 'LABEL') {
        const newLabelForValue = field.getAttribute('for').replace('0', String(formNumber));
        field.setAttribute('for', newLabelForValue);
    }
}

function deleteQuestionField(event) {
    let icon = event.target;
    const fieldParagraph = icon.parentNode;
    fieldParagraph.remove();
}

function updateTotalForms(fieldId) {
    const prefix = fieldId.split('-')[0].split('_').slice(1).join('_');
    const formsetContainer = document.querySelector('.formset-container');
    const totalForms = formsetContainer.children.length
    const totalFormsInput = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
    totalFormsInput.value = totalForms;
}

// function updateTotalForms(fieldId) {
//     const prefix = fieldId.split('-')[0].split('_').slice(1).join('_');
//     const formsetContainer = document.querySelector('.formset-container');
//     const totalForms = formsetContainer.children.length
//     const totalFormsInput = document.querySelector(`#id_${prefix}-TOTAL_FORMS`);
//     totalFormsInput.value = totalForms;
// }
