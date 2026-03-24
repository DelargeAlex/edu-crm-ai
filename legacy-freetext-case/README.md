# Legacy Freetext Case

Detta case är medvetet fult och felbyggt.

## Tanke

- Företaget sparar "hela formuläret" som en enda blob i databasen.
- Databasen är SQLite, men den får spela rollen av en gammal "mysql-ish" integrationspunkt.
- Elevens uppgift är att läsa blobben, regex-parsa ut fält, normalisera datan och spara den strukturerat.

## Tjänsten

När stacken är igång finns sidan på:

- `http://localhost:8085`

Internt i Docker-nätverket:

- `http://legacy-ugly-web:8086`

## SQLite-fil

Databasen skapas automatiskt i:

- `legacy-freetext-case/data/legacy_ingest.sqlite3`

## Reward-webhook

För att visa ett snyggt resultat kan n8n eller annat verktyg posta strukturerad JSON till:

- `POST http://legacy-ugly-web:8086/reward`

Exempelpayload:

```json
{
  "name": "Karin Koi",
  "email": "karin@lobbylagret.se",
  "phone": "070-123 45 67",
  "product": "Konserverad Koi Premium",
  "quantity": "18",
  "city": "Borås",
  "category": "bulk_order",
  "issue": "Vill ha premiumfisk till hotellobbyn",
  "source": "sqlite-regex-övning",
  "profileUrl": "https://api.dicebear.com/9.x/fun-emoji/svg?seed=KarinKoi",
  "rawBlob": "namn=Karin Koi | email=..."
}
```

Svar: HTML med tabell, previewkort och bild från `profileUrl`.

## n8n-flöden som hör till caset

Importera dessa filer i n8n:

- `n8n/workflows/legacy-regex-starter.json`
- `n8n/workflows/legacy-reward-preview.json`
- `n8n/workflows/legacy-regex-solution.json`

### Vad de gör

- `legacy-regex-starter.json`: scaffold för elever. Hämtar senaste legacy-raden men lämnar regex-extraktionen som uppgift.
- `legacy-reward-preview.json`: webhook som tar strukturerad JSON och svarar med HTML-preview.
- `legacy-regex-solution.json`: komplett facit som kan öppnas direkt i webbläsaren och visar hela kedjan.

### Webhookar

- `POST http://localhost:5678/webhook/legacy-reward-preview`
- `GET http://localhost:5678/webhook/legacy-sqlite-solution`
- `GET http://localhost:5678/webhook/legacy-sqlite-solution?submissionId=2`

## Frågor till eleverna

1. Om företaget Kjells Konserverade Koi nu har sparat allt i en sträng, beskriv med processdiagram hur vi ska gå tillväga i systemet.
2. Vilka regexar behövs för att hämta ut `namn`, `email`, `telefon`, `produkt`, `antal`, `stad` och `profileUrl`?
3. Vilken målyta väljer ni för den strukturerade datan, och varför?
4. Hur validerar ni att n8n faktiskt extraherat rätt data innan ni skickar den vidare?
5. Hur skulle ni bygga om lösningen om företaget till slut vill sluta med blobbar helt?
