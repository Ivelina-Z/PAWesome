let hoverTrigger = Array.from(document.querySelectorAll('.hover-trigger'));

function showHoverInfo(event) {
    let hoverDiv = event.target.parentElement;
    let hoverInfo = hoverDiv.querySelector('.hover-info');
    hoverInfo.style.display = 'block';
    document.addEventListener('keydown', handleEscKeyPress);

}

function hideHoverInfo(event) {
    let hoverDiv = event.target.parentElement;
    let hoverInfo = hoverDiv.querySelector('.hover-info');
    hoverInfo.style.display = 'none';
    document.removeEventListener('keydown', handleEscKeyPress);
}

function handleEscKeyPress(event) {
    if (event.key === 'Escape') {
        hideHoverInfo(event);
    }
}

hoverTrigger.forEach(element => {
    element.addEventListener('mouseover', showHoverInfo);
    element.addEventListener('click', hideHoverInfo);
})