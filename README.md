# n8n — Zubair's automation builder (on this VM)

**Version:** 2.43.7 · **Status:** running · **Editor:** http://localhost:5678

## Start / Stop

```bash
# START (from any terminal on this VM)
cd ~/workspace/n8n
N8N_USER_FOLDER=~/workspace/n8n/data N8N_PORT=5678 ./node_modules/.bin/n8n start

# run it in background instead:
cd ~/workspace/n8n
N8N_USER_FOLDER=~/workspace/n8n/data N8N_PORT=5678 nohup ./node_modules/.bin/n8n start > /tmp/n8n-server.log 2>&1 &

# STOP
pkill -f "[n]8n start"

# HEALTH CHECK
curl -s http://localhost:5678/healthz   # -> 200 means up
```

## Important notes

- **Data persists** in `~/workspace/n8n/data/` (SQLite DB + encryption key). It survives VM restarts — everything under `~` is persistent. Just re-run the START command after a reboot.
- **The editor is ONLY reachable from this VM's browser** (http://localhost:5678). Your phone cannot open it directly. If you later want phone/anywhere access, the option is a Cloudflare tunnel (`cloudflared`) — ask Lapis before enabling; it would expose the editor to the internet, so it needs a login + care.
- **No owner account created yet** — the first time you open http://localhost:5678 in the VM browser, n8n will ask you to set up the owner account (email + password). **Do that yourself** — Lapis never creates accounts or credentials for you.
- **No credentials are stored** — the demo workflow's Gmail and Google Sheets nodes are intentionally empty. You connect YOUR Google account in the editor (Credentials → New → Gmail OAuth2 / Google Sheets OAuth2). Nothing leaves this VM until you wire a credential and activate a workflow.
- **Server is NOT exposed publicly** — it binds to localhost only.

## Demo workflow: "Lead Alerts - Agency Demo" ✅ tested end-to-end

`lead-alerts-agency-demo.json` (also imported + ACTIVE in n8n)

```
Webhook (POST /webhook/new-lead) → IF (has email?) → Gmail: Notify Owner ─┐
                                                      Sheets: Log Lead ────┴→ Respond ("Lead received")
```

- **Live test result (2026-10-18):** POSTing `{"name":"Final Test","email":"final@example.com",...}` executed Webhook → IF routed to the TRUE branch → Gmail node attempted and stopped **only** at the credential gate (`Node does not have any credentials set for "gmailOAuth2"`). That is the expected state — connect your Gmail in the editor and it sends.
- The Gmail "To" is pre-set to your own address (notification goes to you); change it in the node if you want.
- Test it yourself: `curl -X POST http://localhost:5678/webhook/new-lead -H "Content-Type: application/json" -d '{"name":"Ali","email":"ali@test.com","source":"website"}'`

## RAM

n8n uses ~450MB idle on this VM (~990MB free while running). It stays up fine. If the VM ever gets slow, stop n8n when you're not building.

## If you ever need to reinstall

`npm install n8n` FAILS in this sandbox (npm's tar tries `chown`, which is blocked even for root → thousands of EPERM errors). The working method used here:
1. `npm install --package-lock-only` (generates a full lockfile, no extraction)
2. `node manual-reify.js` — extracts cached tarballs with system `tar --no-same-owner`
3. Missing tarballs: `node fetch-missing2.js` (downloads + hash-verifies into npm cache)
4. sqlite3 native binding: prebuilt downloaded to `node_modules/sqlite3/build/Release/node_sqlite3.node` manually (prebuild-install's chown also blocked)

Keep `manual-reify.js`, `fetch-missing.js`, `fetch-missing2.js` — they make a reinstall reproducible.
