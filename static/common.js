function getElement(id) {
    return document.getElementById(id);
}

function sendAjaxPUTRequest(url, data) {
    return sendAjaxFormRequest(url, data, 'PUT');
}

function sendAjaxPOSTRequest(url, data) {
    return sendAjaxFormRequest(url, data, 'POST');
}

function sendAjaxDELETERequest(url, data) {
    return sendAjaxFormRequest(url, data, 'DELETE');
}

function sendGETRequest(url) {
    if (window.XMLHttpRequest) {
        // code for modern browsers
        xmlhttp = new XMLHttpRequest();
      } else {
        // code for old IE browsers
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
     }
     xmlhttp.open('GET', url, true);
     xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     xmlhttp.send();
     return xmlhttp;
}

function sendAjaxFormRequest(url, data, method) {
    if (window.XMLHttpRequest) {
        // code for modern browsers
        xmlhttp = new XMLHttpRequest();
      } else {
        // code for old IE browsers
        xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
     }
     xmlhttp.open(method, url, true);
     xmlhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     if(data) {
        xmlhttp.send(data);
     } else {
         xmlhttp.send();
     }
     return xmlhttp;
}

function blockFormSubmission() {
    return false;
}

function hideElement(element) {
    element.classList.add('d-none');
}

function showElement(element) {
    if(element && elementHidden(element)) {
        element.classList.remove('d-none');
    }
}

function toggleElement(element) {
    if(!elementHidden(element)) {
        hideElement(element);
    } else {
        showElement(element);
    }
}

function elementHidden(element) {
    return element.classList.contains('d-none');
}


/*
// the function is not enabled, because it is not fully working.
// In the disabled state, at least the default tooltips are working
$(document).ready(function () {
    $('[data-toggle="tooltip"]').tooltip();
});*/


var previousState = [];

function hideAllBoxes() {
    jumbotronContent = getElement("jumbotronContent");
    jumbotronEditItemBox = getElement("jumbotronEditItemBox");
    jumbotronAddItemBox = getElement("jumbotronAddItemBox");
    jumbotronDeleteItemBox = getElement("jumbotronDeleteItemBox");
    jumbotronEditCategoryBox = getElement("jumbotronEditCategoryBox");
    jumbotronAddCategoryBox = getElement("jumbotronAddCategoryBox");
    jumbotronDeleteCategoryBox = getElement("jumbotronDeleteCategoryBox");

    if(jumbotronContent && !elementHidden(jumbotronContent)) {
        hideElement(jumbotronContent);
        previousState.push(1);
    }
    if(jumbotronEditItemBox && !elementHidden(jumbotronEditItemBox)) {
        hideElement(jumbotronEditItemBox);
        previousState.push(2);
    }
    if(jumbotronAddItemBox && !elementHidden(jumbotronAddItemBox)) {
        hideElement(jumbotronAddItemBox);
        previousState.push(3);
    }
    if(jumbotronDeleteItemBox && !elementHidden(jumbotronDeleteItemBox)) {
        hideElement(jumbotronDeleteItemBox);
        previousState.push(4);
    }
    if(jumbotronEditCategoryBox && !elementHidden(jumbotronEditCategoryBox)) {
        hideElement(jumbotronEditCategoryBox);
        previousState.push(5);
    }
    if(jumbotronAddCategoryBox && !elementHidden(jumbotronAddCategoryBox)) {
        hideElement(jumbotronAddCategoryBox);
        previousState.push(6);
    }
    if(jumbotronDeleteCategoryBox && !elementHidden(jumbotronDeleteCategoryBox)) {
        hideElement(jumbotronDeleteCategoryBox);
        previousState.push(7);
    }
}

function restorePreviousState() {
    jumbotronContent = getElement("jumbotronContent");
    jumbotronEditItemBox = getElement("jumbotronEditItemBox");
    jumbotronAddItemBox = getElement("jumbotronAddItemBox");
    jumbotronDeleteItemBox = getElement("jumbotronDeleteItemBox");
    jumbotronEditCategoryBox = getElement("jumbotronEditCategoryBox");
    jumbotronAddCategoryBox = getElement("jumbotronAddCategoryBox");
    jumbotronDeleteCategoryBox = getElement("jumbotronDeleteCategoryBox");

    tempPreviousState = 0;
    if(previousState.length > 0) {
        tempPreviousState = previousState.pop();
    }
    switch(tempPreviousState) {
        case 1:
            toggleElement(jumbotronContent);
        break;
        case 2:
            toggleElement(jumbotronEditItemBox);
        break;
        case 3:
            toggleElement(jumbotronAddItemBox);
        break;
        case 4:
            toggleElement(jumbotronDeleteItemBox);
        break;
        case 5:
            toggleElement(jumbotronEditCategoryBox);
        break;
        case 6:
            toggleElement(jumbotronAddCategoryBox);
        break;
        case 7:
            toggleElement(jumbotronDeleteCategoryBox);
        break;
    }
}

function hideAllButtons() {
    addItemButton = getElement('addItemButton');
    editCategoryButton = getElement('editCategoryButton');
    addCategoryButton = getElement('addCategoryButton');

    if(addItemButton) {
        hideElement(addItemButton);
    }
    if(editCategoryButton){
        hideElement(editCategoryButton);
    }
    if(addCategoryButton) {
        hideElement(addCategoryButton);
    }
}

function showAllButtons() {
    addItemButton = getElement('addItemButton');
    editCategoryButton = getElement('editCategoryButton');
    addCategoryButton = getElement('addCategoryButton');

    if(addItemButton) {
        showElement(addItemButton);
    }
    if(editCategoryButton){
        showElement(editCategoryButton);
    }
    if(addCategoryButton) {
        showElement(addCategoryButton);
    }
}

function displayErrorAlert(errorMessage) {
    errorAlertBox = getElement('errorAlertBox');
    htmlString = ' \
    <div class="alert alert-danger alert-dismissible fade show" role="alert"> \
        <div>' + errorMessage +'</div> \
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"> \
            <span aria-hidden="true">&times;</span> \
        </button> \
    </div>';
    errorAlertBox.innerHTML = htmlString;
}

function displaySuccessAlert(successMessage) {
    errorAlertBox = getElement('errorAlertBox');
    htmlString = ' \
    <div class="alert alert-success alert-dismissible fade show" role="alert"> \
        <div>'+successMessage+'</div> \
        <button type="button" class="close" data-dismiss="alert" aria-label="Close"> \
            <span aria-hidden="true">&times;</span> \
        </button> \
    </div>';
    errorAlertBox.innerHTML = htmlString;
}