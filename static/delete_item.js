function deleteItem(url) {
    jumbotronDeleteItemBox = getElement('jumbotronDeleteItemBox');
    if(elementHidden(jumbotronDeleteItemBox)) {
        hideAllBoxes();
        hideAllButtons();
        showElement(jumbotronDeleteItemBox);
    }
}

function cancelDeleteItem() {
    jumbotronDeleteItemBox = getElement('jumbotronDeleteItemBox');
    if(!elementHidden(jumbotronDeleteItemBox)) {
        hideElement(jumbotronDeleteItemBox);
    }
    showAllButtons();
    restorePreviousState();
}

function confirmDeleteItem(url) {
    cancelDeleteItem();  // function simply just hides the ddelete box and restores the previous state
    // send an ajax request to the server to remove the current item
    request = sendAjaxDELETERequest(url, '');
    request.addEventListener('error', function(event) {
        // show an error message, delete failed
        displayErrorAlert('error removing the item');
    });
    request.addEventListener('load', function(event) {
        if(request.status == 200) {
            // show a message, that the delete successful
            displaySuccessAlert('item successfully removed');
            setTimeout(function() {
                window.location = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port;
            }, 500);
        } else {
            // show an error message, delete failed
            displayErrorAlert('error removing the item');
        }
    });
}