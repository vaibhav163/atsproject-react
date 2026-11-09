import { Link } from "react-router-dom";
import { CITIES, SITE } from "../config.js";
import { PROJECTS, waLink } from "../data/projects.js";
import { track } from "../lib/tracking.js";

export const OPEN_COOKIE_PREFS_EVENT = "ats:open-cookie-prefs";

export default function Footer() {
  const openPrefs = () => window.dispatchEvent(new Event(OPEN_COOKIE_PREFS_EVENT));
  return (
    <>
      <footer>
        <div className="wrap">
          <div className="foot-grid">
            <div>
              <img
                className="foot-logo"
                src={SITE.logo}
                alt="ATS Group logo"
                width="132"
                height="44"
                loading="lazy"
                decoding="async"
              />
              <h3>ATS Projects — Channel Partner</h3>
              <p style={{ maxWidth: "44ch" }}>
                Residential, commercial and plotted projects by ATS Group (ATS Greens / ATS Homekraft)
                across Noida, Greater Noida and Ghaziabad. Enquiries:{" "}
                <a href={"tel:+" + SITE.phoneIntl} data-track="call_click" onClick={() => track("call_click")}>
                  {SITE.phoneDisplay}
                </a>
                .
              </p>
            </div>
            <nav aria-label="Projects by city">
              <h3>Projects by City</h3>
              <ul>
                {CITIES.map((c) => (
                  <li key={c.slug}>
                    <Link to={"/projects-in-" + c.slug}>ATS Projects in {c.name}</Link>
                  </li>
                ))}
              </ul>
            </nav>
            <nav aria-label="Site">
              <h3>Explore</h3>
              <ul>
                <li>
                  <Link to="/">Home</Link>
                </li>
                <li>
                  <Link to="/projects">All {PROJECTS.length} projects</Link>
                </li>
                <li>
                  <Link to="/about">About ATS Group</Link>
                </li>
                <li>
                  <Link to="/contact">Contact &amp; enquire</Link>
                </li>
                <li>
                  <button
                    type="button"
                    onClick={openPrefs}
                    style={{
                      background: "none",
                      border: "none",
                      padding: 0,
                      color: "var(--on-dark-muted)",
                      font: "inherit",
                      cursor: "pointer",
                    }}
                  >
                    Cookie preferences
                  </button>
                </li>
                <li>
                  <a href="/sitemap.xml">Sitemap</a> · <a href="/robots.txt">robots.txt</a>
                </li>
              </ul>
            </nav>
          </div>
          <div className="disclaimer">
            <p>
              <b>Disclaimer:</b> Authorized Channel Partner — this is not the official ATS Group website.
              This website is owned and operated by an <b>authorized channel partner</b> of ATS Group and
              is <b>not</b> the official website of ATS Group, ATS Greens or ATS Homekraft. Project names,
              images and details are shown for information only; images are representative renders and may
              differ from the actual project. Prices and availability change without notice and are
              confirmed on enquiry. RERA numbers, where shown, are as printed in project sources — please
              verify the current registration on the respective state RERA portal (e.g. up-rera.in,
              haryanarera.gov.in) and on the developer’s official website before booking. Projects shown
              without a RERA number are upcoming/coming-soon and may not yet be registered.
            </p>
            <p>© 2026 ATS Projects — Authorized Channel Partner. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Sticky mobile actions */}
      <div className="action-bar">
        <a
          className="btn small"
          href={"tel:+" + SITE.phoneIntl}
          data-track="call_click"
          onClick={() => track("call_click")}
        >
          ☎ Call now
        </a>
        <a
          className="btn small wa"
          target="_blank"
          rel="noopener"
          data-track="whatsapp_click"
          onClick={() => track("whatsapp_click")}
          href={waLink("Hi, I'm interested in an ATS Group project.")}
        >
          WhatsApp
        </a>
        <Link className="btn small on-dark" to="/contact">
          Enquire
        </Link>
      </div>
    </>
  );
}
