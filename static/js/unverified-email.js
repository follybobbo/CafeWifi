document.addEventListener("DOMContentLoaded", function () {
  let resendButton = document.querySelector(".resend-email");
  let counter = 30;

  //IF USER GOES TO ANOTHER PAGE AND COMES BACK, THE COUNTER MUST STILL GO ON
  //Check state of button, if disabled, try to get current time, keep on counting
  //else enable button and dont show counter


  resendButton.addEventListener("click", async function () {
    console.log("clicked")
    let response = await resendVerificationLink()

    if(response.status == "sent") {
      resendButton.innerText = "Sent";

    }
  });

})


function startCountDown() {
  resendButton.disabled = true //disables resend button

  let timer = setInterval(function () {             //performs function after every 1 second
   resendButton.innerText = `sent ${counter} s`;
   counter--;

   if (counter < 0) {
     clearInterval(timer);
     resendButton.disabled = false;
     resendButton.innerText = "Resend"
   }

  }, 1000);
}


async function resendVerificationLink() {
  try {
    const response = await fetch("/resend-verification", {
     method: "POST",
     headers: {
      "Content-Type": "application/json"
     }
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const responseData = await response.json();
     startCountDown();
    return responseData

  }catch(error) {
    console.log("Fetch Failed", error)
  }


}