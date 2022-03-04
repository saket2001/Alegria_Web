const quizFormDiv = document.getElementById("quiz-form");
const quizoptions = document.getElementById("optionsNumber");
const addNewQuizOptionBtn = document.getElementById("addNewQuizOptionBtn");

// this functions add one option input and one image url input in form
function createQuizele(i = 0) {
  //   option label
  const optionQ = document.createElement("p");
  optionQ.classList.add("mb-0");
  optionQ.classList.add("fs-7");
  optionQ.classList.add("main-font");
  optionQ.textContent = `Option ${i}`;
  quizFormDiv.insertAdjacentElement("beforeend", optionQ);

  //   option input
  const optionInput = document.createElement("input");
  optionInput.setAttribute("placeholder", `Option ${i} Name`);
  optionInput.setAttribute("name", `Option ${i} Name`);
  optionInput.required = true;
  optionInput.classList.add("input_value");
  quizFormDiv.insertAdjacentElement("beforeend", optionInput);

}

addNewQuizOptionBtn.addEventListener("click", () => {
  const optionQ = document.createElement("p");
  optionQ.classList.add("mb-0");
  optionQ.classList.add("fs-7");
  optionQ.classList.add("main-font");
  optionQ.textContent = `Option 1 (Correct option)`;
  quizFormDiv.insertAdjacentElement("beforeend", optionQ);

  //   option input
  const optionInput = document.createElement("input");
  optionInput.setAttribute("placeholder", `Option 1 Name (Correct option)`);
  optionInput.setAttribute("name", `Option 1 Name (Correct Option)`);
  optionInput.required = true;
  optionInput.classList.add("input_value");
  quizFormDiv.insertAdjacentElement("beforeend", optionInput);
  for (let i = 1; i < +quizoptions.value; i++) {
    createQuizele(i+1);
  }
});