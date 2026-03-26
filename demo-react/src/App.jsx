import React, { useMemo, useState } from "react";
import ChatwootWidget from "./ChatwootWidget.jsx";

const N8N_BASE = "http://localhost:5678";
const BASIC_USER = "admin";
const BASIC_PASS = "admin";

const products = [
  {
    id: "zombie-guppy",
    emoji: "🧟",
    name: "Zombie Guppy Deluxe",
    price: "299 kr",
    tag: "B2B lobbyfavorit",
    blurb: "En död guppy med aggressivt premiumförpackad stillhet. Bäst i receptioner där ingen vill ha överraskningar.",
    useCase: "Bulkorder till hotell, coworkingyta eller event.",
    starterLead:
      "Hej! Vi driver ett coworkingkontor i Malmö och vill beställa 24 Zombie Guppy Deluxe till reception och mötesrum. Kan ni skicka offert, leveranstid och om ni har volympris?",
  },
  {
    id: "resurrection-addon",
    emoji: "⚡",
    name: "Återupplivning Plus",
    price: "149 kr",
    tag: "Upsell / addon",
    blurb: "Valfritt tillägg för kunder som ångrar att fisken är för död. Ger hopp, inte garantier.",
    useCase: "Merförsäljning till kunder som redan köpt fisk.",
    starterLead:
      "Hej! Vi säljer Bosses akvariefiskar vidare i presentbutik och undrar om vi kan lägga till Återupplivning Plus som upsell i kassan. Har ni partnerpris?",
  },
  {
    id: "time-machine",
    emoji: "⏳",
    name: "Tidsmaskin Experience Pack",
    price: "899 kr",
    tag: "Premiumupplevelse",
    blurb: "Se fisken i ett tidigare, mer levande tillstånd. Perfekt för kunder som vill ha nostalgi som tjänst.",
    useCase: "Premium lead eller PR-vinklad förfrågan.",
    starterLead:
      "Hej! Vi jobbar på ett upplevelsecenter och vill testa ert Tidsmaskin Experience Pack som premiumprodukt i vår souvenirshop. Kan ni berätta hur det funkar och vad som ingår?",
  },
  {
    id: "stillhet-subscription",
    emoji: "📦",
    name: "Månadens Mystiskt Orörliga Fisk",
    price: "199 kr / man",
    tag: "Retention / abonnemang",
    blurb: "Prenumeration för kunder som vill bli överraskade av en ny akvatisk tragedi varje månad.",
    useCase: "Retention, abonnemang och lojalitetsflöden.",
    starterLead:
      "Hej! Vi driver en absurd presentbox-tjänst och vill paketera Månadens Mystiskt Orörliga Fisk som prenumeration. Går det att få white label-upplägg?",
  },
];

const flowHighlights = [
  {
    title: "Use case 1: bulk lead",
    blurb:
      "Hotellkedja vill ha 40 Zombie Guppy Deluxe till lobbyer i tre städer.",
    outcome:
      "Flowise ska markera bulk_order, föreslå produkt och ge säljteamet en kort sammanfattning.",
  },
  {
    title: "Use case 2: merförsäljning",
    blurb:
      "Kund har redan köpt fiskar och undrar om Återupplivning Plus kan läggas till i efterhand.",
    outcome:
      "Flowise ska kategorisera addon_question och visa varför det är ett upsell-läge, inte ett supportärende.",
  },
  {
    title: "Use case 3: support / eskalering",
    blurb:
      "Kunden skriver att fisken fortfarande inte rör sig trots återupplivningspaket och tidsmaskin.",
    outcome:
      "Flowise ska svara artigt, klassificera supporttyp och föreslå eskalering vid behov.",
  },
  {
    title: "Use case 4: press / PR",
    blurb:
      "En influencer eller journalist vill göra reportage om död fisk som premiumupplevelse.",
    outcome:
      "Flowise ska skilja press_or_partnership från vanlig säljförfrågan.",
  },
];

const supportExamples = [
  {
    id: "still-dead",
    label: "Fisken är fortfarande död",
    message:
      "Hej support! Vi köpte 3 Zombie Guppy Deluxe med Återupplivning Plus men de är fortfarande helt orörliga efter 48 timmar. Är detta normalt eller ska vi eskalera till nivå 2?",
  },
  {
    id: "time-machine-refund",
    label: "Tidsmaskinen visar fel fisk",
    message:
      "Hej! Tidsmaskin Experience Pack visar en helt annan fisk än den vi köpte. Hur reklamerar man ett tidsparadox-relaterat fel?",
  },
  {
    id: "subscription-confusion",
    label: "Prenumerationsfråga",
    message:
      "Hej! Vi fick två exemplar av Månadens Mystiskt Orörliga Fisk samma vecka. Är det en bonus eller ett lagerfel?",
  },
  {
    id: "chatwoot-style",
    label: "Kort chattfråga",
    message:
      "Varför rör sig inte min fisk alls? Jag tog ju premium.",
  },
];

function authHeader() {
  return `Basic ${btoa(`${BASIC_USER}:${BASIC_PASS}`)}`;
}

async function postToN8n(path, body) {
  const res = await fetch(`${N8N_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: authHeader(),
    },
    body: JSON.stringify(body),
  });

  const text = await res.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = text;
  }

  return { ok: res.ok, status: res.status, body: parsed };
}

export default function App() {
  const defaultLeadMessage = useMemo(
    () =>
      "Hej! Vi driver ett litet hotell i Göteborg och vill beställa 12 Zombie Guppy Deluxe till receptionen. Kan ni skicka offert, leveranstid och om Återupplivning Plus går att lägga till senare?",
    [],
  );

  const [leadForm, setLeadForm] = useState({
    name: "Bosse Backström",
    email: "bosse@vattenvision.se",
    message: defaultLeadMessage,
  });
  const [supportMessage, setSupportMessage] = useState(
    "Hej support! Vi köpte Återupplivning Plus till en Zombie Guppy Deluxe men fisken har fortfarande noll energi. Vad är nästa steg?",
  );

  const [leadResult, setLeadResult] = useState(null);
  const [supportResult, setSupportResult] = useState(null);
  const [leadStatus, setLeadStatus] = useState("idle");
  const [supportStatus, setSupportStatus] = useState("idle");

  const useProductForLead = (product) => {
    setLeadForm((current) => ({
      ...current,
      message: product.starterLead,
    }));
  };

  const submitLead = async (event) => {
    event.preventDefault();
    setLeadStatus("loading");
    setLeadResult(null);
    try {
      const result = await postToN8n("/webhook/lead", leadForm);
      setLeadResult(result);
      setLeadStatus(result.ok ? "ok" : "error");
    } catch (error) {
      setLeadStatus("error");
      setLeadResult({
        ok: false,
        status: 0,
        body: String(error),
      });
    }
  };

  const submitSupport = async (event) => {
    event.preventDefault();
    setSupportStatus("loading");
    setSupportResult(null);
    try {
      const result = await postToN8n("/webhook/support", { message: supportMessage });
      setSupportResult(result);
      setSupportStatus(result.ok ? "ok" : "error");
    } catch (error) {
      setSupportStatus("error");
      setSupportResult({
        ok: false,
        status: 0,
        body: String(error),
      });
    }
  };

  const chatwootConfigured =
    Boolean(import.meta.env.VITE_CHATWOOT_BASE_URL) &&
    Boolean(import.meta.env.VITE_CHATWOOT_WEBSITE_TOKEN);

  return (
    <div className="page">
      <ChatwootWidget />
      <header className="hero">
        <p className="eyebrow">BOSSES AKVARIEFISKAR · REACT SHOP DEMO</p>
        <h1>Död fisk, tidsmaskiner och ett CRM-flöde som faktiskt är begripligt</h1>
        <p>
          Den här butiken är byggd för kurscaset <strong>Bosses Akvariefiskar</strong>. Leads och
          supportfrågor skickas direkt till n8n-webhooks för demo av ert AI + CRM-flöde med
          <strong>Bosses absurda produkter</strong> som röd tråd genom hela stacken.
        </p>
        <div className="meta-row">
          <span>Lead: /webhook/lead</span>
          <span>Support: /webhook/support</span>
          <span>Chatwoot: /webhook/chatwoot</span>
          <span>Auth: admin/admin</span>
        </div>
      </header>

      <section className="story-grid" aria-label="Varför just det här caset">
        {flowHighlights.map((item) => (
          <article key={item.title} className="story-card">
            <h2>{item.title}</h2>
            <p>{item.blurb}</p>
            <p className="story-outcome">{item.outcome}</p>
          </article>
        ))}
      </section>

      <section className="products-grid" aria-label="Roliga produkter">
        {products.map((product) => (
          <article key={product.id} className="product-card">
            <div className="emoji" aria-hidden="true">
              {product.emoji}
            </div>
            <span className="tag">{product.tag}</span>
            <h2>{product.name}</h2>
            <p className="price">{product.price}</p>
            <p className="blurb">{product.blurb}</p>
            <p className="use-case">{product.useCase}</p>
            <button type="button" onClick={() => useProductForLead(product)}>
              Fyll lead med detta case
            </button>
          </article>
        ))}
      </section>

      <section className="forms-grid">
        <article className="panel">
          <h3>Lead capture for Bosses Akvariefiskar</h3>
          <p className="panel-intro">
            Testa bulkorder, partnerfråga, premiumprodukt eller upsell. Resultatet ska sedan
            klassificeras i n8n och Flowise.
          </p>
          <form onSubmit={submitLead}>
            <label>
              Namn
              <input
                value={leadForm.name}
                onChange={(e) => setLeadForm((f) => ({ ...f, name: e.target.value }))}
                required
              />
            </label>
            <label>
              E-post
              <input
                type="email"
                value={leadForm.email}
                onChange={(e) => setLeadForm((f) => ({ ...f, email: e.target.value }))}
                required
              />
            </label>
            <label>
              Meddelande
              <textarea
                value={leadForm.message}
                onChange={(e) => setLeadForm((f) => ({ ...f, message: e.target.value }))}
                required
              />
            </label>
            <button disabled={leadStatus === "loading"} type="submit">
              {leadStatus === "loading" ? "Skickar..." : "Skicka lead"}
            </button>
          </form>
          <p className={`status ${leadStatus === "ok" ? "ok" : leadStatus === "error" ? "error" : ""}`}>
            {leadStatus === "idle" && ""}
            {leadStatus === "ok" && "Lead skickat"}
            {leadStatus === "error" && "Något gick fel"}
            {leadStatus === "loading" && "Skickar till n8n..."}
          </p>
          {leadResult && <pre>{JSON.stringify(leadResult, null, 2)}</pre>}
        </article>

        <article className="panel">
          <h3>Support / Chatwoot-liknande frågor</h3>
          <p className="panel-intro">
            Formuläret nedan skickar direkt till n8n <code>/webhook/support</code> (samma AI-steg som
            labbet, men <strong>inte</strong> via Chatwoot). För riktig chatt mot Chatwoot: skapa en
            <strong> Website</strong>-inbox i Chatwoot, kopiera <em>website token</em>, sätt{" "}
            <code>VITE_CHATWOOT_BASE_URL</code> (t.ex. <code>http://localhost:3001</code>) och{" "}
            <code>VITE_CHATWOOT_WEBSITE_TOKEN</code> i miljön och starta om React-demon — då visas
            Chatwoots widget här. Koppla sedan Chatwoots webhook till n8n enligt README.
          </p>
          {!chatwootConfigured && (
            <p className="panel-hint">
              Widget ej aktiv: lägg till Vite-variablerna ovan (se <code>demo-react/.env.example</code>
              ).
            </p>
          )}
          <div className="example-buttons" aria-label="Supportexempel">
            {supportExamples.map((example) => (
              <button
                key={example.id}
                className="ghost-button"
                type="button"
                onClick={() => setSupportMessage(example.message)}
              >
                {example.label}
              </button>
            ))}
          </div>
          <form onSubmit={submitSupport}>
            <label>
              Fråga
              <textarea
                value={supportMessage}
                onChange={(e) => setSupportMessage(e.target.value)}
                required
              />
            </label>
            <button disabled={supportStatus === "loading"} type="submit">
              {supportStatus === "loading" ? "Skickar..." : "Skicka support"}
            </button>
          </form>
          <p
            className={`status ${
              supportStatus === "ok" ? "ok" : supportStatus === "error" ? "error" : ""
            }`}
          >
            {supportStatus === "idle" && ""}
            {supportStatus === "ok" && "Supportfråga skickad"}
            {supportStatus === "error" && "Något gick fel"}
            {supportStatus === "loading" && "Skickar till n8n..."}
          </p>
          {supportResult && <pre>{JSON.stringify(supportResult, null, 2)}</pre>}
        </article>
      </section>
    </div>
  );
}
