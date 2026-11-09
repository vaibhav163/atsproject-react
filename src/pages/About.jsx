import { useEffect } from "react";
import { Link } from "react-router-dom";
import Seo, { PAGE_SEO } from "../components/Seo.jsx";
import { SITE } from "../config.js";
import { PROJECTS } from "../data/projects.js";
import { track } from "../lib/tracking.js";

export default function About() {
  useEffect(() => {
    track("page_view", { view: "about" });
  }, []);
  return (
    <div className="wrap">
      <Seo title={PAGE_SEO.about.t} description={PAGE_SEO.about.d} path="about" />
      <nav className="crumbs" aria-label="Breadcrumb">
        <Link to="/">Home</Link>
        <span aria-hidden="true">›</span>
        <span aria-current="page">About</span>
      </nav>
      <section className="block" style={{ paddingTop: 18 }} aria-labelledby="about-h">
        <div className="two-col">
          <div>
            <h1 id="about-h" style={{ fontSize: "clamp(2rem,4.5vw,3rem)" }}>
              About ATS Group
            </h1>
            <p style={{ color: "var(--muted)", marginTop: 14 }}>
              ATS Group — through ATS Greens and its housing arm ATS Homekraft — is a Noida-headquartered
              real estate developer known for green, low-density residential communities. ATS describes its
              journey in its own words: nearly 2.5 million sq. m. of housing space delivered and 1.9 million
              sq. m. underway, 25,000+ satisfied customers and a 3,500-strong workforce with in-house
              construction, design and maintenance teams.
            </p>
            <p style={{ color: "var(--muted)", marginTop: 12 }}>
              The portfolio on this site spans {PROJECTS.length} projects across Noida, Greater Noida and Ghaziabad: flagship Noida
              residences such as Knightsbridge (Sector 124), Le Grandiose and Kingston Heath (Sector 150) and
              Picturesque Reprieves (Sector 152); Greater Noida and Yamuna Expressway projects including
              Destinaire, Rhapsody, Happy Trails and Nobility; and Ghaziabad projects including Floral
              Pathways, Homekraft NH-24 and Khyber Range; plus commercial developments like ATS Bouquet and
              Kinghood Drive, and plotted developments on the Yamuna Expressway.
            </p>
            <ul className="about-points">
              <li>
                <span>
                  <b>This website</b> is operated by an authorized channel partner of ATS Group — it is not
                  the official ATS Group website. Your enquiry comes to us, and we arrange site visits,
                  price lists and booking assistance.
                </span>
              </li>
              <li>
                <span>
                  <b>Developer’s official website:</b>{" "}
                  <a href="https://www.ats.ind.in/" target="_blank" rel="noopener">
                    ats.ind.in
                  </a>{" "}
                  — project details there prevail over anything on this site.
                </span>
              </li>
              <li>
                <span>
                  <b>Looking to buy?</b> Start with the <Link to="/projects">full project list</Link>, browse
                  by city such as <Link to="/projects-in-noida">Noida</Link> or{" "}
                  <Link to="/projects-in-ghaziabad">Ghaziabad</Link>, or <Link to="/contact">talk to us</Link>{" "}
                  about budgets and site visits.
                </span>
              </li>
            </ul>
          </div>
          <div>
            <img
              src="/assets/og-image.jpg"
              alt="ATS Group residential project"
              loading="lazy"
              decoding="async"
              style={{ borderRadius: 18, boxShadow: "var(--shadow)", width: "100%" }}
            />
            <div className="contact-cards" style={{ marginTop: 18 }}>
              <div className="contact-card">
                <h3>Talk to the channel partner desk</h3>
                <p>
                  <a
                    className="big"
                    href={"tel:+" + SITE.phoneIntl}
                    data-track="call_click"
                    onClick={() => track("call_click")}
                  >
                    {SITE.phoneDisplay}
                  </a>
                </p>
                <p>Call or WhatsApp for price lists, availability and site visits.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
