

document.addEventListener("DOMContentLoaded", () => {
  const placePicker = document.getElementById("placePicker");
  const locationInput = document.getElementById("location-input");
  const locationUrl = document.getElementById("location-url");

  // Listen for selection event from Google Place Picker

  placePicker.addEventListener("gmpx-placechange", () => {
    const place = placePicker.value;
    console.log(place);
    if (place) {
//        DISPLAY MAP AND MARKER
        console.log(place.formattedAddress);

//        console.log(place.displayName);
//      locationInput.value = place.formattedAddress || place.displayName || "";
//      console.log(place.formattedAddress);
//      console.log(place.displayName);
        const lat = Number(place.location.lat());
        const lng = Number(place.location.lng());


        let refinedMap = new google.maps.Map(document.getElementById("map"), {
           zoom: 15,
           center: new google.maps.LatLng(lat, lng),
           mapTypeId: google.maps.MapTypeId.ROADMAP
        });



        const point = new google.maps.LatLng(lat, lng);
        marker = new google.maps.Marker({
           map: refinedMap,
           position: point,
           title: place.displayName,
        });


        let pictureArray = place.photos;
        console.log(pictureArray);
        pictureArray.forEach(function (object, index) {
//              const authorAttributions = object.authorAttributions;
//              console.log(authorAttributions[0].photoURI);
            let img = document.createElement('img');
            img.src =  object.getURI();
            console.log(img.src);
        })




//    1  GET MAP PICTURE AND ASSIGN INT VARIABLE AND SET ATTRIBUTE

//    2 GET PICTURES OF PLACES FOR USER TO SELECT
    }


  });


});


let pictures = document.querySelectorAll(".location-picture");

pictures.forEach(function (object) {
   object.addEventListener("click", function () {
     console.log(this)
     const selectedPicture = this;
   });
   object.addEventListener("mouseenter", function () {
     this.classList.toggle("add-focus");
   });

   object.addEventListener("mouseleave", function () {
     this.classList.toggle("add-focus");
   });

});



