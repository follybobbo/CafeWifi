

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

//           create map object using latitude and longitude
        let refinedMap = new google.maps.Map(document.getElementById("map"), {
           zoom: 15,
           center: new google.maps.LatLng(lat, lng),
           mapTypeId: google.maps.MapTypeId.ROADMAP
        });


//         create marker to be displayed on map
        const point = new google.maps.LatLng(lat, lng);
        marker = new google.maps.Marker({
           map: refinedMap,
           position: point,
           title: place.displayName,
        });

//        GET PICTURES AND DISPLAY ON PAGE
        let pictureArray = place.photos;                                    //picture array is stored in place.photos attributes.
        let pictures = document.querySelectorAll(".location-picture");      //select all location picture html elements.
//        console.log(pictures.length);
        noOfPictures = pictures.length;
//        console.log(pictureArray);
        pictureArray.forEach(function (object, index) {
//              const authorAttributions = object.authorAttributions;
//              console.log(authorAttributions[0].photoURI);
            let img = document.createElement('img');
            img.src =  object.getURI();                                       //get src using getURI()

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

pictures.forEach(function (object, index) {
   object.addEventListener("click", function () {
     const selectedPicture = this;
     let clickedIndex = index;
     let urlFormInput = document.querySelector("#url-value");
     urlFormInput.value = this.getAttribute("src");
     console.log(urlFormInput.value);
     this.classList.toggle("clicked");

//     if (!index) {
//        this.classList.toggle("clicked");
//     }



   });
   object.addEventListener("mouseenter", function () {
     this.classList.toggle("add-focus");
   });

   object.addEventListener("mouseleave", function () {
     this.classList.toggle("add-focus");
   });

});



