document.addEventListener('DOMContentLoaded', function () {
    let currentLocationField = document.getElementById('id_current_residence');
    function enableExtraCurrentLocationField() {
        console.log('event triggered.')
        let chosenCurrentLocation = currentLocationField.value;
        let vetField = document.getElementById('id_vet');
        let fosterHomeField = document.getElementById('id_foster_home');

        if (chosenCurrentLocation === 'vet') {
            vetField.disabled = false;
            fosterHomeField.disabled = true;
            fosterHomeField.value = '';
        } else if (chosenCurrentLocation === 'foster_home') {
            vetField.disabled = true;
            vetField.value = '';
            fosterHomeField.disabled = false;
        } else {
            vetField.disabled = true;
            fosterHomeField.disabled = true;
        }
    }
    currentLocationField.addEventListener('input', enableExtraCurrentLocationField)
})