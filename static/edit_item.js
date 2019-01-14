function editItem(url) {
    jumbotronEditItemBox = getElement('jumbotronEditItemBox');
    if(jumbotronEditItemBox) {
        hideAllBoxes();
        hideAllButtons();
        showElement(jumbotronEditItemBox);
    }
    return false;
}

function cancelEditItem() {
    if(elementHidden(jumbotronContent)) {
        showElement(jumbotronContent);
        hideElement(jumbotronEditItemBox);
    }
    showAllButtons();
    return false;
}

function confirmEditItem(url) {
    cancelEditItem();  // function simply just hides the edit box and restores the previous state
    newTitle = getElement('editTitle').value;
    newDescription = getElement('editDescription').value;
    newCategory = getElement('editCategory').value;
    oldTitle = getElement('displayTitle').innerHTML;
    oldDescription = getElement('displayDescription').innerHTML;
    
    if(newTitle !== oldTitle) {
        getElement('displayTitle').innerHTML = newTitle;
    }
    if(newDescription !== oldDescription) {
        getElement('displayDescription').innerHTML = newDescription;
    }
    
    // send an ajax request to the server to save the changes made to the item
    request = sendAjaxPUTRequest(url, 'title='+encodeURI(newTitle)+'&description='+encodeURI(newDescription)+'&category_id='+newCategory);
    request.addEventListener('error', function(event) {
        displayErrorAlert('error editing the item');
    });
    request.addEventListener('load', function(event) {
        if(request.status == 200) {
            // show a message, that the editing was successful
            displaySuccessAlert('item successfully edited');
            setTimeout(function() {
                window.location.reload();
            }, 500);
        } else {
            displayErrorAlert('error editing the item');
        }
    });
}