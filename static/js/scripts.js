

document.addEventListener("DOMContentLoaded", () => {
  const placePicker = document.getElementById("placePicker");
  const locationInput = document.getElementById("location-input");
  const locationUrl = document.getElementById("location-url");

  const rowOne = document.querySelector(".picture-row-1");
  const rowTwo = document.querySelector(".picture-row-2");



  // Listen for selection event from Google Place Picker


    placePicker.addEventListener("gmpx-placechange", () => {
    const place = placePicker.value;

    /*IF A PLACE IS CHOSEN RUN THE CODE BELOW*/
    if (place) {
//      DISPLAY MAP AND MARKER
        rowOne.innerHTML = "";
        rowTwo.innerHTML = "";
        console.log(place.displayName);
//      SETS DISPLAY NAME TO FORM INPUT
        locationInput.value = place.displayName;

        const lat = Number(place.location.lat());
        const lng = Number(place.location.lng());

//      create map object using latitude and longitude
        let refinedMap = new google.maps.Map(document.getElementById("map"), {
           zoom: 15,
           center: new google.maps.LatLng(lat, lng),
           mapTypeId: google.maps.MapTypeId.ROADMAP
        });

//      create marker to be displayed on map
        const point = new google.maps.LatLng(lat, lng);
        marker = new google.maps.Marker({
           map: refinedMap,
           position: point,
           title: place.displayName,
        });

//      GET PICTURES AND DISPLAY ON PAGE
        function loadIt() {
          return new Promise(function (resolve, reject) {
            let pictureArray = place.photos;
            let lenOfPictureArray = pictureArray.length;

            pictureArray.forEach(function (object, index) {

//           let img = document.createElement('img');
            if (index < 4) {

               let imgUri =  object.getURI();
               let img = document.createElement('img');
               img.setAttribute("src", imgUri);
               img.alt = "picture of location";
               img.tabIndex = -1;
               img.classList.add("location-picture");


               if (index < 2) {
                  let rowOne = document.querySelector(".picture-row-1");
                  rowOne.appendChild(img);
               } else {
                   let rowTwo = document.querySelector(".picture-row-2");
                   rowTwo.appendChild(img);
               }
            }

           });

//         GET HIDDEN ITEMS  TO DISPLAY AFTER EVERYTHING IS SET
         let itemsToShow = document.querySelectorAll(".hidden");
         itemsToShow.forEach( function (object, index) {
            object.classList.add("show-hidden");

         });

            let pictures = document.querySelectorAll(".location-picture");
            resolve(pictures);
          });
        }

        loadIt().then(addIt);  //adds event listener when all img elements have beem successfully loaded.

    }
  });
});





//EVENT LISTENER SECTION

function addIt(data) {
   let clickedArray = [];

   data.forEach(function (object, index) {
   object.addEventListener("click", function () {

//     LOGIC TO REMOVE STYLE FROM PREVIOUSLY SELECTED PHOTO WHEN NEW PHOTO IS SELECTED.
     if (clickedArray.length > 0) {
        clickedArray[0].classList.remove("clicked");   //CHECK IF CLICKED ARRAY HAS ANY CONTENT UPON NEW CLICK, IF SO REMOVE STYLE
     }
     clickedArray.length = 0;


     let clickedIndex = index;
     const selectedPicture = this;

//     STORES SELECTED PICTURE IN CLICKED ARRAY
     clickedArray.push(this);

//     WTF FORM INPUT ASSIGNED TO VARIABLE
     let urlFormInput = document.querySelector("#url-value");

//     ASSIGNS SRC VALUE TO FORM INPUT VARIABLE
     urlFormInput.value = this.getAttribute("src");
     console.log(urlFormInput.value);
     this.classList.toggle("clicked");

   });

   object.addEventListener("mouseenter", function () {
     this.classList.toggle("add-focus");
   });

   object.addEventListener("mouseleave", function () {
     this.classList.toggle("add-focus");
   });

});


}





