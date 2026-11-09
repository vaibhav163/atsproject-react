import { useEffect } from "react";
import { SITE } from "../config.js";

// Per-page SEO — the React equivalent of the static site's setMeta() plus
// the JSON-LD each static page carried in its head. Sets the page title,
// meta description, canonical, Open Graph and Twitter tags, and (optionally)
// a page-specific JSON-LD block (used for the project BreadcrumbList).
function upsertMeta(selector, attrs) {
  let el = document.head.querySelector(selector);
  if (!el) {
    el = document.createElement(selector.startsWith("link") ? "link" : "meta");
    document.head.appendChild(el);
  }
  Object.entries(attrs).forEach(([k, v]) => el.setAttribute(k, v));
  return el;
}

export default function Seo({ title, description, path = "", image, jsonLd }) {
  useEffect(() => {
    const url = SITE.url + "/" + (path || "");
    const img = SITE.url + "/" + String(image || SITE.ogImage).replace(/^\//, "");
    document.title = title;
    upsertMeta('meta[name="description"]', { name: "description", content: description });
    upsertMeta('link[rel="canonical"]', { rel: "canonical", href: url });
    upsertMeta('meta[property="og:title"]', { property: "og:title", content: title });
    upsertMeta('meta[property="og:description"]', { property: "og:description", content: description });
    upsertMeta('meta[property="og:url"]', { property: "og:url", content: url });
    upsertMeta('meta[property="og:image"]', { property: "og:image", content: img });
    upsertMeta('meta[name="twitter:title"]', { name: "twitter:title", content: title });
    upsertMeta('meta[name="twitter:description"]', { name: "twitter:description", content: description });
    upsertMeta('meta[name="twitter:image"]', { name: "twitter:image", content: img });

    let script = null;
    if (jsonLd) {
      script = document.createElement("script");
      script.type = "application/ld+json";
      script.id = "crumbLd";
      script.textContent = JSON.stringify(jsonLd);
      document.head.appendChild(script);
    }
    return () => {
      if (script) script.remove();
    };
  }, [title, description, path, image, jsonLd]);
  return null;
}

// The per-page SEO values for the main (non-project) pages.
export const PAGE_SEO = {
  home: {
    t: "ATS Projects in Noida, Greater Noida & Ghaziabad | Authorized Channel Partner",
    d: "Explore 30 ATS Group projects — ATS Knightsbridge, Le Grandiose, Picturesque Reprieves, Pious Hideaways, Destinaire, Happy Trails and more across Noida, Greater Noida and Ghaziabad. Call +91 87997 56026.",
  },
  projects: {
    t: "All ATS Group Projects — Noida, Greater Noida & Ghaziabad",
    d: "Browse all 30 ATS Group (ATS Greens & ATS Homekraft) projects: luxury residences, commercial spaces and plots across Noida, Greater Noida and Ghaziabad. Prices, floor plans, galleries and RERA details. Call +91 87997 56026.",
  },
  about: {
    t: "About ATS Group | ATS Greens & ATS Homekraft — Channel Partner",
    d: "ATS Group (ATS Greens, founded 1998) is a Noida-based developer known for green, low-density residential communities delivered across NCR. Learn about the portfolio and this channel-partner website.",
  },
  contact: {
    t: "Enquire — ATS Group Projects | Call +91 87997 56026",
    d: "Enquire about any ATS Group project: price lists, availability, site visits and booking assistance from the authorized channel partner desk. Call or WhatsApp +91 87997 56026.",
  },
  notfound: {
    t: "Page Not Found (404) | ATS Projects — Authorized Channel Partner",
    d: "The page you requested could not be found. Browse all ATS Group projects in Noida, Greater Noida and Ghaziabad instead.",
  },
};
