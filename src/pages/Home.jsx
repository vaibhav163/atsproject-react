import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import EnquiryForm from "../components/EnquiryForm.jsx";
import ProjectCard, { SkeletonCards } from "../components/ProjectCard.jsx";
import Seo, { PAGE_SEO } from "../components/Seo.jsx";
import { CITIES, SITE } from "../config.js";
import { PROJECTS, projectsByCity, waLink } from "../data/projects.js";
import { track } from "../lib/tracking.js";

const FEATURED = [
  "ats-knightsbridge-sector-124",
  "ats-le-grandiose-sector-150-noida-expressway",
  "ats-picturesque-reprieves-sector-152",
  "ats-homekraft-pious-hideaways-sector-150-noida-expressway",
  "ats-kingston-heath-sector-150",
  "ats-codename-hotcake-150-sector-150",
];

export default function Home() {
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    track("page_view", { view: "home" });
    const t = setTimeout(() => setLoading(false), 350);
    return () => clearTimeout(t);
  }, []);
  const featured = FEATURED.map((s) => PROJECTS.find((p) => p.slug === s)).filter(Boolean);
  const shown = featured.length ? featured : PROJECTS.slice(0, 6);

  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "RealEstateAgent",
        "@id": SITE.url + "/#business",
        name: SITE.name,
        description:
          "Authorized channel partner for ATS Group (ATS Greens & ATS Homekraft) projects across Noida, Greater Noida and Ghaziabad.",
        url: SITE.url + "/",
        logo: SITE.url + SITE.logo,
        telephone: "+91-8799756026",
        image: SITE.url + SITE.ogImage,
        areaServed: CITIES.map((c) => c.name),
        address: { "@type": "PostalAddress", addressLocality: "Noida", addressRegion: "Uttar Pradesh", addressCountry: "IN" },
      },
      { "@type": "WebSite", name: SITE.name, url: SITE.url + "/", publisher: { "@id": SITE.url + "/#business" } },
      {
        "@type": "ItemList",
        name: "ATS Group Projects",
        itemListElement: PROJECTS.map((p, i) => ({
          "@type": "ListItem",
          position: i + 1,
          name: p.name + " — " + (p.location || p.cityName),
          url: SITE.url + "/projects/" + p.slug,
        })),
      },
    ],
  };

  return (
    <>
      <Seo title={PAGE_SEO.home.t} description={PAGE_SEO.home.d} path="" jsonLd={jsonLd} />
      <section className="hero">
        <img className="hero-bg" src={SITE.heroImage} alt="" fetchPriority="high" width="1920" height="860" />
        <div className="wrap hero-in">
          <p className="eyebrow">ATS Greens · ATS Homekraft — Authorized Channel Partner</p>
          <h1>
            ATS homes, in the green <em>ATS way</em>
          </h1>
          <p className="hero-sub">
            {PROJECTS.length} ATS Group projects across {CITIES.length} cities — luxury residences, high-street
            commercial and plotted developments, with price lists, floor plans, galleries and RERA details on
            every page.
          </p>
          <div className="hero-actions">
            <Link className="btn" to="/projects">
              Browse all {PROJECTS.length} projects
            </Link>
            <a
              className="btn wa"
              target="_blank"
              rel="noopener"
              href={waLink("Hi, I'm interested in an ATS Group project. Please share options.")}
              data-track="whatsapp_click"
              onClick={() => track("whatsapp_click", { where: "hero" })}
            >
              WhatsApp us
            </a>
          </div>
          <div className="hero-stats">
            <div>
              <b>{PROJECTS.length}</b>
              <span>Projects listed</span>
            </div>
            <div>
              <b>{CITIES.length}</b>
              <span>Cities covered</span>
            </div>
            <div>
              <b>{projectsByCity("noida").length + projectsByCity("greater-noida").length}</b>
              <span>Noida + Gr. Noida projects</span>
            </div>
          </div>
        </div>
      </section>

      <section className="wrap" aria-labelledby="cities-h">
        <div className="sec-head">
          <h2 className="sec-title" id="cities-h">
            Projects by city
          </h2>
          <Link className="sec-link" to="/projects">
            View all projects →
          </Link>
        </div>
        <div className="corridors">
          {CITIES.map((c) => (
            <Link key={c.slug} className="corridor" to={"/projects-in-" + c.slug}>
              <img src={c.img} alt={"ATS projects in " + c.name} loading="lazy" decoding="async" width="640" height="420" />
              <span className="corridor-in">
                <b>{c.name}</b>
                <span>
                  {projectsByCity(c.slug).length} project{projectsByCity(c.slug).length === 1 ? "" : "s"} →
                </span>
              </span>
            </Link>
          ))}
        </div>
      </section>

      <section className="wrap" aria-labelledby="feat-h">
        <div className="sec-head">
          <h2 className="sec-title" id="feat-h">
            Featured ATS projects
          </h2>
          <Link className="sec-link" to="/projects">
            All projects →
          </Link>
        </div>
        <div className="grid" aria-busy={loading}>
          {loading ? <SkeletonCards n={6} /> : shown.map((p) => <ProjectCard key={p.slug} p={p} />)}
        </div>
      </section>

      <section className="wrap two-col" aria-labelledby="why-h">
        <div>
          <h2 className="sec-title" id="why-h">
            Why buyers choose ATS
          </h2>
          <p className="detail-desc">
            Since 1998, ATS Group has built its name on one promise — homes set in green surroundings, with
            Spanish-inspired and contemporary architecture, in-house construction and on-time delivery. From
            ATS Greens’ flagship residences in Noida’s Sector 150 and 152 to ATS Homekraft’s new launches
            across NCR, every project on this site links to its price list, plans and RERA registration where
            available.
          </p>
          <ul className="about-points">
            <li>🌳 Low-density, green-first communities — the original “ATS advantage”</li>
            <li>🏛️ In-house construction, design and maintenance teams</li>
            <li>🛡️ RERA numbers shown per project, exactly as published — verify before you book</li>
            <li>📞 One desk for all {PROJECTS.length} projects: price lists, site visits, booking support</li>
          </ul>
        </div>
        <EnquiryForm heading="Request a callback" />
      </section>
    </>
  );
}
