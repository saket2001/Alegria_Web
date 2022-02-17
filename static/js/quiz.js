inputBtnList = document.querySelectorAll(".custom_input");

inputBtnList.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    // first removing active class from all buttons
    inputBtnList.forEach((btn) => {
      btn.classList.remove("custom_input-active");
      btn.removeAttribute("name");
    });
    // console.log(e.target.children[0]);
    e.target.children[0].setAttribute("name", "selected-answer");
    e.target.classList.add("custom_input-active");
  });
});
