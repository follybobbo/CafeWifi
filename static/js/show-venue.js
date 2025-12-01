document.addEventListener("DOMContentLoaded", async function () {
  let location = document.querySelector(".sv-heading");
  let locationValue = location.value;
  console.log(location.innerText)

  try {
    const response = await fetch('/api/latlong?city=${encodeURIComponent(locationValue)}');
    if (!response.ok) {
       throw new Error("HTTP error! status: $(response.status)");
    }
    const data = await response.json();
    console.log(data)
  } catch(error) {
    console.log("Fetch failed", error)

  }








});