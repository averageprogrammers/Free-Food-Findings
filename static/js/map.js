jQuery(function($) {
    // Asynchronously Load the map API
    var script = document.createElement('script');
    script.src = "//maps.googleapis.com/maps/api/js?key=AIzaSyACw_ke4ccRtwOcsqzMKL3X7WFqpR8VTtw&sensor=false&callback=initialize";
    document.body.appendChild(script);
});



var map;
var mapOptions = {
    mapTypeId: 'roadmap'
};
var markers;
var infoWindowContent = [];
var UTLat

function initialize() {
    console.log("initializing map");
    var bounds = new google.maps.LatLngBounds();
    var info_window = new google.maps.InfoWindow();


    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);


    $.get("/map/api", function(data,status){
      markers = JSON.parse(data);

    // Display multiple markers on a map
    for(var j = 0; j < markers.length; j++){
      console.log("markers: " + markers[j]["name"]);
      infoWindowContent.push('<div class="info_content"><h5>'+markers[j]["name"]+'</h5><p>' + markers[j]["description"]+"</p></div>");
    }


    // Loop through our array of markers & place each one on the map
    console.log("looping through markers");
    for( var i = 0; i < markers.length; i++ ) {
        var place = markers[i];
        var secretMessages = ['This', 'is', 'the', 'secret', 'message'];
        console.log("current location: " + place["location"]);
        $.get("https://maps.googleapis.com/maps/api/geocode/json?address="
                + place["location"]+ "&key=AIzaSyACw_ke4ccRtwOcsqzMKL3X7WFqpR8VTtw",
                  (function(_i) {

                      return function(data, status){
                          console.log("data result of get : ");
                          console.log(data);
                          var geometry = data["results"][0]["geometry"];
                          var position = new google.maps.LatLng(geometry["location"]["lat"],geometry["location"]["lng"]);
                          bounds.extend(position);
                          var marker = new google.maps.Marker({
                              position: position,
                              map: map,
                              title: place["name"]
                          });
                          console.log("i = " + _i);
                          //console.log('contentString = ' + contentString);
                          google.maps.event.addListener(marker, 'click', (function(_marker,__i) {
                              return function() {
                                  console.log("clicked on marker = " + _marker.title);
                                  //console.log("info window content for marker : " + _content);
                                  var contentString = infoWindowContent[__i];
                                  info_window.setContent(contentString);
                                  info_window.open(map,_marker);
                              }
                          })(marker,_i));
                          console.log(infoWindowContent[_i]);
                          //attachSecretMessage(marker,secretMessages[i]);
    /*
                          google.maps.event.addListener(marker, 'click', function() {
                              return function() {
                                  console.log(infoWindowContent);
                                  console.log("index: " + i);
                                  var place2 = infoWindowContent[i];
                                  console.log("place2: " + place2);
                                  infoWindow.setContent('<div class="info_content"><h3>'+place2["name"]+'</h3><p>' + place2["description"]+"</p></div>");
                                  infoWindow.open(map, marker);
                              }
                          }*/


                      }
                    })(i)
             );
    }
    // Automatically center the map fitting all markers on the screen
    map.fitBounds(bounds);

    var geocoder = new google.maps.Geocoder();
      geocoder.geocode( { 'address': "The University of Texas at Austin"}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        map.fitBounds(results[0].geometry.viewport);
        map.setZoom(15);
      }
      else {
          map.setCenter({lat:30.284921, long:-97.735843});
          map.setZoom(15);
      }
    });


  });

    // Override our map zoom level once our fitBounds function runs (Make sure it only runs once)
    var boundsListener = google.maps.event.addListener((map), 'bounds_changed', function(event) {
        this.setZoom(14);
        google.maps.event.removeListener(boundsListener);
    });

}


function attachSecretMessage(marker, secretMessage) {
        var infowindow = new google.maps.InfoWindow({
          content: secretMessage
        });

        marker.addListener('click', function() {
          infowindow.open(marker.get('map'), marker);
        });
      }
