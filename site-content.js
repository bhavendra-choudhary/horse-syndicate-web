// Edit this file to update the brand, copy, colors, inbox and imagery site-wide.
window.SYNDICATE_CONFIG = {
  brand: {
    name: "Maison Thoroughbred",
    shortName: "Maison TB",
    tagline: "Ownership, elevated.",
    colors: {
      charcoal: "#111111",
      white: "#FFFFFF",
      warmWhite: "#F8F7F4",
      gold: "#C5A059"
    }
  },
  contact: {
    email: "hello@maisonthoroughbred.com",
    phone: "+44 (0)20 7946 0188"
  },
  images: {
    hero: "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=1600&q=80",
    story: "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?auto=format&fit=crop&w=1000&q=80",
    horses: [
      "https://images.unsplash.com/photo-1598974357801-cbca100e65d3?auto=format&fit=crop&w=1000&q=80",
      "https://images.unsplash.com/photo-1553284965-83fd3e82fa5a?auto=format&fit=crop&w=1000&q=80",
      "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=1600&q=80"
    ]
  },
  home: {
    eyebrow: "A new standard in shared ownership",
    headline: "Own the moment.<br><em>Live the race.</em>",
    intro: "Maison Thoroughbred makes racehorse ownership beautifully simple. Curated horses, exceptional trainers, and a considered experience for a select circle of owners.",
    valueTitle: "The thrill of the thoroughbred, <em>without the noise.</em>",
    valueBody: "We bring together the sport’s rarest ingredients and make them accessible through thoughtfully structured syndicates. Every detail is handled, from bloodstock to race day.",
    steps: [
      { number: "01", title: "Choose your horse", body: "Meet our hand-picked shortlist of athletes selected for talent, temperament and potential." },
      { number: "02", title: "Secure your share", body: "Join with a transparent, straightforward share designed around your ambitions." },
      { number: "03", title: "Experience every win", body: "Enjoy exclusive stable access, owner updates and unforgettable days at the races." }
    ]
  },
  about: {
    eyebrow: "The Maison Thoroughbred story",
    headline: "A more considered<br><em>way to own.</em>",
    storyTitle: "The sport we love.<br><em>The experience we believe in.</em>",
    storyBody: "Founded by people who live and breathe the racing world, Maison Thoroughbred exists to make the magic of ownership more personal, more transparent and more beautifully done.",
    mission: "To build a modern ownership community around brilliant horses, trusted expertise and the belief that every race day should feel like an occasion."
  },
  horses: [
    { name: "Aurelia", age: "3yo filly", pedigree: "Frankel — Luna Mare", trainer: "Ralph Beckett", availability: "2 shares left", image: 0 },
    { name: "Nocturne", age: "2yo colt", pedigree: "Dubawi — Night Garden", trainer: "Charlie Appleby", availability: "Taking reservations", image: 1 },
    { name: "Valentino", age: "4yo gelding", pedigree: "Sea The Stars — Valentina", trainer: "William Haggas", availability: "1 share left", image: 2 }
  ]
};

(function hydrateSite() {
  const c = window.SYNDICATE_CONFIG;
  document.documentElement.style.setProperty("--charcoal", c.brand.colors.charcoal);
  document.documentElement.style.setProperty("--white", c.brand.colors.white);
  document.documentElement.style.setProperty("--warm-white", c.brand.colors.warmWhite);
  document.documentElement.style.setProperty("--gold", c.brand.colors.gold);
  document.querySelectorAll("[data-brand]").forEach((el) => { el.textContent = c.brand.name; });
  document.querySelectorAll("[data-email]").forEach((el) => { el.textContent = c.contact.email; el.href = `mailto:${c.contact.email}`; });
  document.querySelectorAll("[data-phone]").forEach((el) => { el.textContent = c.contact.phone; el.href = `tel:${c.contact.phone.replace(/\s/g, "")}`; });

  const page = document.body.dataset.page;
  if (page === "home") {
    document.querySelector("[data-home-eyebrow]").textContent = c.home.eyebrow;
    document.querySelector("[data-home-headline]").innerHTML = c.home.headline;
    document.querySelector("[data-home-intro]").textContent = c.home.intro;
    document.querySelector("[data-value-title]").innerHTML = c.home.valueTitle;
    document.querySelector("[data-value-body]").textContent = c.home.valueBody;
    document.querySelector("[data-hero-image]").src = c.images.hero;
    c.home.steps.forEach((step, index) => {
      const card = document.querySelectorAll("[data-step]")[index];
      if (!card) return;
      card.querySelector(".step-number").textContent = step.number;
      card.querySelector("h3").textContent = step.title;
      card.querySelector("p").textContent = step.body;
    });
  }
  if (page === "about") {
    document.querySelector("[data-about-eyebrow]").textContent = c.about.eyebrow;
    document.querySelector("[data-about-headline]").innerHTML = c.about.headline;
    document.querySelector("[data-story-title]").innerHTML = c.about.storyTitle;
    document.querySelector("[data-story-body]").textContent = c.about.storyBody;
    document.querySelector("[data-mission]").textContent = c.about.mission;
    document.querySelector("[data-story-image]").src = c.images.story;
    document.querySelector("[data-horse-grid]").innerHTML = c.horses.map((horse) => `
      <article class="horse-card">
        <div class="horse-image-wrap"><img src="${c.images.horses[horse.image]}" alt="${horse.name}, ${horse.pedigree}" loading="lazy"><span class="availability">${horse.availability}</span></div>
        <div class="horse-card-body"><p class="eyebrow">${horse.age}</p><h3>${horse.name}</h3><p class="pedigree">${horse.pedigree}</p><p class="trainer">Trained by ${horse.trainer}</p><a class="text-link" href="contact.html?horse=${encodeURIComponent(horse.name)}">Enquire about this horse <span>↗</span></a></div>
      </article>`).join("");
  }
})();
