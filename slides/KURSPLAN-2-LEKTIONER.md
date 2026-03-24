# Kursplan: AI, automation och CRM-flöden (2 x 90 min)

Det här upplägget bygger vidare på tidigare arbete med Zapier, men flyttar fokus från enskilda verktyg till hur en modern automationskedja faktiskt hänger ihop. Materialet är tänkt att delas med studenterna som stöd före, under och efter kursen.

## Målgrupp

Studenter och marknadsförare utan djup teknisk bakgrund, men med behov av att förstå hur formulär, AI, CRM och integrationsflöden samverkar i praktiken.

## Övergripande mål

Efter kursens två lektioner ska deltagarna kunna:

- beskriva hur ett affärsflöde går från insamling till uppföljning
- förstå vilken tjänst som gör vad i vår demo-stack
- känna igen vanliga felbilder i integrationer
- koppla teknikval till affärsnytta, svarstid och datakvalitet
- resonera om när AI tillför värde i ett flöde och när det mest skapar brus

## Varför kursen är upplagd i två lektioner

Vi har valt två lektioner för att skapa en tydlig progression:

- **Lektion 1** ger helhetsbilden: historik, begrepp, arkitektur, tjänster och huvudflöde.
- **Lektion 2** fokuserar på tillämpning: problemformulering, felsökning, exempel och hur samma arkitektur kan användas i flera typer av flöden.

Det gör att deltagarna först får ett språk för att förstå kedjan, och därefter verktyg för att läsa, testa och resonera om den.

## Varför vi har valt just dessa delar

- Vi bygger vidare på **Zapier-logik** eftersom deltagarna redan känner igen trigger, action, fältmappning och skillnaden mellan polling och webhook.
- Vi visar en **sammanhängande stack** i stället för många lösa verktyg, för att göra ansvarsfördelningen tydlig.
- Vi utgår från **problem före exempel** så att varje demo har ett affärsmässigt sammanhang.
- Vi prioriterar **förståelse framför full implementation**. Målet är inte att alla ska kunna sätta upp allt själva från grunden, utan att förstå hur delarna samverkar.
- Eftersom upplägget är för **distans** tonar vi ned parövningar och lägger mer vikt vid visuella diagram, gemensam genomgång och egen testning.

## Delar vi medvetet tonar ned

- djup programmering och större mängder egen kod
- avancerad drift, säkerhet och produktionshärdning
- många parallella sidoflöden som riskerar att splittra fokus
- övningar där studenter måste sitta fysiskt tillsammans för att få ut värde

## Förslag på upplägg

## Lektion 1 (90 min)

**Tema:** Från Zapier-tänk till en egen AI + CRM-stack

| Del | Tid | Innehåll | Varför |
|-----|-----|----------|--------|
| Introduktion och mål | 10 min | Vad kursen handlar om och vad deltagarna ska kunna efter två lektioner. | Skapar förväntansbild och ramar in kursen affärsmässigt. |
| Repetition från tidigare lektioner | 15 min | Trigger/action, fältmappning, polling vs webhook, Zapier-logik. | Sänker tröskeln genom att starta i något deltagarna redan känner igen. |
| Historik och översikt | 10 min | CSV -> ETL -> iPaaS -> AI + API. | Visar att dagens lösningar är en fortsättning på äldre arbetssätt, inte ett helt nytt universum. |
| Vår stack och ansvarsfördelning | 20 min | React/formulär, n8n, Flowise, Twenty, Chatwoot, Docker Compose. | Gör det tydligt vilket område som ägs av vilken tjänst. |
| Kundresa och arkitektur | 15 min | Från signal till handling: användare -> n8n -> AI/CRM -> svar. | Ger en mental modell för hela kedjan. |
| Gemensam demo | 15 min | Lead skickas genom flödet och följs i stacken. | Förankrar teorin i ett konkret exempel. |
| Avslutning | 5 min | Sammanfattning och frågor. | Hjälper deltagarna att sortera vad som är viktigast. |

**Takeaway från lektion 1:** Deltagarna ska kunna förklara vilket problem stacken löser, vilken tjänst som gör vad, och hur huvudflödet ser ut.

## Lektion 2 (90 min)

**Tema:** Felsökning, exempel och tillämpning

| Del | Tid | Innehåll | Varför |
|-----|-----|----------|--------|
| Problembild och metod | 10 min | Vad går ofta fel i automatiserade flöden och hur börjar man tänka när något inte fungerar? | Tränar deltagarna att läsa flöden som problemkedjor, inte bara som teknik. |
| HTTP-statuskoder och felbilder | 15 min | 200, 400, 401, 404, 500 och vad de betyder i praktiken. | Gör felsökning mer konkret och användbart i dialog med leverantörer och IT. |
| n8n executions och miljövariabler | 20 min | Hur man spårar körningar, läser indata/utdata och kopplar fel till konfiguration. | Visar var man faktiskt felsöker i ett riktigt flöde. |
| Lösningsmönster | 10 min | Dela upp ansvar mellan frontend, n8n, AI och CRM. | Hjälper deltagarna att förstå varför vi inte lägger allt i ett enda verktyg. |
| Exempel med diagram | 20 min | Lead capture, support triage och batch/sammanfattning. | Visar hur samma grundarkitektur kan användas för olika affärsproblem. |
| Demo / mini-labb | 10 min | Spåra en körning, provocera fram fel och testa webhook utan webbläsare. | Ger praktisk förståelse för hur fel upptäcks och tolkas. |
| Avslutning | 5 min | Sammanfattning och nästa steg. | Knyter ihop affärsnytta, teknik och lärdomar. |

**Takeaway från lektion 2:** Deltagarna ska kunna beskriva vad som sannolikt har gått fel i ett flöde, var de ska börja titta, och hur samma lösningsmönster kan återanvändas.

## Flöden vi visar och varför

### 1. Lead capture

**Flöde:** Formulär -> n8n -> Flowise -> Twenty  
**Varför vi visar det:** Det är kursens viktigaste exempel eftersom det kopplar direkt till marknad, leadhantering och CRM. Det visar hela kedjan från insamling till affärsobjekt.

### 2. Support triage

**Flöde:** Fråga -> n8n -> Flowise -> svar + eventuell eskalering  
**Varför vi visar det:** Det visar att samma arkitektur inte bara fungerar för försäljning, utan också för support. Det gör det lättare att förstå varför Chatwoot finns med i sammanhanget.

### 3. Batch / sammanfattning

**Flöde:** Insamlad data -> n8n -> AI-sammanfattning -> Slack / CRM / Sheet  
**Varför vi visar det:** Alla flöden är inte realtid. Det här exemplet visar hur automation också kan användas för översikt, prioritering och beslut.

## Varför vi inte visar fler flöden

Vi har medvetet valt att fokusera på tre tydliga flödestyper i stället för att visa många varianter. Skälet är att deltagarna lättare ser mönster när samma grundstruktur återkommer:

- en signal kommer in
- n8n orkestrerar
- AI används där det skapar värde
- data skrivs vidare eller leder till ett beslut

När den modellen sitter blir det lättare att senare förstå nya fall på egen hand.

## Material som delas till studenterna

- `slides/index.html` — startsida till presentationerna
- `slides/forelasning-1-ai-crm-stack.html` — helhetsbild, historik, stack och arkitektur
- `slides/forelasning-2-ai-crm-stack.html` — felsökning, exempel, statuskoder och tillämpning
- `flowise/import/lead-qualifier-chatflow.json` — exempel på AI-flöde för lead
- `flowise/import/support-triage-chatflow.json` — exempel på AI-flöde för support
- `flowise/README.md` — stöd för uppsättning och förståelse av miljön
- `n8n/workflows/lead.json`, `support.json`, `chatwoot.json` — n8n-import (lead, formulär-support, Chatwoot-webhook)
- `n8n/README.md` — kort översikt över arbetsflödena

## Sammanfattning

Målet med kursen är inte att deltagarna ska bli utvecklare på två lektioner. Målet är att de ska kunna förstå flöden bättre, ställa klokare frågor, läsa fel mer systematiskt och se hur automation och AI kan användas på ett sätt som faktiskt hjälper verksamheten.
