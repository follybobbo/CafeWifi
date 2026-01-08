document.addEventListener("DOMContentLoaded", function () {

  let borderToChangeList = document.querySelectorAll(".tooltip-container p");

  borderToChangeList.forEach(function (borderToChange, index) {
    console.log(borderToChange);
    let classOfElement = borderToChange.classList.value;
    applyChanges(classOfElement, borderToChange);
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