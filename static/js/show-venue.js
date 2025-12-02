document.addEventListener("DOMContentLoaded", async function () {
  let location = document.querySelector(".sv-heading");
  let locationValue = location.innerText;


  try {
    const response = await fetch(`/api/latlong?city=${encodeURIComponent(locationValue)}`);
    if (!response.ok) {
       throw new Error("HTTP error! status: $(response.status)");
    }
    const data = await response.json();
    console.log(data)

    const map =  new google.maps.Map(document.getElementById("sv-map"), {
      zoom: 4,
      center: data[0]
    });

    const bounds = await new google.maps.LatLngBounds();
    const infoWindow = new google.maps.InfoWindow();

    //loop through list of lat/long, then use latitude and logitude to generate map.
    data.forEach( location => {
      const marker =  new google.maps.Marker({
        position: {lat: location.lat, lng: location.lng},
        map,
        title: location.title
      });

      marker.addListener("click", () => {
        infoWindow.setContent(
           `<div style="font-size: 14px; padding: 10px 10px 10px 10px; text-align: centre;">
            <strong>${location.title}</strong><br>
          </div>`
        );
        infoWindow.open(map, marker)
      });

      bounds.extend({lat: location.lat, lng: location.lng})

    } );
    map.fitBounds(bounds)

  } catch(error) {
    console.log("Fetch failed", error);
  }


});