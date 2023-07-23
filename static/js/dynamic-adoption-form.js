function addFormsetField() {
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

    // let crossIcon = document.createElement('i');
    // crossIcon.className = "fas fa-times";
    // crossIcon.onclick = deleteQuestionField;

    newCard.appendChild(newFormSet);
    newCard.appendChild(formSetImage);
    // newCard.appendChild(crossIcon);

    formsetContainer.appendChild(newCard);
    // let formSetImageField = Array.from(formSetImage.children);
    // const form = formInput.parentNode;
    // const totalForms = formsetContainer.children.length;
    // newFormSet.style.display = 'block';
    // let newFormFields= Array.from(newForm.children);
    // newFormFields.forEach(element => {
    //     if (element.tagName === 'INPUT') {
    //         const newInputId = element.getAttribute('id').replace('0', String(totalForms));
    //         element.setAttribute('id', newInputId);
    //         const newInputName = element.getAttribute('name').replace('0', String(totalForms));
    //         element.setAttribute('name', newInputName)
    //     } else if (element.tagName === 'LABEL') {
    //         const newLabelForValue = element.getAttribute('for').replace('0', String(totalForms));
    //         element.setAttribute('for', newLabelForValue);
    //     }
    // });





    // let newFormSetDiv = document.createElement('div');
    // newFormSetDiv.classList.add('formset', 'd-flex', 'justify-content-between', 'bg-blurred');

    // newFormSet.classList.add('w-75');
    // crossIcon.classList.add('pl-2');

    // newFormSetDiv.appendChild(newFormSet);
    // newFormSetDiv.appendChild(crossIcon);

}


function updateFieldsFormNumber(field, formNumber){
    if (field.tagName === 'INPUT') {
        const newInputId = field.getAttribute('id').replace('0', String(formNumber));
        field.setAttribute('id', newInputId);
        const newInputName = field.getAttribute('name').replace('0', String(formNumber));
        field.setAttribute('name', newInputName)
    } else if (field.tagName === 'LABEL') {
        const newLabelForValue = field.getAttribute('for').replace('0', String(formNumber));
        field.setAttribute('for', newLabelForValue);
    }
}
// function addFormsetField(fieldId) {
//     const prefix = fieldId.split('-')[0].split('_').slice(1).join('_');
//     const fieldName = fieldId.split('-').pop();
//     const formsetContainer = document.querySelector('.formset-container');
//     const formInput = document.getElementById(fieldId);
//     const form = formInput.parentNode;
//     const totalForms = formsetContainer.children.length;
//     let newForm = form.cloneNode(true);
//     newForm.style.display = 'block';
//     let newFormFields= Array.from(newForm.children);
//     newFormFields.forEach(element => {
//         if (element.tagName === 'INPUT') {
//             const newInputId = element.getAttribute('id').replace('0', String(totalForms));
//             element.setAttribute('id', newInputId);
//             const newInputName = element.getAttribute('name').replace('0', String(totalForms));
//             element.setAttribute('name', newInputName)
//         } else if (element.tagName === 'LABEL') {
//             const newLabelForValue = element.getAttribute('for').replace('0', String(totalForms));
//             element.setAttribute('for', newLabelForValue);
//         }
//     });
//
//     let crossIcon = document.createElement('i');
//     crossIcon.className = "fas fa-times";
//     crossIcon.onclick = deleteQuestionField;
//     let newParagraph = document.createElement('div');
//     newForm.classList.add('w-75');
//     crossIcon.classList.add('pl-2');
//     newParagraph.appendChild(newForm);
//     newParagraph.appendChild(crossIcon);
//     newParagraph.classList.add('d-flex', 'flex-row');
//     formsetContainer.appendChild(newParagraph);
// }

// function addFormsetField(fieldId) {
//     const prefix = fieldId.split('-')[0].split('_').slice(1).join('_');
//     const fieldName = fieldId.split('-').pop();
//     const formsetContainer = document.querySelector('.formset-container');
//     const formInput = document.getElementById(fieldId);
//     const totalForms = formsetContainer.children.length;
//     let newField = formInput.cloneNode(true);
//     newField.name = `${prefix}-${totalForms}-${fieldName}`;
//     newField.id = `id_${prefix}-${totalForms}-${fieldName}`;
//     newField.value = '';
//
//
//     let crossIcon = document.createElement('i');
//     crossIcon.className = "fas fa-times";
//     crossIcon.onclick = deleteQuestionField;
//     let newParagraph = document.createElement('p');
//     newField.classList.add('w-75');
//     crossIcon.classList.add('px-2');
//     newParagraph.appendChild(newField);
//     newParagraph.appendChild(crossIcon);
//     newParagraph.classList.add('d-flex');
//     formsetContainer.appendChild(newParagraph);
// }

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
