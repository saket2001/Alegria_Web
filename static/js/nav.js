const mobileNav = document.querySelector("#mobile-nav");
const desktopNav = document.querySelector("#desktop-nav");
const navBtn = document.getElementById("nav-toggler");

navBtn.addEventListener("click", () => {
  if (mobileNav.classList.contains("hidden"))
    mobileNav.classList.toggle("hidden");
  else mobileNav.classList.toggle("hidden");
});
