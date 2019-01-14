function deleteCategory() {
    jumbotronDeleteCategoryBox = getElement('jumbotronDeleteCategoryBox');
    if(jumbotronDeleteCategoryBox) {
        hideAllBoxes();
        hideAllButtons();
        showElement(jumbotronDeleteCategoryBox);
    }
    return false;
}

function cancelDeleteCategory() {
    jumbotronDeleteCategoryBox = getElement('jumbotronDeleteCategoryBox');
    if(!elementHidden(jumbotronDeleteCategoryBox)) {
        hideElement(jumbotronDeleteCategoryBox);
    }
    showAllButtons();
    restorePreviousState();
    return false;
}

function confirmDeleteCategory(url) {
    cancelDeleteCategory(); // function simply just hides the delete box and restores the previous state

    // send an ajax request to the server to remove the current category
    request = sendAjaxDELETERequest(url, '');
    request.addEventListener('error', function(event) {
        // show an error message, delete failed
        displayErrorAlert('error removing the category');
    });
    request.addEventListener('load', function(event) {
        if(request.status == 200) {
            // show a message, that the delete successful
            displaySuccessAlert('category successfully removed');
            setTimeout(function() {
                window.location = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
            }, 500);
        } else {
            // show an error message, delete failed
            displayErrorAlert('category removing the item');
        }
    });
    return false;
}