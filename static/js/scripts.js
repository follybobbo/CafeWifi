

document.addEventListener("DOMContentLoaded", () => {
  const placePicker = document.getElementById("placePicker");
  const locationInput = document.getElementById("location-input");
//  const locationUrl = document.getElementById("location-url");

  // Listen for selection event from Google Place Picker
  placePicker.addEventListener("gmpx-placechange", () => {
    const place = placePicker.value;
    console.log(place);
    if (place) {
      locationInput.value = place.formattedAddress || place.displayName || "";

      console.log(locationInput.value)

//      if (locationUrl) {
//        locationUrl.value = place.googleMapsUri || "";
//      }
    }


  });


});


