//ADD.HTML
 document.addEventListener("DOMContentLoaded", () => {
  const placePicker = document.getElementById("placePicker");
  const locationInput = document.getElementById("location-input");
  const locationUrl = document.getElementById("location-url");

  const rowOne = document.querySelector(".picture-row-1");
  const rowTwo = document.querySelector(".picture-row-2");



  // Listen for selection event from Google Place Picker


    placePicker.addEventListener("gmpx-placechange", async () => {
    const place = placePicker.value;

    /*IF A PLACE IS CHOSEN RUN THE CODE BELOW*/
    if (place) {
        //FETCH DATA FROM BACKEND AND CHECK
        const listOfPlaces = await fetchListOfPlaces();
        let existsResult = checkIfPlaceExist(listOfPlaces, place.displayName);
//        console.log(exists);
//        console.log(place.id);

        console.log(existsResult.exist);
        if (existsResult.exist) {
            console.log("place already exist");
            //HIDE ALL VISIBLE SECTIONS THAT SHOULD ONLY SHOW WHEN SELECTION IS SUCCESFULL OR PLACE DOESNT EXIST
            let stuffToHide = document.querySelectorAll(".hidden");  //selects all inputs that are currently hidden
            stuffToHide.forEach(function (obj, index) {
              obj.classList.remove("show-hidden")    //removes show-hidden class if the restaurant entered exists in the data base

            });
            //DISPLAY ERROR MESSAGE
            let errorMessage = document.querySelector(".error-msg");
            errorMessage.classList.add("show-err-msg");

            errorMessage.addEventListener("click", async function () {
               let placeDetails = existsResult.placeDetails;
               console.log(placeDetails);
               getRequestToLocation(placeDetails.city, placeDetails.name)
//               let fetchResponse = await getRequestToLocation(placeDetails.city, placeDetails.name)
//
//               if (!fetchResponse.ok) {
//                 console.log(fetchResponse.data?.message)
//                 return
//               }
//               console.log(fetchResponse.status);
//              call function
            });

            //clear any previously stored elements to prevent posting wrong things to backend
        } else {
            //removes error message from screen if place search does not exist in database
            let errorMessage = document.querySelector(".error-msg");
            errorMessage.classList.remove("show-err-msg");

    //      DISPLAY MAP AND MARKER
            rowOne.innerHTML = "";   //make rowOne and rowTwo empty
            rowTwo.innerHTML = "";
    //        console.log(place.addressComponents.length)
    //        console.log(place.addressComponents)
    //        LOOP THROUGH ADDRESS COMPONENT AND GET DETAILS OF LOCATION
            let addressComponentArray = place.addressComponents;
            console.log(addressComponentArray)
            let streetName, country, streetNo, city, postalCode;

            addressComponentArray.forEach(
              function(object, index) {
                 if (object["types"][0] == "route") {
                    streetName = object["longText"];                     //STREET NAME
                 } else if (object["types"][0] == "country") {
                    country = object["longText"];                        //COUNTRY
                 } else if (object["types"][0] == "street_number") {
                    streetNo = object["longText"];                      //STREET NO
                 } else if (object["types"][0] == "postal_town") {
                     city = object["longText"];                          //CITY
                 } else if (object["types"][0] == "postal_code") {
                    postalCode = object["longText"];                     //POSTAL CODE
                 }
              }
            );

            let address = streetNo + " " + streetName + ", " + city + ", " + postalCode + ", " + country;
    //        TRANSFER CITY AND COUNTRY TO FORM INPUT
            let formCity = document.querySelector(".city");
            formCity.value = city

            let formCountry = document.querySelector(".country");
            formCountry.value = country;

            let formStreet = document.querySelector(".street-one");
            formStreet.value = address;


    //      SETS DISPLAY NAME TO FORM INPUT
            locationInput.value = place.displayName;        //NEEDED

            const lat = Number(place.location.lat());      //NEEDED PROBABLY SDK
            const lng = Number(place.location.lng());      //NEEDED PROBABLY SDK

            let latitudeInput = document.querySelector("#latitude-input");
            let longitudeInput = document.querySelector("#longitude-input")

            latitudeInput.value = lat;
            longitudeInput.value = lng;

    //      create map object using latitude and longitude
            let refinedMap = await new google.maps.Map(document.getElementById("map"), {
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

            let pictureArray = place.photos;
            console.log(pictureArray.at(0).name)

    //      GET PICTURES AND DISPLAY ON PAGE
    //      A PROMISE WAS USED HERE SO IT WILL BE EASY TO ADD EVENT LISTENERS TO THE IMAGES AFTER THEY HAVE BEEN LOADED.
    //      IT WAS DIFFICULT WITHOUT USING PROMISES BECAUSE ADDING THE EVENT LISTENER PREVIOUSLY HAPPENED BEFORE THE PICTURES WERE LOADED SUCCESSFULLY/
            function loadIt() {
              return new Promise(function (resolve, reject) {
                let pictureArray = place.photos;
                let lenOfPictureArray = pictureArray.length;

                pictureArray.forEach(function (object, index) {
                console.log(object.name);
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
            // ONLY ADD EVENT LISTENER AFTER ALL IMAGE ELELMENT HAVE BEEN SUCCESSFULLY LOADED.
            loadIt().then(addIt);  //adds event listener when all img elements have beem successfully loaded.

    }
    }
  });
 });





//EVENT LISTENER SECTION
//data is the promise returned from the loadIt function
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
     urlFormInput.value = this.getAttribute("src");   //NEEDED
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


//uses async function to fetch restaurant that exist in the database

async function fetchListOfPlaces() {
  try {
    const response = await fetch("/api/restaurants");
    if (!response.ok) {
      throw new Error(`HTTP error! status: $(response.status)`);
    }
    const placeList = await response.json();

    return placeList;

  } catch(error) {
     console.log("Fetch Failed", error)
  }
}

//FUNCTION CHECKS IF RESTAURANT INPUT BY USER EXISTS.
//ARGUMENTS LIST = LIST OF PLACES SENT FROM BACKEND, PLACE, NAME OF RESTAURANT ENETERED BY USER.
function checkIfPlaceExist(List, place) {
  for (item of List) {
    if (item.name == place) {
      return {exist: true, placeDetails: item}
    } else {
      return {exist: false}
    }
  }

//  return List.includes(place)

}



//function to make get request if user click on HERE
function getRequestToLocation(city, name) {
  window.location.href = `/${encodeURIComponent(city)}/${encodeURIComponent(name)}`
}







