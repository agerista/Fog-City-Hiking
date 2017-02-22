use strict;

function showSearchResults(result) {
    alert(result);
}

function submitSearch(evt) {
    evt.preventDefault();
    
    var formValues = {
        "trail": $("#trail-field").val(),
        "city": $("#city-field").val(),
        "duration": $("#duration-field").val(),
        "intensity": $("#intensity-field").val(),
    };

    $.post("/search",
          formInputs,
          showSearchResults);
}

$("#search-form").on("submit", submitSearch);