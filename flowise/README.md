# Flowise — snabbstart för demot

Flowise kör i Docker på **http://localhost:3000** (se rotens `docker-compose.yml`).

## 1. Sätt API-nyckel (OpenAI)

Det enklaste för labbet är att skicka in OpenAI-nyckeln som miljövariabel till containern.

- Antingen: exportera innan start i **värden** (där du kör Docker):

  ```bash
  export OPENAI_API_KEY="sk-..."
  docker compose up -d
  ```

  (Rotens `docker-compose` läser `OPENAI_API_KEY` för Flowise-tjänsten om den finns.)

- Eller: lägg nyckeln manuellt i Flowise UI under **Credentials** om du föredrar det.

> **Obs:** Utan nyckel kan du fortfarande köra hela kedjan, men AI-svar blir tomma eller fel tills nyckeln finns.

## 2. Skapa en enkel Chatflow

1. Öppna **http://localhost:3000**  
2. **Add New** → **Chatflow**  
3. Dra in ett **Chat Models**-steg, t.ex. **OpenAI** (eller motsvarande i din Flowise-version) och koppla till en **LLM Chain** / huvudnod enligt guiden i UI.  
4. Målet är minimal kedja: **inmatning (question) → språkmodell → svar**.  
5. Spara chatflow och döp den gärna till **demo** (namnet är bara för er själva).

## 2b. Importera färdiga exempel för kursen

I repot finns två exempel som matchar presentationerna och n8n-demot:

- [`flowise/import/lead-qualifier-chatflow.json`](import/lead-qualifier-chatflow.json)
- [`flowise/import/support-triage-chatflow.json`](import/support-triage-chatflow.json)

### Så här laddar du in dem

1. Öppna **Flowise**
2. Skapa ett **tomt chatflow**
3. Öppna inställningsmenyn i editorn och välj **Load Chatflow**
4. Ladda in en av JSON-filerna ovan
5. Koppla eller välj din **OpenAI credential** i modellen om Flowise ber om det
6. Spara chatflow

> Obs: Filerna i `import/` ar nu byggda efter samma `nodes`/`edges`-format som den installerade lokala Flowise-versionens egna marketplace-chatflows anvander. Om ni senare uppgraderar Flowise kraftigt kan nodmetadata fortfarande skilja sig, men i denna miljo ar de anpassade till lokal version.

## 3. Koppla n8n till rätt prediction-URL

Flowises HTTP-API använder **chatflow-id** (UUID), inte bara namnet “demo”.

- Öppna chatflow i editorn och leta upp id i URL:en, eller via Flowise lista/export.  
- Sätt miljövariabeln **`FLOWISE_CHATFLOW_ID`** för **n8n**-containern (i `docker-compose.yml` under `n8n.environment`), och starta om n8n:

  ```yaml
  FLOWISE_CHATFLOW_ID: "din-chatflow-uuid"
  ```

n8n-workflows i detta repo anropar:

`http://flowise:3000/api/v1/prediction/<FLOWISE_CHATFLOW_ID>`

med JSON-kroppen:

```json
{ "question": "meddelande från användaren" }
```

## 4. Kursens två Flowise-scenarier

### A. Lead Qualifier

- Syfte: ge ett kort AI-stöd för **lead-sammanfattning**
- Används ihop med: `n8n/workflows/lead.json`
- Rekommenderat namn i UI: **demo-lead**

### B. Support Triage

- Syfte: ge första svar och markera när frågan bör **eskaleras**
- Används ihop med: `n8n/workflows/support.json`
- Rekommenderat namn i UI: **demo-support**

## 5. Testa prediction manuellt (valfritt)

```bash
curl -sS -X POST "http://localhost:3000/api/v1/prediction/<DITT_ID>" \
  -H "Content-Type: application/json" \
  -d '{"question":"Hej! Kan du förklara vad en webhook är?"}'
```

Om svaret kommer tillbaka som JSON med modellens text är Flowise redo för n8n-demot.
