use strict;

///////////////////////////////////////
// This is to retrieve search results//
///////////////////////////////////////

function showSearchResults(results) {
    alert(results);
    console.log(results);
}

function submitSearch(evt) {
    evt.preventDefault();
    
    var formValues = {

        "trail": $("#trail").val(),
        "length": $("#length").val(),
    };

    $.post("/search",
          formInputs,
          showSearchResults);
}

$("#search-form").on("submit", submitSearch);

//////////////////////////////////
// This is to save hikes to db //
/////////////////////////////////

function saveHikestoDB(results) {
    alert(results);
    console.log(results);
}

function submitHikes(evt) {
    evt.preventDefault();
    
    var formValues = {

        "trail_id": $("#trail_id").val(),
        "completed": $("#completed").val(),
        "bookmark": $("#bookmark").val(),
        "date-completed": $("#date-completed").val(),
        "temperature": $("#temperature").val(),
        "condition": $("#condition").val(),
        "comment": $("#comment").val(),
        "rating": $("#rating").val(),
    };

    $.post("/search",
          formInputs,
          showSearchResults);
}

$("#wishlist").on("submit", submitSearch);
