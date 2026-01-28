document.addEventListener("DOMContentLoaded", function () {
  let locationButton = document.querySelector(".explore-button");

  //getCurrentPosition function calls both showPosition and getError callback functions
  navigator.geolocation.getCurrentPosition(
   showPosition,
   getError

  );
  // position is returned by the getCurrentPosition and passed as a variable into the showPosition function
  async function showPosition(position) {
      let latitude = position.coords.latitude;
      let longitude = position.coords.longitude;

      let responseData = await getCityName(latitude, longitude);
      let cityName = responseData.city
      locationButton.innerText = "Explore " + cityName;
      locationButton.classList.remove("hidden")

      //      location.reload()
      console.log(responseData);
      //GET CITY NAME.
      locationButton.addEventListener("click", async function() {
        console.log(`${this} got clicked`);
        console.log(cityName)
        window.location.href = `/${encodeURIComponent(cityName)}` //navigate to page when user clicks on button
//        let reqStatus = await makeShowVenueRequest(cityName);

      });
  }





  function getError(error) {

      switch (error.code) {
        case error.PERMISSION_DENIED:
          locationButton.innerText = "User denied location access.";
          break;
        case error.POSITION_UNAVAILABLE:
          locationButton.innerText = "Location unavailable.";
          break;
        case error.TIMEOUT:
          locationButton.innerText = "Location request timed out..";
          break;
        default:
          locationButton.innerText = "An unknown error occurred.";
      }
  }

  async function getCityName(lat, lng) {
    try {
      let response = await fetch(`/reverse/geo?latitude=${lat}&longitude=${lng}`);
      if(!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }
      const data = await response.json();
      return data
    }catch(error) {
      console.log(error)
    }
  }

});








