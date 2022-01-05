let controller = new ScrollMagic.Controller();
const t1 = new TimelineMax();
const t2 = new TimelineMax();
const t3 = new TimelineMax();
const t4 = new TimelineMax();

t1.fromTo(".bg", { y: -100 }, { y: 0, duration: 3 })
  .to(".mountains", 3, { y: -300 }, "-=3")
  .to(".land", 3, { y: -400 }, "-=3")
  .to(".title", 3, { y: -600, opacity: 0 }, "-=3")
  .to(".about_us", 3, { top: "0%" }, "-=3")
  .fromTo(
    ".about_img",
    { y: 200, opacity: 0 },
    { y: 0, opacity: 1, duration: 3 },
    "-=3"
  )
  .fromTo(
    ".about_text",
    { y: 200, opacity: 0 },
    { y: 0, opacity: 1, duration: 3 },
    "-=3"
  );

let scene1 = new ScrollMagic.Scene({
  triggerElement: ".parallax_section",
  duration: "300%",
  triggerHook: 0,
})
  .setTween(t1)
  .setPin(".parallax_section")
  .addTo(controller);

//

t2.fromTo(
  "#events-section",
  { y: "90px", opacity: 0 },
  { y: "0px", opacity: 1, duration: 2 }
);

const scene2 = new ScrollMagic.Scene({
  triggerElement: "#events-section",
})
  .setTween(t2)
  .addTo(controller);

//

t3.fromTo(
  "#hackathon-title",
  { y: "50px", opacity: 0.2 },
  { y: "0px", opacity: 1, duration: 2 }
)
  .fromTo(
    ".hackathon-content",
    { y: "50px", opacity: 0.2 },
    { y: "0px", opacity: 1, duration: 2 },
    "-=2"
  )
  .fromTo(
    ".hackathon-image",
    { y: "50px", opacity: 0 },
    { y: "0px", opacity: 1, duration: 2 },
    "-=2"
  )
  .fromTo(
    ".hackathon-prize",
    { y: "50px", opacity: 0 },
    { y: "0px", opacity: 1, duration: 2 },
    "-=2"
  );

const scene3 = new ScrollMagic.Scene({
  triggerElement: ".hackathon",
})
  .setTween(t3)
  .addTo(controller);

//
t4.fromTo(
  "#gallery-image1",
  { y: "50px", opacity: 0 },
  { y: "0px", opacity: 1, duration: 1 }
).fromTo(
  ".gallery-image",
  { y: "50px", opacity: 0 },
  { y: "0px", opacity: 1, duration: 1 },
  "-=1"
);

const scene4 = new ScrollMagic.Scene({
  triggerElement: "#gallery",
})
  .setTween(t4)
  .addTo(controller);
