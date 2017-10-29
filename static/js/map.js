jQuery(function($) {
    // Asynchronously Load the map API
    var script = document.createElement('script');
    script.src = "//maps.googleapis.com/maps/api/js?key=AIzaSyDNVdKelw47aJbPkz7rZyasRSKjhkE_3Oc&sensor=false&callback=initialize";
    document.body.appendChild(script);
});

function initialize() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'
    };

    // Display a map on the page
    map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
    map.setTilt(45);


    // Multiple Markers
    var markers = [
        ['London Eye, London', 51.503454,-0.119562],
        ['Palace of Westminster, London', 51.499633,-0.124755]
    ];

    var infoWindowContent = [
        ['<div class="info_content">' +
        '<h3>London Eye</h3>' +
        '<p>The London Eye is a giant Ferris wheel situated on the banks of the River Thames. The entire structure is 135 metres (443 ft) tall and the wheel has a diameter of 120 metres (394 ft).</p>' +        '</div>'],
    ];


    $.get("/api/map", function(data,status){
      var markers = JSON.parse(data);
      console.log("markers: " + markers);


    console.log("markers: " + markers);
    // Display multiple markers on a map
    var infoWindow = new google.maps.InfoWindow(), marker, i;
    var infoWindowContent = [];
    console.log('starting for loop');
    for(var j = 0; j < markers.length; j++){
      console.log("markers: " + markers[j]["name"]);
      infoWindowContent.push('<div class="info_content"><h3>'+markers[j]["name"]+'</h3><p>' + markers[j]["description"]+"</p></div>");
    }
    console.log(infoWindowContent);
    // Loop through our array of markers & place each one on the map
    for( var i = 0; i < markers.length; i++ ) {
        var place = markers[i];
        var secretMessages = ['This', 'is', 'the', 'secret', 'message'];
        console.log("place: " + place);
        console.log("current location: " + place["location"]);
        $.get("https://maps.googleapis.com/maps/api/geocode/json?address="
                + place["location"]+ "&key=AIzaSyDNVdKelw47aJbPkz7rZyasRSKjhkE_3Oc",
                  function(data, status){
                      var geometry = data["results"][0]["geometry"];
                      var position = new google.maps.LatLng(geometry["location"]["lat"],geometry["location"]["lng"]);
                      bounds.extend(position);
                      var marker = new google.maps.Marker({
                          position: position,
                          map: map,
                          title: place["name"]
                      });
                      var contentString = infoWindowContent[i];
                      google.maps.event.addListener(marker, 'click', function() {
      var info_window = new google.maps.InfoWindow();
      console.log(i);
    info_window.setContent(infoWindowContent[i]);
    info_window.open(map,marker);

 });
                      console.log(infoWindowContent[i]);
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

                      // Automatically center the map fitting all markers on the screen
                      map.fitBounds(bounds);
                  }
             );
    }

    var geocoder = new google.maps.Geocoder();
      geocoder.geocode( { 'address': "The University of Texas at Austin"}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        map.fitBounds(results[0].geometry.viewport);
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
