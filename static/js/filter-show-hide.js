let crossIcon = document.querySelector('.fa-times');
let filterIcon = document.querySelector('.fa-filter');


function hideFilter(event) {
    let filterContainer = document.querySelector('.filter-container');
    const hiddenFilterContainerWidth = 40;
    filterContainer.style.left = `-${filterContainer.offsetWidth - hiddenFilterContainerWidth}px`;
    crossIcon.style.display = 'none';
    filterIcon.style.display = 'block';
    let contentContainer = filterContainer.nextElementSibling;
    contentContainer.style.marginLeft = `${hiddenFilterContainerWidth}px`;
}

function showFilter(event) {
    let filterContainer = document.querySelector('.filter-container');
    filterContainer.style.left = '0';
    crossIcon.style.display = 'block';
    filterIcon.style.display = 'none';
    let contentContainer = filterContainer.nextElementSibling;
    contentContainer.style.marginLeft = `${filterContainer.offsetWidth}px`;
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