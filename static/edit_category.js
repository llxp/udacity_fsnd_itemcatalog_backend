function editCategory() {
    jumbotronEditCategoryBox = getElement('jumbotronEditCategoryBox');
    if(jumbotronEditCategoryBox) {
        hideAllBoxes();
        hideAllButtons();
        showElement(jumbotronEditCategoryBox);
    }
    return false;
}

function cancelEditCategory() {
    jumbotronEditCategoryBox = getElement('jumbotronEditCategoryBox');
    if(jumbotronEditCategoryBox) {
        hideElement(jumbotronEditCategoryBox);
    }
    showAllButtons();
    restorePreviousState();
    return false;
}

function confirmEditCategory(url) {
    cancelEditCategory();
    editCategoryTitle = getElement('editCategoryTitle').value;
    // send an ajax request to the server to save the changes made to the category
    request = sendAjaxPUTRequest(url, 'category='+encodeURI(editCategoryTitle));
    request.addEventListener('error', function(event) {
        displayErrorAlert('error adding the category');
    });
    request.addEventListener('load', function(event) {
        if(request.status == 200) {
            displaySuccessAlert('the category was edited successfully');
            setTimeout(function() {
                window.location.reload();
            }, 500);
        } else {
            displayErrorAlert('error editing the category');
        }
    });
    return false;
}