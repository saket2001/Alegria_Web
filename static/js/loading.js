// hides loader
window.onload = (e) => {
  document.querySelector(".loading-bg").classList.add("hide");
  document.querySelector(".loader").classList.add("hide");
};

// fallback
setTimeout(() => {
  document.querySelector(".loading-bg").classList.add("hide");
  document.querySelector(".loader").classList.add("hide");
}, 15000);
