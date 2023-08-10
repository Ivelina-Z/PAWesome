let crossIcon = document.querySelector('.fa-times');
let filterIcon = document.querySelector('.fa-filter');


function hideFilter(event) {
    let filterContainer = document.querySelector('.style-container.filter');
    crossIcon.style.display = 'none';
    filterIcon.style.display = 'block';
    let contentContainer = document.querySelector('.box.filter');
    contentContainer.style.left = `-${contentContainer.offsetWidth * 0.9}px`;
}

function showFilter(event) {
    let filterContainer = document.querySelector('.style-container.filter');
    crossIcon.style.display = 'block';
    filterIcon.style.display = 'none';
    let contentContainer = document.querySelector('.box.filter');
    contentContainer.style.left = `0`;
}

function responsiveHideShowFilter(event) {
    const screenSizeThreshold = 1800;

    if (window.innerWidth <= screenSizeThreshold) {
        hideFilter();
    } else if (window.innerWidth > screenSizeThreshold) {
        showFilter();
    }
}

crossIcon.addEventListener('click', hideFilter);
filterIcon.addEventListener('click', showFilter);
window.addEventListener('resize', responsiveHideShowFilter);
responsiveHideShowFilter();