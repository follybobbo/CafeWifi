

document.addEventListener("DOMContentLoaded", () => {
  const placePicker = document.getElementById("placePicker");
  const locationInput = document.getElementById("location-input");
  const locationUrl = document.getElementById("location-url");
  const map = document.getElementById("map");


  // Listen for selection event from Google Place Picker
  map.addEventListener("gmp-map-ready", function () {console.log("hello map")})
  placePicker.addEventListener("gmpx-placechange", () => {
    const place = placePicker.value;
    console.log(place);
    if (place) {
        console.log(place.formattedAddress);
        let pictureArray = place.photos;
        console.log(pictureArray);
        pictureArray.forEach(function (object, index) {
              const authorAttributions = object.authorAttributions;
//              console.log(authorAttributions[0].photoURI);
//            let img = document.createElement('img');
//            img.src =  photo.getURI()
//            console.log(img.src)
        })
//        console.log(place.displayName);
//      locationInput.value = place.formattedAddress || place.displayName || "";
//      console.log(place.formattedAddress);
//      console.log(place.displayName);
        const lat = Number(place.location.lat());
        const lng = Number(place.location.lng());
        console.log(lat);
        console.log(lng);
        map.center = {lat, lng};
        map.zoom = 15;



//        const classMap = map.map;
//        const marker = new google.maps.marker.AdvancedMarkerElement({
//        map: classMap,
//        position: {lat, lng},
//        title: place.displayName,
//
//
//        });




//    1  GET MAP PICTURE AND ASSIGN INT VARIABLE AND SET ATTRIBUTE

//    2 GET PICTURES OF PLACES FOR USER TO SELECT
    }


  });


});


