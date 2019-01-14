function onKeydownSearch() {
    searchbar = getElement('searchbar');
    searchResultsHeadline = getElement('searchResultsHeadline');
    searchbarText = searchbar.value;
    if(searchbarText) {
        request = sendGETRequest(window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/api/catalog/search_item/' + searchbarText);
        request.addEventListener('load', function(event) {
            searchResult = JSON.parse(request.responseText);
            searchResultContainer = getElement('searchResults');
            liPre = '<li><a class="show nav-link" href="' + window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/catalog/category/';
            liPost = '</a></li>';
            searchResultContainer.innerHTML = '';
            fullList = '';
            for(var i = 0; i < searchResult.length; ++i) {
                item = searchResult[i];
                if(item) {
                    html = liPre + item.category + '/item/' + item.id + '">' + item.title + liPost;
                    fullList += html;
                }
            }
            searchResultContainer.innerHTML = fullList;
            showElement(searchResultsHeadline);
        });
    } else {
        searchResultContainer.innerHTML = '';
        hideElement(searchResultsHeadline);
    }
    return true;
}