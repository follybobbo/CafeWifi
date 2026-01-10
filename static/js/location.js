document.addEventListener("DOMContentLoaded", function () {

  let borderToChangeList = document.querySelectorAll(".tooltip-container p");

  borderToChangeList.forEach(function (borderToChange, index) {
    let classOfElement = borderToChange.classList.value;
    applyChanges(classOfElement, borderToChange);
  });



//  hover effect on reaction buttons

  let reactionEmojiList = document.querySelectorAll(".unto i");

  reactionEmojiList.forEach(function (reactionEmoji, index) {

       var clicked = false;
       reactionEmoji.addEventListener("mouseenter", function () {
            if (!clicked) {
              let className = reactionEmoji.classList[1];
              let newName = fill(className);

              this.classList.replace(className, newName);
              changeBackgroundColor(index, reactionEmoji);
            }
       });

      reactionEmoji.addEventListener("mouseleave", function () {
            if (!clicked) {
              let className = reactionEmoji.classList[1];
              let newName = deFill(className);

              this.classList.replace(className, newName);
              removeBackgroundColor(index, reactionEmoji);
            }
      });

      reactionEmoji.addEventListener("click", function () {
            clicked = !clicked; //when user clicks the opposite of the current value of click becomes its new value.

            if (clicked) {
              let className = reactionEmoji.classList[1];
//              let newName = fill(className);
              this.classList.replace(className, className);
              changeBackgroundColor(index, reactionEmoji);
            } else {
              let className = reactionEmoji.classList[1];
              let newName = deFill(className);

              this.classList.replace(className, newName);
              removeBackgroundColor(index, reactionEmoji);
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