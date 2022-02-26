inputBtnList = document.querySelectorAll(".custom_input");

inputBtnList.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    if (e.target.classList.contains("custom_input-active")) {
      e.target.classList.remove("custom_input-active");
      if (e.target.children[0]) e.target.children[0].removeAttribute("name");
      return;
    }
    // first removing active class from all buttons
    inputBtnList.forEach((btn) => {
      btn.classList.remove("custom_input-active");
      btn.removeAttribute("name");
    });
    e.target.children[0].setAttribute("name", "selected-answer");
    e.target.classList.add("custom_input-active");
  });
});

// window.addEventListener("blur", () => window.location.replace("/quiz"));

// quiz logic
// window.onload = () => {
//   const timerDisplay = document.querySelector(".quiz_timer");
//   let timer_time = 35;
//   let timer = setInterval(() => {
//     if (timer_time === 0) {
//       clearInterval(timer); // show alert
//       alert("Quiz Ended");
//       // redirect to quiz page
//       window.location.replace("/quiz");
//       return;
//     }
//     timer_time -= 1;
//     timerDisplay.innerHTML = `${timer_time}`;
//   }, 1000);
// };
