// Central editing file: update the brand, inbox, copy, horse profiles and image paths here.
window.SYNDICATE_CONFIG = {
  brand: { name: "Maison Thoroughbred", shortName: "Maison TB", tagline: "Ownership, elevated.", colors: { charcoal: "#111111", white: "#FFFFFF", warmWhite: "#F8F7F4", gold: "#C5A059" } },
  contact: { email: "hello@maisonthoroughbred.com", phone: "+44 (0)20 7946 0188", location: "Newmarket, Suffolk · By appointment" },
  images: { hero: "images/hero-racehorse.jpg", story: "images/story-horse.jpg", horses: ["images/horse-1.jpg", "images/horse-2.jpg", "images/horse-3.jpg"] },
  home: {
    status: "2026 Racing Season · Shares now open",
    headline: "Own the moment.<br><em>Live the race.</em>",
    intro: "A private circle of owners, exceptional Thoroughbreds and a more considered way to experience the sport we love.",
    valueTitle: "The thrill of the Thoroughbred, <em>without the noise.</em>",
    valueBody: "Maison Thoroughbred curates the bloodstock, expertise and access. You join the story with complete clarity, from first gallop to winner’s enclosure.",
    metrics: [["18+", "Stakes performers"], ["5–25%", "Flexible share tiers"], ["100%", "Transparent monthly reports"], ["VIP", "Owners’ enclosure access"]],
    steps: [
      { number: "01", title: "Meet your horse", body: "A considered shortlist of athletes chosen for pedigree, performance and potential." },
      { number: "02", title: "Choose your share", body: "Flexible 5%, 10% and 25% tiers, structured with clarity from day one." },
      { number: "03", title: "Live every race", body: "Stable access, monthly reports and the electric theatre of race day." }
    ],
    testimonials: [
      ["“It feels less like an investment and more like being invited into a world I have always admired.”", "— James W., Founder & owner"],
      ["“The transparency is exceptional. We know where the horse is, how she is progressing and what comes next.”", "— Olivia R., Maison owner"]
    ]
  },
  about: {
    eyebrow: "Heritage, reimagined",
    headline: "A more considered<br><em>way to own.</em>",
    storyTitle: "The sport we love.<br><em>The experience we believe in.</em>",
    storyBody: "Born in Newmarket and shaped by a lifelong respect for the Thoroughbred, Maison was created for people who want to feel closer to racing — not buried in its complexity.",
    mission: "To build a modern ownership community around brilliant horses, trusted expertise and the belief that every race day should feel like an occasion.",
    philosophy: ["Pedigree with purpose", "Temperament matters", "Progress over promise"]
  },
  horses: [
    { name: "Aurelia", category: "Fillies", age: "3yo filly", pedigree: "Frankel × Luna Mare", sire: "Frankel", dam: "Luna Mare", trainer: "Ralph Beckett", availability: "2 shares remaining", remaining: 20, image: 0, note: "A balanced, athletic filly with an electric turn of foot. Her first two starts have suggested a deep well of improvement." },
    { name: "Nocturne", category: "2YO Colts", age: "2yo colt", pedigree: "Dubawi × Night Garden", sire: "Dubawi", dam: "Night Garden", trainer: "Charlie Appleby", availability: "Taking reservations", remaining: 55, image: 1, note: "Beautifully bred and progressing through his early education with a calm, professional attitude." },
    { name: "Valentino", category: "In Training", age: "4yo gelding", pedigree: "Sea The Stars × Valentina", sire: "Sea The Stars", dam: "Valentina", trainer: "William Haggas", availability: "1 share remaining", remaining: 10, image: 2, note: "A proven performer with the attitude and experience to make this season his most compelling yet." }
  ],
  faqs: [
    ["How does a syndicate share work?", "You own a defined percentage of a racehorse through a simple syndicate structure. We manage the day-to-day detail and keep you close to every milestone."],
    ["Can I visit the yard?", "Yes. Owners are invited to private stable mornings and selected gallops visits by appointment."],
    ["What is included in my share?", "Your share includes the horse, training and ownership administration described in the relevant schedule, plus invitations to Maison owner experiences."]
  ]
};

(function hydrateSite() {
  const c = window.SYNDICATE_CONFIG;
  Object.entries(c.brand.colors).forEach(([key, value]) => document.documentElement.style.setProperty(`--${key.replace(/[A-Z]/g, (m) => `-${m.toLowerCase()}`)}`, value));
  document.querySelectorAll("[data-brand]").forEach((el) => { el.textContent = c.brand.name; });
  document.querySelectorAll("[data-email]").forEach((el) => { el.textContent = c.contact.email; el.href = `mailto:${c.contact.email}`; });
  document.querySelectorAll("[data-phone]").forEach((el) => { el.textContent = c.contact.phone; el.href = `tel:${c.contact.phone.replace(/\s/g, "")}`; });
  document.querySelectorAll("[data-location]").forEach((el) => { el.textContent = c.contact.location; });
  const page = document.body.dataset.page;
  if (page === "home") {
    document.querySelector("[data-status]").textContent = c.home.status;
    document.querySelector("[data-home-headline]").innerHTML = c.home.headline;
    document.querySelector("[data-home-intro]").textContent = c.home.intro;
    document.querySelector("[data-value-title]").innerHTML = c.home.valueTitle;
    document.querySelector("[data-value-body]").textContent = c.home.valueBody;
    document.querySelector("[data-hero-image]").src = c.images.hero;
    document.querySelector("[data-metrics]").innerHTML = c.home.metrics.map(([value, label]) => `<div class="metric"><strong>${value}</strong><span>${label}</span></div>`).join("");
    document.querySelector("[data-steps]").innerHTML = c.home.steps.map((step) => `<article class="editorial-card"><span class="card-number">${step.number}</span><h3>${step.title}</h3><p>${step.body}</p><span class="card-rule"></span></article>`).join("");
    document.querySelector("[data-testimonials]").innerHTML = c.home.testimonials.map(([quote, byline]) => `<blockquote><p>${quote}</p><cite>${byline}</cite></blockquote>`).join("");
    document.querySelector("[data-home-horses]").innerHTML = c.horses.slice(0, 3).map((horse) => horseCard(horse, c)).join("");
  }
  if (page === "about") {
    document.querySelector("[data-about-eyebrow]").textContent = c.about.eyebrow;
    document.querySelector("[data-about-headline]").innerHTML = c.about.headline;
    document.querySelector("[data-story-title]").innerHTML = c.about.storyTitle;
    document.querySelector("[data-story-body]").textContent = c.about.storyBody;
    document.querySelector("[data-mission]").textContent = c.about.mission;
    document.querySelector("[data-story-image]").src = c.images.story;
    document.querySelector("[data-philosophy]").innerHTML = c.about.philosophy.map((item, index) => `<li><span>0${index + 1}</span>${item}</li>`).join("");
    renderHorseGrid(c);
  }
  if (page === "contact") {
    document.querySelector("[data-faqs]").innerHTML = c.faqs.map(([question, answer]) => `<details><summary>${question}<span>+</span></summary><p>${answer}</p></details>`).join("");
    document.querySelector("[data-horse-options]").innerHTML = `<option value="">Select a horse</option>${c.horses.map((horse) => `<option>${horse.name}</option>`).join("")}<option>General ownership enquiry</option>`;
    document.querySelector("[data-contact-hero]").src = c.images.story;
  }
})();

function horseCard(horse, config) {
  return `<article class="horse-card" data-category="${horse.category}">
    <div class="horse-image-wrap"><img src="${config.images.horses[horse.image]}" alt="${horse.name}, ${horse.pedigree}" loading="lazy"><span class="availability">${horse.availability}</span></div>
    <div class="horse-card-body"><div class="horse-topline"><span>${horse.age}</span><span>${horse.category}</span></div><h3>${horse.name}</h3><p class="pedigree">${horse.pedigree}</p><p class="trainer">Trained by <strong>${horse.trainer}</strong></p><div class="share-row"><span>Share availability</span><strong>${horse.remaining}%</strong></div><div class="progress"><span style="width:${horse.remaining}%"></span></div><a class="text-link" href="contact.html?horse=${encodeURIComponent(horse.name)}">Enquire about share <span>↗</span></a></div>
  </article>`;
}

function renderHorseGrid(config) {
  const grid = document.querySelector("[data-horse-grid]");
  grid.innerHTML = config.horses.map((horse) => `${horseCard(horse, config)}<div class="horse-detail"><div><span class="eyebrow">Pedigree</span><p><strong>Sire</strong>${horse.sire}</p><p><strong>Dam</strong>${horse.dam}</p></div><div><span class="eyebrow">Trainer’s note</span><p>${horse.note}</p></div></div>`).join("");
  document.querySelectorAll("[data-filter]").forEach((button) => button.addEventListener("click", () => {
    document.querySelectorAll("[data-filter]").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    const filter = button.dataset.filter;
    document.querySelectorAll(".horse-card").forEach((card) => { card.hidden = filter !== "All" && card.dataset.category !== filter; });
    document.querySelectorAll(".horse-detail").forEach((detail) => { detail.hidden = filter !== "All" && detail.previousElementSibling.hidden; });
  }));
}
