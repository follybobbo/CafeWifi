

document.addEventListener("DOMContentLoaded", () => {
  const placePicker = document.getElementById("placePicker");
  const locationInput = document.getElementById("location-input");
  const locationUrl = document.getElementById("location-url");

  // Listen for selection event from Google Place Picker

  placePicker.addEventListener("gmpx-placechange", () => {
    const place = placePicker.value;
    console.log(place);
    /*IF A PLACE IS CHOSEN RUN THE CODE BELOW*/
    if (place) {
//        DISPLAY MAP AND MARKER
//        console.log(place.formattedAddress);

        console.log(place.displayName);
//        SETS DISPLAY NAME TO FORM INPUT
        locationInput.value = place.displayName;


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

//        GET PICTURES AND DISPLAY ON PAGE
        let pictureArray = place.photos;
        let pictures = document.querySelectorAll(".location-picture");
//        console.log(pictures.length);
        noOfPictures = pictures.length;
//        console.log(pictureArray);
        pictureArray.forEach(function (object, index) {
//              const authorAttributions = object.authorAttributions;
//              console.log(authorAttributions[0].photoURI);
            let img = document.createElement('img');
            img.src =  object.getURI();

            if (index < noOfPictures) {
               pictures[index].setAttribute("src", img.src);
//               console.log(pictures[index]);
            }
        });


//        GET HIDDEN ITEMS  TO DISPLAY AFTER EVERYTHING IS SET
         let itemsToShow = document.querySelectorAll(".hidden");
         itemsToShow.forEach( function (object) {
            object.classList.add("show-hidden")
         });




    }



  });


});





let pictures = document.querySelectorAll(".location-picture");

pictures.forEach(function (object) {
   object.addEventListener("click", function () {
//     console.log(this)
     const selectedPicture = this;
   });
   object.addEventListener("mouseenter", function () {
     this.classList.toggle("add-focus");
   });

   object.addEventListener("mouseleave", function () {
     this.classList.toggle("add-focus");
   });

});



