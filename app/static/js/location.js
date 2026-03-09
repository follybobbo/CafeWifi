document.addEventListener("DOMContentLoaded", async function () {

  //LOAD PRESET VALUE OF SUMMARY


  let borderToChangeList = document.querySelectorAll(".tooltip-container a");


  borderToChangeList.forEach(function (borderToChange, index) {
    let classOfElement = borderToChange.classList.value;
    applyChanges(classOfElement, borderToChange);
  });



//  hover effect on reaction buttons
  let clicked_list = []
  let summaryValue = document.querySelector(".unto").classList[1];  //get value of summary
  let reactionEmojiList = document.querySelectorAll(".unto i");
     //sets state of buttons. ensures color does not change when user hovers or moves cursor over a clicked button
  //THE EMOJI CLICKING LOGIC MECHANISM IS EXPLAINED BELOW:
//  1. ADD CLICKED DATASET TO ALL reactionEmoji,


  reactionEmojiList.forEach(function (reactionEmoji, index) {
//       reactionEmoji.classList.add("disabled-link")
       reactionEmoji.dataset.clicked = false; //sets default value of data set on all reactionEmoji
        //       let clicked = (reactionEmoji.dataset.clicked.toString() === "true");


       reactionEmoji.addEventListener("mouseover", function () {
            clicked = (this.dataset.clicked.toString() === "true");
            if (!clicked) {
              let className = reactionEmoji.classList[1];
              let newName = fill(className);     //adds '-flll' to the existing class name if not filled e.g 'bi-heart' becomes 'bi-heart-fill'

              this.classList.replace(className, newName);   //replaces 'bi-heart' with 'bi-heart-fill' in classList: element.classList.replace(oldClass, newClass);
              changeBackgroundColor(index, reactionEmoji);   //applies a color changing class depending on index.
            }
       });

      reactionEmoji.addEventListener("mouseout", function () {
            clicked = (this.dataset.clicked.toString() === "true");
            if (!clicked) {
              let className = reactionEmoji.classList[1];
              let newName = deFill(className);   //removes '-flll' in the existing class name if filled e.g 'bi-heart-fill' becomes 'bi-heart'

              this.classList.replace(className, newName);  //replaces : element.classList.replace(oldClass, newClass);
              removeBackgroundColor(index, reactionEmoji);  //removes background image from emoji
            }
      });

      reactionEmoji.addEventListener("click", async function () {

            this.dataset.clicked = true;  //tracks if this was clicked or not.

            clicked = (this.dataset.clicked.toString() === "true"); //converts to string then compare
            let fillStatus = this.classList[3];

            if (clicked) {

              //happens if user is clicking on an emoji that is not already clicked
              if (clicked_list.length == 1) {

                  //deals with instance where user is clicking another button when a button has already been clicked.

                  let alreadyClicked = clicked_list[0][0];       //clickedList = [this -> <i class="bi bi-heart-fill rating-emoji med"></i>, index]
                  let indexAlreadyClicked = clicked_list[0][1];  //index of previously clicked

                  clicked_list[0][0].dataset.clicked = false;    //change clicked dataset value of previously clicked button


                  //THIS SECTION OF CODE DEALS WITH DE-FILLING OR DE-COLOURING PREVIOUSLY CLICKED BUTTON
                  let alreadyClickedClassName = alreadyClicked.classList[1];
                  let defillAlreadyClickedClassName = deFill(alreadyClickedClassName);                       //returns de-filled background name
                  alreadyClicked.classList.replace(alreadyClickedClassName, defillAlreadyClickedClassName);  //make
                  removeBackgroundColor(indexAlreadyClicked, alreadyClicked);

                  alreadyClicked.closest("span").classList.remove("disabled-link");                                         //once user clicks another button, remove disable class from previous button


                  clicked_list.length = 0; //RESET CLICKED LIST
                  console.log(`${clicked_list.length} clicked inside clicked_list length`)
              }


              clicked_list.push([this, index]);              //add newly clicked button to clicked_list array

              let className = reactionEmoji.classList[1];
              this.classList.replace(className, className); //dont need to fill or de-fill because on clicking user is already hovering hence fill class already applied.
                                                            //i.e bi-heart-fill = bi-heart-fill {fill class is active as user is already hovering before clicked}

              changeBackgroundColor(index, reactionEmoji);  //changes background color, naturally the fill class default background color is black
              this.closest("span").classList.add("disabled-link")           //disable button once user clicks, so as to control user input

              //MAKE AJAX REQUEST TO SERVER TO UPDATE VALUE OF SUMMARY


              //adds emoji that has been clicked to display container in header
              let containerOfHeaderEmoji = document.querySelector("#emoji");
              let cloneOfEmoji = this.cloneNode(true);
              cloneOfEmoji.style.fontSize = "16px";
              containerOfHeaderEmoji.replaceChildren();
              containerOfHeaderEmoji.appendChild(cloneOfEmoji);

              //AJAX FUNCTION TO UPDATE SUMMARY
              let valueOfEmoji = reactionEmoji.id;  //ID STORES THE SUMMARY VALUE.
              let nameOfRestaurant = document.querySelector(".location-name").innerText;
              let response = updateSummary(valueOfEmoji, nameOfRestaurant);
              console.log(response)




            }
      });
      //LOADS DEFAULT VALUE OF SUMMARY INTO THE EMOJI
      let valueOfEmoji = reactionEmoji.id;

      if (summaryValue == valueOfEmoji) {
       //      let selectedEmoji = reactionEmoji;
        clicked_list.push([reactionEmoji, index]);
        console.log(clicked_list)
        let className = reactionEmoji.classList[1];
        let newName = fill(className);
        reactionEmoji.classList.replace(className, newName);
        changeBackgroundColor(index, reactionEmoji);
        reactionEmoji.closest("span").classList.add("disabled-link");


         //adds emoji that has been clicked to display container in header
         let containerOfHeaderEmoji = document.querySelector("#emoji");
         let cloneOfEmoji = reactionEmoji.cloneNode(true);
         cloneOfEmoji.style.fontSize = "16px";
         containerOfHeaderEmoji.replaceChildren();
         containerOfHeaderEmoji.appendChild(cloneOfEmoji);



      }

  });

//  Report closed mechanism
  let closedButton = document.querySelector("#report-closed");  //will go
  let closedBanner = document.querySelector("#closed");
  let updatePageButton = document.querySelector("#update-button");

  let valueOfClosedButton = closedButton.innerText;
  let nameOfRestaurant = document.querySelector(".location-name").innerText;




//CHECK STATUS THEN DO EFFECT OR NOT

  let closedStatusData = await checkStatus(nameOfRestaurant)
  let isOpenedOnLoad = closedStatusData.status
  console.log(isOpenedOnLoad)

  //FUNCTION TO EFFECT CHANGE
  if (isOpenedOnLoad) {
      console.log("True")
      removeEffectOnRestaurantOpen(closedButton, closedBanner, reactionEmojiList, borderToChangeList, updatePageButton);
  } else {
      console.log("False")
      addEffectOnRestaurantClose(closedButton, closedBanner, reactionEmojiList, borderToChangeList, updatePageButton);
  }

  //  IF USER CLICKS ON REPORT CLOSED BUTTON
  closedButton.addEventListener("click", async function(){
    let statusData = await checkStatus(nameOfRestaurant);
    let isOpened = statusData.status


     //    CHECK DATASET OF BUTTON
    if (isOpened) {
     //      REPORT CLOSED
      let report_res = await reportClosedOrOpened(nameOfRestaurant);
      addEffectOnRestaurantClose(closedButton, closedBanner, reactionEmojiList, borderToChangeList, updatePageButton);
    } else {
      let report_res = await reportClosedOrOpened(nameOfRestaurant)
      removeEffectOnRestaurantOpen(closedButton, closedBanner, reactionEmojiList, borderToChangeList, updatePageButton);

    }

  });

     //SELECTS PRE-SAVED VALUE ON LOAD.



});




function applyChanges(classOf, borderToChang) {
  if (classOf == "low") {
    borderToChang.style.borderColor = "red";
  } else if(classOf == "medium") {
    borderToChang.style.borderColor = "orange";
  } else if (classOf == "high") {
    borderToChang.style.borderColor = "green";
  } else {
    borderToChang.classList.add("disabled-link")
  }
}


function fill(className) {
//  let className = Emoji.classList[1];
  let newClassName = className + "-fill";

  return newClassName;
}

function deFill(className) {
  let newClassNameList = className.split("-");
  let first = newClassNameList.at(0);
  let second = newClassNameList.at(1);

  let newClassName = first + "-" + second;
  return newClassName;
}

function changeBackgroundColor(index, Emoji) {
  if (index == 0) {
    Emoji.classList.add("lo");
  } else if (index == 1) {
    Emoji.classList.add("med");
  } else {
    Emoji.classList.add("hig");
  }
}

function removeBackgroundColor(index, Emoji) {
  if (index == 0) {
    Emoji.classList.remove("lo");
  } else if (index == 1) {
    Emoji.classList.remove("med");
  } else {
    Emoji.classList.remove("hig");
  }
}



async function checkStatus(nameOfRestaurant) {
  try{
     const response = await fetch(`/restaurant/status?name=${encodeURIComponent(nameOfRestaurant)}`);
     if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
     }
     const data = await response.json()
//     console.log(data)
//     console.log("AJAX FETCH");
     return data
  } catch(error) {
    console.log(error)
  }

}

//USED ID LATER
async function reportClosedOrOpened(nameOfRestaurant) {
    try {
//        MAKE PATCH REQUEST
        const response = await fetch(`/restaurant/closed-or-opened`, {
        method: "PATCH",
        headers: {
         "Content-Type": "application/json"
        },
        body: JSON.stringify({name: nameOfRestaurant})
        });

       if(!response.ok) {
        throw new Error(`HTTP error ${response.status}`)
       }
       const data = await response.json();
       console.log(data)

    }catch(error) {
        console.log(error)
    }

}


function addEffectOnRestaurantClose(button, banner, emojiList, listOfBorderToChange, updateButton) {
    button.textContent = "NOT CLOSED";

    banner.classList.remove("closed-display");

    emojiList.forEach(function(obj, index){
        obj.classList.add("disabled-link");
    });

    listOfBorderToChange.forEach(function(obj, ind) {
       obj.classList.add("disabled-link")
    });

    updateButton.classList.add("disabled-link");


}

function removeEffectOnRestaurantOpen(button, banner, emojiList, listOfBorderToChange, updateButton) {
    button.textContent = "REPORT CLOSED";

    banner.classList.add("closed-display");

    emojiList.forEach(function(obj, index){
        obj.classList.remove("disabled-link");
    });

    listOfBorderToChange.forEach(function(obj, ind) {
       obj.classList.remove("disabled-link")
    });

    updateButton.classList.remove("disabled-link");

}




async function updateSummary(summary, nameOfRestaurant) {
  try {
    response = await fetch(`/update/summary`, {
    method: "PATCH",
    headers: {
         "Content-Type": "application/json"
    },
    body: JSON.stringify({
    name: nameOfRestaurant,
    summary_value: summary
    })

    });
    if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
    }
    result = await response.json();
    return result;
  } catch(error) {
    console.log(error);
  }

}
