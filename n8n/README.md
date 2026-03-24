# n8n-arbetsflöden (demo)

Importera i n8n (**Workflows → Import from File**) och **aktivera** varje flöde.

| Fil | Webhook-sökväg | Syfte |
|-----|----------------|--------|
| [workflows/lead.json](workflows/lead.json) | `/webhook/lead` | Lead från formulär → Flowise → Twenty |
| [workflows/support.json](workflows/support.json) | `/webhook/support` | Supportfråga → Flowise → JSON-svar (`reply`, `escalate`) |
| [workflows/chatwoot.json](workflows/chatwoot.json) | `/webhook/chatwoot` | Chatwoot `message_created` → Flowise → svar tillbaka via Chatwoot API |
| [workflows/legacy-regex-starter.json](workflows/legacy-regex-starter.json) | - | Starterflöde för elever: hämta senaste legacy-raden och fyll i regex själv |
| [workflows/legacy-reward-preview.json](workflows/legacy-reward-preview.json) | `/webhook/legacy-reward-preview` | Tar emot strukturerad JSON och svarar med HTML-preview |
| [workflows/legacy-regex-solution.json](workflows/legacy-regex-solution.json) | `/webhook/legacy-sqlite-solution` | Komplett lösning: hämta legacy-rad → regex-parsa → HTML-preview |

**Chatwoot:** se huvud-README för `CHATWOOT_API_ACCESS_TOKEN`, webhook-URL (`http://n8n:5678/webhook/chatwoot`) och loop-skydd (bara inkommande meddelanden).

## Legacy-case

Det nya legacy-caset bygger på `legacy-freetext-case/`.

- Datakällan är SQLite, men n8n hämtar raden via `http://legacy-ugly-web:8086/api/submissions/latest` eller `.../api/submissions/{id}` för att kursmiljön ska vara stabil.
- Starterflödet är till för att eleverna ska fylla i regex-logiken själva.
- Reward-webhooken är till för sista steget i övningen, när blobben redan är uppstrukturerad.
- Solution-webhooken kan öppnas direkt i webbläsaren för att visa ett komplett facit.

Exempel:

- `http://localhost:5678/webhook/legacy-sqlite-solution`
- `http://localhost:5678/webhook/legacy-sqlite-solution?submissionId=2`
