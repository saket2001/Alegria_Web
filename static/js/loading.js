// hides loader
window.onload = (e) => {
  document.querySelector(".loading-bg").classList.add("hide");
  document.querySelector(".loader").classList.add("hide");
  document.querySelector("#loader-logo").classList.add("hide");
  document.querySelector(".loader-body").style.height = "auto";
  document.querySelector(".loader-body").style.overflow = "auto";
};

// fallback
setTimeout(() => {
  document.querySelector(".loading-bg").classList.add("hide");
  document.querySelector(".loader").classList.add("hide");
  document.querySelector(".loader-body").style.height = "auto";
  document.querySelector(".loader-body").style.overflow = "auto";
}, 10000);
