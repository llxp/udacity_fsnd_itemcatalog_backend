var previousShownState = 0;

function addItem() {
    jumbotronAddItemBox = getElement('jumbotronAddItemBox');
    if(jumbotronAddItemBox) {
        hideAllBoxes();
        hideAllButtons();
        showElement(jumbotronAddItemBox);
    }
    return false;
}

function cancelAddItem() {
    jumbotronAddItemBox = getElement('jumbotronAddItemBox');
    hideElement(jumbotronAddItemBox);
    showAllButtons();
    restorePreviousState();
    return false;
}

function confirmAddItem(url) {
    cancelAddItem(); // function simply just hides the add box and restores the previous state
    
    newTitle = getElement('addTitle').value;
    newDescription = getElement('addDescription').value;
    newCategory = getElement('addCategory').value;
    
    // send an ajax request to the server to add the new item
    request = sendAjaxPOSTRequest(url, 'title='+encodeURI(newTitle)+'&description='+encodeURI(newDescription)+'&category_id='+newCategory);
    request.addEventListener('error', function(event) {
        displayErrorAlert('error adding the item to the catalog');
    });
    request.addEventListener('load', function(event) {
        if(request.status == 200) {
            displaySuccessAlert('item successfully added to the catalog');
            setTimeout(function() {
                window.location.reload();
            }, 500);
        } else {
            displayErrorAlert('error adding the item to the catalog');
        }
    });
}