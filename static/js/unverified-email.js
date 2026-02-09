document.addEventListener("DOMContentLoaded", function () {
  let resendButton = document.querySelector(".resend-email");

  resendButton.addEventListener("click", async function () {
    console.log("clicked")
    let response = await resendVerificationLink()
    if(response.status == "sent") {
      resendButton.innerText = "Sent"
    }
  });


})

async function resendVerificationLink() {
  try {
    const response = await fetch("/send-verification", {
     method: "POST",
     headers: {
      "Content-Type": "application/json"
     }
    })
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    const responseData = await response.json();
    console.log(responseData)
    return responseData

  }catch(error) {
    console.log("Fetch Failed", error)
  }



}