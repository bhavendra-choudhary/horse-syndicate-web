// Central editing file: update the brand, inbox, copy, horse profiles and image paths here.
window.SYNDICATE_CONFIG = {
  brand: { name: "Vanguard Thoroughbreds", shortName: "Vanguard TB", tagline: "Command the rail. Own the legacy.", colors: { charcoal: "#111111", white: "#FFFFFF", warmWhite: "#F8F7F4", gold: "#C5A059" } },
  contact: { email: "concierge@vanguardthoroughbreds.com", phone: "+1 (859) 555-0194", location: "Lexington, Kentucky · Saratoga Springs (by appointment)" },
  images: { hero: "images/hero-racehorse.jpg", story: "images/story-horse.jpg", horses: ["images/horse-1.jpg", "images/horse-2.jpg", "images/horse-3.jpg"] },
  home: {
    status: "2026 Keeneland & Saratoga acquisitions open",
    headline: "Command the Rail.<br><em>Own the Legacy.</em>",
    intro: "Direct fractional ownership in elite Grade-1 caliber Thoroughbreds. Curated bloodlines, Hall-of-Fame trainers, and full paddock-to-winner's-circle access.",
    valueTitle: "Championship Pedigrees.<br><em>Institutional Transparency.</em>",
    valueBody: "Vanguard Thoroughbreds gives a select circle of partners direct access to elite bloodstock, disciplined reporting and the moments that define a racing legacy.",
    metrics: [["18+", "Stakes performers"], ["5–25%", "Flexible share tiers"], ["100%", "Transparent monthly reports"], ["VIP", "Owners’ enclosure access"]],
    steps: [
      { number: "01", title: "Select the bloodline", body: "Review a disciplined shortlist of Grade-1 caliber athletes selected for pedigree, athleticism and upside." },
      { number: "02", title: "Define your equity", body: "Choose a transparent 5%, 10% or 25% ownership position with economics understood upfront." },
      { number: "03", title: "Enter the circle", body: "Receive every training report, paddock invitation and race-day access from first work to winner's circle." }
    ],
    testimonials: [
      ["“Vanguard delivers the rare combination of elite access and institutional-level reporting. Every decision is made with conviction.”", "— James W., Founding Partner"],
      ["“The bloodstock is exceptional, but the discipline around ownership is what sets this syndicate apart.”", "— Olivia R., Vanguard Partner"]
    ]
  },
  about: {
    eyebrow: "Heritage, reimagined",
    headline: "Built for the<br><em>Pursuit of Classic Glory.</em>",
    storyTitle: "American racing heritage.<br><em>Modern ownership discipline.</em>",
    storyBody: "Vanguard was built for partners who expect more from Thoroughbred ownership: uncommon bloodlines, respected trainers, precise communication and a seat inside the sport's defining moments.",
    mission: "To compound the power of elite American racing through disciplined bloodstock selection, clear economics and a true owner's proximity to the horse.",
    philosophy: ["Pedigree with purpose", "Athleticism under pressure", "Performance over promise"]
  },
  horses: [
    { name: "Aurelia", category: "Fillies", age: "3yo filly", pedigree: "Into Mischief × Golden Hour", sire: "Into Mischief", dam: "Golden Hour", trainer: "Brad H. Cox", circuit: "Keeneland / Saratoga", availability: "Only 15% remaining", remaining: 15, image: 0, note: "An athletic filly with a sharp turn of foot and the composure to thrive on the biggest American stages." },
    { name: "Nocturne", category: "2YO Colts", age: "2yo colt", pedigree: "Curlin × Midnight Bloom", sire: "Curlin", dam: "Midnight Bloom", trainer: "Todd A. Pletcher", circuit: "Belmont / Saratoga", availability: "Only 25% remaining", remaining: 25, image: 1, note: "A deep-bodied colt with a professional mind, scope to develop and a pedigree built for classic distance." },
    { name: "Valentino", category: "In Training", age: "4yo colt", pedigree: "Quality Road × Valentina", sire: "Quality Road", dam: "Valentina", trainer: "Chad C. Brown", circuit: "Santa Anita / Keeneland", availability: "Only 10% remaining", remaining: 10, image: 2, note: "A proven performer with tactical speed, polished racecraft and an appetite for championship company." }
  ],
  faqs: [
    ["How does a syndicate share work?", "You own a defined percentage of a racehorse through a simple syndicate structure. We manage the day-to-day detail and keep you close to every milestone."],
    ["Can I visit the yard?", "Yes. Owners are invited to private stable mornings and selected gallops visits by appointment."],
    ["What is included in my share?", "Your share includes the horse, training and ownership administration described in the relevant schedule, plus invitations to Vanguard partner experiences."]
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
    <div class="horse-image-wrap"><img src="${config.images.horses[horse.image]}" alt="${horse.name}, ${horse.pedigree}" loading="eager"><span class="availability">${horse.availability}</span></div>
    <div class="horse-card-body"><div class="horse-topline"><span>${horse.age}</span><span>${horse.category}</span></div><h3>${horse.name}</h3><div class="pedigree-grid"><span><b>Sire</b>${horse.sire}</span><span><b>Dam</b>${horse.dam}</span><span><b>Trainer</b>${horse.trainer}</span><span><b>Target circuit</b>${horse.circuit}</span></div><div class="share-row"><span>Share availability</span><strong>${horse.remaining}%</strong></div><div class="progress"><span style="width:${horse.remaining}%"></span></div><a class="button dark card-button" href="contact.html?horse=${encodeURIComponent(horse.name)}">Enquire about share <span>↗</span></a></div>
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
