"use strict";


function initMap() {

  // Specify where the map is centered
  // Defining this variable outside of the map optios markers
  // it easier to dynamically change if you need to recenter
  var myLatLng = {lat: 37.8272, lng: -122.2913};

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('weather-map'), {
    center: myLatLng,
    scrollwheel: false,
    zoom: 5,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    styles: MAPSTYLES,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });
////////////
// marker //
////////////

function addMarker() {
  var myImageURL = 'static/white-marker.png';
  var bayArea = new google.maps.LatLng(37.8272, -122.2913);
  var marker = new google.maps.Marker({
      position: bayArea,
      map: map,
      title: 'Hover text',
      icon: myImageURL
  });
  return marker;
}

var marker = addMarker();

/////////////////
// info window //
/////////////////

function addInfoWindow() {

  var contentString = '<div id="content">' +
    '<h1>All my custom content</h1>' +
    '</div>';

  var infoWindow = new google.maps.InfoWindow({
    content: contentString,
    maxWidth: 200
  });

  marker.addListener('click', function() {
    infoWindow.open(map, marker);
  });
}
}
// addInfoWindow()


