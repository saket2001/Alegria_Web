const pollForm = document.getElementById("poll-form");
const totalOptions = document.getElementById("optionsNumber");
const addNewPollOptionBtn = document.getElementById("addNewPollOptionBtn");

// this functions add one option input and one image url input in form
function createElements(i = 0) {
  //   option label
  const optionP = document.createElement("p");
  optionP.classList.add("mb-0");
  optionP.classList.add("fs-7");
  optionP.classList.add("main-font");
  optionP.innerHTML = `Option ${i}`;
  pollForm.insertAdjacentElement("beforeend", optionP);

  //   option input
  const optionInput = document.createElement("input");
  optionInput.setAttribute("placeholder", `Option ${i} Name`);
  optionInput.setAttribute("name", `Option ${i} Name`);
  optionInput.classList.add("input_value");
  pollForm.insertAdjacentElement("beforeend", optionInput);

  //   image url label
  const imageP = document.createElement("p");
  imageP.classList.add("mb-0");
  imageP.classList.add("fs-7");
  imageP.classList.add("main-font");
  imageP.innerHTML = `Image Url ${i}`;
  pollForm.insertAdjacentElement("beforeend", imageP);

  //   image url input
  const imageInput = document.createElement("input");
  imageInput.setAttribute("placeholder", `Image url ${i}`);
  imageInput.setAttribute("name", `Image url ${i}`);
  imageInput.classList.add("input_value");
  pollForm.insertAdjacentElement("beforeend", imageInput);

  const br = document.createElement("br");
  pollForm.insertAdjacentElement("beforeend", br);
}

addNewPollOptionBtn.addEventListener("click", () => {
  for (let i = 1; i <= +totalOptions.value; i++) {
    createElements(i);
  }
});
