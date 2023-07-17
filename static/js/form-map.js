function initMap() {
    let map = L.map('location_map').setView([42.930, 26.027], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    function onClick(event) {
        let mapBlock = document.getElementById('location_map');
        let coordinates = event.latlng;
        const inputField = document.getElementById('id_location')
        inputField.value = `POINT (${coordinates.lat} ${coordinates.lng})`;
        console.log(inputField.value);
    }
    map.on('click', onClick);
}
window.addEventListener('DOMContentLoaded', (event) => {
    initMap();
});
