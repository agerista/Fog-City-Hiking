use strict;

///////////////////////////////////////
// This is to retrieve search results//
///////////////////////////////////////

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

//////////////////////////////////
// This is to save hikes to db //
/////////////////////////////////

function saveHikestoDB(results) {
    alert(results);
    console.log(results);
}

function submitHikes(evt) {

    
    var formValues = {

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

/////////////////////////////////////////////////////
//Look into this for possible multi submit purposes// 
/////////////////////////////////////////////////////


// function onSingleSubmitButtonClicked(button)
// {
//   var bookmark = $('form');
//   var data =  frm.serialize();
//   var url = frm.attr('action');
//   var method = frm.attr('data-ajax-method');
//   var target = frm.attr('data-ajax-update');
//   $.ajax({
//     type: method,
//     url: url,
//     data: data,
//     beforeSend: function() {showLoader();},
//     complete: function(response) {$(target).html(response.responseText);hideLoader();}
//   });
// }
