# Social Content Scheduler (Sheet → FB/IG)

**File:** `social-content-scheduler.json` · **Nodes:** 9 · **Status in n8n:** imported, inactive

**Kya karta hai:** Client apna poora mahine ka content Google Sheet (Content Calendar) me pehle se likh deta hai → workflow roz subah 9 baje check karta hai: aaj ki date wali, abhi `posted` na hui rows ko platform ke mutabiq **Facebook Page** ya **Instagram** pe post kar deta hai → sheet me status `posted` mark. Koi roz ki mehnat nahi — sheet bharo, mahina chalao.

**Flow:** Morning Schedule (9:00) → Google Sheets (Content Calendar) → Code node (aaj ki + unposted rows filter) → Facebook? → FB Page post → Mark Posted / Instagram? → IG Container → IG Publish → Mark Posted.

**Sheet format (Content Calendar tab):** columns `date` (YYYY-MM-DD), `platform` (facebook / instagram), `caption`, `media_url`, `status` (khaali ya pending; workflow `posted` kar deta hai).

**Credentials chahiye (client ke):**
- Google Sheets (OAuth) — dono Sheets nodes; sheet ID placeholder.
- Meta Graph API: FB Page ID + Page access token (Facebook nodes me placeholder), IG user ID + access token (Instagram nodes me placeholder). IG posting ke liye account professional (business/creator) + publicly hosted image URL chahiye — Meta ki requirement hai.

**Client pe deploy:** JSON import → sheet connect → Meta tokens → ek aaj ki test row se manual Execute → Active. Caption/media client sheet me deta hai; workflow koi text khud nahi likhta (is liye is me AR/EN message template nahi — content client ka apna hota hai).

**Note:** IG ke 2-step flow (container create → publish) Meta API ki shart hai; dono nodes ready hain.
