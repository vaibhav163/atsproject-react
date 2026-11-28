// SITE config — the ONLY file you need to edit for contact details,
// form keys and tracking IDs. Everything else reads from here.
export const SITE = {
  url: "https://www.atsproject.in",
  name: "ATS Projects — Authorized Channel Partner",
  builder: "ATS Group",
  phoneDisplay: "+91 87997 56026",
  phoneIntl: "918799756026",
  whatsapp: "918799756026",
  // EmailJS keys — taken from the SITE_CFG block in the atsproject.in
  // source pages (publicKey / serviceId / templateId).
  emailjs: {
    publicKey: "xLfYDZXLlR6IeQ-C6",
    serviceId: "service_fkmfynb",
    templateId: "template_bdjcyq6",
  },
  formEndpoint: "",
  // Conversion tracking — paste your real IDs to activate (trackers only
  // load after the visitor consents; events always queue to dataLayer).
  gaId: "", // e.g. "G-XXXXXXXXXX"
  googleAdsId: "", // e.g. "AW-794330788" (seen in the source site's code)
  metaPixelId: "", // e.g. "478183509607003" (seen in the source site's code)
  logo: "/assets/ats-logo.png",
  ogImage: "/assets/og-image.jpg",
  heroImage: "/images/home/slider-1.webp",
};

export const CITIES = [
  { slug: "noida", name: "Noida", img: "/images/city/projects-in-noida.webp" },
  { slug: "greater-noida", name: "Greater Noida", img: "/images/city/projects-in-greater-noida.webp" },
  { slug: "ghaziabad", name: "Ghaziabad", img: "/images/city/projects-in-ghaziabad.webp" },
  { slug: "delhi", name: "Delhi", img: "/images/city/projects-in-delhi.webp" },
  { slug: "gurugram", name: "Gurugram", img: "/images/city/projects-in-gurugram.webp" },
  { slug: "faridabad", name: "Faridabad", img: "/images/city/projects-in-faridabad.webp" },
  { slug: "sohna", name: "Sohna", img: "/images/city/projects-in-sohna.webp" },
  { slug: "mumbai", name: "Mumbai", img: "/images/city/projects-in-mumbai.webp" },
  { slug: "panipat", name: "Panipat", img: "/images/city/projects-in-panipat.webp" },
  { slug: "panchkula", name: "Panchkula", img: "/images/city/projects-in-panchkula.webp" },
  { slug: "shimla", name: "Shimla", img: "/images/city/projects-in-shimla.webp" },
  { slug: "gujarat", name: "Gujarat", img: "/images/city/projects-in-gujarat.webp" },
];

export default SITE;
