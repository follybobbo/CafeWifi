document.addEventListener("DOMContentLoaded", function () {

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
});




function applyChanges(classOf, borderToChang) {
  if (classOf == "low") {
    borderToChang.style.borderColor = "red";
  } else if(classOf == "medium") {
    borderToChang.style.borderColor = "orange";
  } else {
    borderToChang.style.borderColor = "green";
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