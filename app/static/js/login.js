document.addEventListener("DOMContentLoaded", function () {

//    calls the promise maker function, runs function 1 when success, runs function 2 when error
    let checkIfFlashMessage = flashMessageGetter()
    checkIfFlashMessage.then(

    //    function 1
        function (flashMessage) {
            setTimeout(function () {
                flashMessage.classList.add("hide-stuff")
            }, 4000);
        },

    //    function 2
        function (error) {
            console.log(error);
        }
    );


//    calls the promise maker function, runs function 1 when success, runs function 2 when error
    let coolDownContainerPromise = cooldownContainerGetter()
    coolDownContainerPromise.then(
//        function 1
        function (coolDownContainer) {
//             console.log(coolDownContainer)
             doTheStuffFunction(coolDownContainer);
        },
//        function 2
        function (error) {
            console.log(error)
        }
    );

//    calls this function on success/promise fulfillment of coolDownContainerPromise
    function doTheStuffFunction (containerOfCounter) {
//        colors timer text red
        containerOfCounter.classList.add("color-red");
        let coolDownValue = containerOfCounter.innerText;
//        console.log(coolDownValue)

//        formats time on first display
        formatTimer(coolDownValue);
        //        let timer = setInterval(counterFunction, 1000);
//        calls setInterval function that runs repeatedly until  coolDownValue equals 0
        let timer = setInterval(function () {
            coolDownValue--;
            if (coolDownValue == 0) {
                  clearInterval(timer);
                  containerOfCounter.classList.add("hide-stuff");
                  containerOfCounter.classList.remove("color-red");
                    //flash tou ca now login
            }

            formatTimer(coolDownValue);
        }, 1000);

//        format timer from ss to min:sec
        function formatTimer(timeInSeconds) {
            if (timeInSeconds < 60) {
            containerOfCounter.innerText = `00:${timeInSeconds}`
            }else {
            let min, sec
            min = Math.trunc(timeInSeconds/60)
            sec = timeInSeconds % 60
            containerOfCounter.innerText = `${min}:${sec}`
            }


        }



    }

//returns a promise that contains the flash message container: cause it is only available when certain conditions are met i.e failed login attempt
function flashMessageGetter() {
        return new Promise(function (resolve, reject) {
            let flashContainer = document.querySelector("#flash-list")
            if (flashContainer) {
                resolve(flashContainer);
            }else{
                reject("Flash Message does not exist yet");
            }
        });
    }

//returns a promise that contains the cool down container: cause it is only available when certain conditions are met i.e failed login attempt
function cooldownContainerGetter() {

    return new Promise(function (resolve, reject) {
        let coolDownContainer = document.querySelector("#cooldown-time");
        if (coolDownContainer) {
            resolve(coolDownContainer);
        }else {
            reject("Container Not Available");
        }

    })


}




  });




//------------------------------------TRIED AJAX BUT ERROR----------------------------------------
//async function getTimerValue(user_email) {
//  try {
//        const response = await fetch(`/api/get-backoff?email=${encodeURIComponent(user_email)}`);
//        console.log(`/api/get-backoff?email=${encodeURIComponent(user_email)}`)
//
////        const response = await fetch(`/api/get-backoff`, {
////            method: "POST",
////            headers: {
////                "content-Type": "application/json"
////            },
////            body: JSON.stringify({email: user_email})
////        });
//
//        if (!response.ok) {
//            throw new Error(`HTTP error! status: ${response.status}`)
//        }
//        const responseData = await response.text();
//        return {
//            status: 1,
//            message: responseData
//        }
//
//  } catch(error) {
////        console.log(error)
//        return {
//             status: 0,
//             message: error.message
//
//        }
//  }
//
//}

