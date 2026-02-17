document.addEventListener("DOMContentLoaded", function () {
  let resendButton = document.querySelector(".resend-email-btn");
  let counter = 30;

  //IF USER GOES TO ANOTHER PAGE AND COMES BACK, THE COUNTER MUST STILL GO ON
  //Check state of button, if disabled, try to get current time, keep on counting
  //else enable button and dont show counter


  resendButton.addEventListener("click", async function () {
    let response = await resendVerificationLink()

    if(response.message === "sent") {
      resendButton.innerText = "Sent";
      console.log(response.status);
    }

  });

})


function startCountDown() {
  let counter = 30;
  let resendButton = document.querySelector(".resend-email-btn");
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

function disappearingMessage(message) {
  let messageContainer = document.querySelector("#too-many-request");
  messageContainer.innerText = message;
  messageContainer.classList.remove("hide-stuff");

  setTimeout(function () {
    messageContainer.classList.add("hide-stuff")
  }, 5000)

}


async function resendVerificationLink() {
  try {
    const response = await fetch("/resend-verification", {
     method: "POST",
    })

    const responseData = await response.json();

    if (!response.ok) {
      disappearingMessage(responseData.message)
//      console.log(responseData.message)
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    startCountDown();       //START COUNTDOWN
    return responseData

  }catch(error) {
    console.log("Fetch Failed", error)
     return {
      status: 0,
      message: "Network error"
    };
  }


}