document.addEventListener("DOMContentLoaded", async function () {

  let borderToChangeList = document.querySelectorAll(".tooltip-container a");


  borderToChangeList.forEach(function (borderToChange, index) {
    let classOfElement = borderToChange.classList.value;
    applyChanges(classOfElement, borderToChange);
  });



//  hover effect on reaction buttons
  let clicked_list = []
  let reactionEmojiList = document.querySelectorAll(".unto i");
     //sets state of buttons. ensures color does not change when user hovers or moves cursor over a clicked button

  reactionEmojiList.forEach(function (reactionEmoji, index) {
       reactionEmoji.dataset.clicked = false;
//       let clicked = (reactionEmoji.dataset.clicked.toString() === "true");


       reactionEmoji.addEventListener("mouseover", function () {
            clicked = (this.dataset.clicked.toString() === "true");
            if (!clicked) {
              let className = reactionEmoji.classList[1];
              let newName = fill(className);

              this.classList.replace(className, newName);
              changeBackgroundColor(index, reactionEmoji);
            }
       });

      reactionEmoji.addEventListener("mouseout", function () {
            clicked = (this.dataset.clicked.toString() === "true");
            if (!clicked) {
              let className = reactionEmoji.classList[1];
              let newName = deFill(className);

              this.classList.replace(className, newName);
              removeBackgroundColor(index, reactionEmoji);
            }
      });

      reactionEmoji.addEventListener("click", function () {
//            clicked = !clicked; //when user clicks the opposite of the current value of click becomes its new value.
            this.dataset.clicked = true;
            clicked = (this.dataset.clicked.toString() === "true");
            console.log(clicked)

            if (clicked) {

              if (clicked_list.length == 1) {   //deals with instance where user is clicking another button when a button has already been clicked.
                let alreadyClicked = clicked_list[0][0];
                let indexAlreadyClicked = clicked_list[0][1];
                clicked_list[0][0].dataset.clicked = false;
                console.log(alreadyClicked + "already clicked")
                let alreadyClickedClassName = alreadyClicked.classList[1];
                let defillAlreadyClickedClassName = deFill(alreadyClickedClassName);
                alreadyClicked.classList.replace(alreadyClickedClassName, defillAlreadyClickedClassName);
                removeBackgroundColor(indexAlreadyClicked, alreadyClicked);

                clicked_list.length = 0;

              }

              clicked_list.push([this, index]);
              let className = reactionEmoji.classList[1];
              this.classList.replace(className, className); //dont need to fill or de-fill because on clicking user is already hovering hence fill class already applied.
              changeBackgroundColor(index, reactionEmoji);

              let containerOfHeaderEmoji = document.querySelector("#emoji");
              let cloneOfEmoji = this.cloneNode(true);
              cloneOfEmoji.style.fontSize = "22px";
              containerOfHeaderEmoji.replaceChildren();
              containerOfHeaderEmoji.appendChild(cloneOfEmoji);

              //take that and put up there,
              //store value of selection for calculation.

            } else {   //if user double clicks to unselect button
              console.log(clicked_list);
              let className = reactionEmoji.classList[1];
              let newName = deFill(className);

              this.classList.replace(className, newName);
              removeBackgroundColor(index, reactionEmoji);
              clicked_list.length = 0;
            }
      });
  });

//  Report closed mechanism
  let closedButton = document.querySelector("#report-closed");  //will go
  let closedBanner = document.querySelector("#closed");
  let updatePageButton = document.querySelector("#update-button");

  let valueOfClosedButton = closedButton.innerText;
  let nameOfRestaurant = document.querySelector(".location-name").innerText;



//  check for current value of button before assigning dataset
//  if (valueOfClosedButton == "REPORT CLOSED") {
//    closedButton.dataset.opened = true;
//  } else {
//    closedButton.dataset.opened = false;
//  }
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
//    isOpened = this.dataset.opened.toString() === "true"
    if (isOpened) {
//      REPORT CLOSED
      let report_res = await reportClosedOrOpened(nameOfRestaurant);
      addEffectOnRestaurantClose(closedButton, closedBanner, reactionEmojiList, borderToChangeList, updatePageButton);
    } else {
      let report_res = await reportClosedOrOpened(nameOfRestaurant)
      removeEffectOnRestaurantOpen(closedButton, closedBanner, reactionEmojiList, borderToChangeList, updatePageButton);
//      closedButton.textContent = "REPORT CLOSED";
////      this.dataset.opened = true;
////      REMOVE CLOSED BANNER
//      closedBanner.classList.toggle("closed-display");
//
//      reactionEmojiList.forEach(function(obj, index){
//        obj.classList.remove("disabled-link");
//      });
//      borderToChangeList.forEach(function(obj, ind) {
//       obj.classList.remove("disabled-link")
//      });
//      updatePageButton.classList.remove("disabled-link");

    }

  });
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
