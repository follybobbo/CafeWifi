//function getDropDownItems () {
//  return new Promise(function (resolve, reject) {
//  let selectElement = document.querySelectorAll("select");
//
//  selectElement.forEach(function (element, index) {
//  element.addEventListener("click", function () {
//     let elementId = element.id
//     let options = document.querySelectorAll("#" + elementId + " option")
//     resolve(options)
//   });
//  });
//
//
//  });
//
//}
//
//
//
//getDropDownItems().then(styleList);
//
//
//
//
//
//function styleList(data) {
// console.log(data)
// data.forEach(function (item, index) {
//
//    item.addEventListener("click", function () {
//      console.log("hello")
//    });
// });
//
//}





//let selectElement = document.querySelectorAll("select");
//
//selectElement.forEach(function (element, index) {
//   element.addEventListener("click", function () {
//        let elementId = element.id
//        let options = document.querySelectorAll("#" + elementId + " option")
//
//        options.forEach( function (listOptions, index) {
//          console.log(listOptions)
//
//           listOptions.addEventListener("mouseenter", function () {
//               console.log(index)
//               if (index == 1) {
//                  this.classList.toggle("option-one")
//               } else if (index == 2) {
//                  this.classList.toggle("option-one")
//               } else if (index == 3) {
//                  this.classList.toggle("option-one")
//               }
//               this.classList.toggle("")
//           });
//
//           listOptions.addEventListener("mouseleave", function () {
//                this.classList.toggle("option-one")
//           });
//
//        });
//
//   });
//});






