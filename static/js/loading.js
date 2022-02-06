// hides loader
window.onload = (e) => {
  document.querySelector(".loading-bg").classList.add("hide");
  document.querySelector(".wrapper").classList.add("hide");
};

// fallback
setTimeout(() => {
  document.querySelector(".loading-bg").classList.add("hide");
  document.querySelector(".wrapper").classList.add("hide");
}, 10000);
