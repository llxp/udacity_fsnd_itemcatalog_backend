var previousShownState = 0;

function addCategory() {
    jumbotronAddCategoryBox = getElement('jumbotronAddCategoryBox');
    if(jumbotronAddCategoryBox) {
        hideAllBoxes();
        hideAllButtons();
        showElement(jumbotronAddCategoryBox);
    }
    return false;
}

function cancelAddCategory() {
    jumbotronAddCategoryBox = getElement('jumbotronAddCategoryBox');
    if(jumbotronAddCategoryBox) {
        hideElement(jumbotronAddCategoryBox);
    }
    showAllButtons();
    restorePreviousState();
    return false;
}

function confirmAddCategory(url) {
    cancelAddCategory();
    addCategoryTitle = getElement('addCategoryTitle').value;
    // send an ajax request to the server to add the new category
    request = sendAjaxPOSTRequest(url, 'category='+encodeURI(addCategoryTitle));
    request.addEventListener('error', function(event) {
        displayErrorAlert('error adding the category to the catalog');
    });
    request.addEventListener('load', function(event) {
        if(request.status == 200) {
            displaySuccessAlert('the category was added successfully');
            setTimeout(function() {
                window.location.reload();
            }, 500);
        } else {
            displayErrorAlert('error adding the category to the catalog');
        }
    });
    return false;
}