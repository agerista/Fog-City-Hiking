use strict;

function showSearchResults(results) {
    alert(results);
    console.log(results);
}

function submitSearch(evt) {

    
    var formValues = {

        "trail": $("#trail").val(),
        "parking": $("#parking").val(),
        "restrooms": $("#restrooms").val(),
    };

    $.post("/search",
          formInputs,
          showSearchResults);
}

$("#search-form").on("submit", submitSearch);