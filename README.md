# Nova - DBC Launchpad + Rug Detection

**Solana | Meteora DBC + DAMM v2 | Free Launch | Auditable**

Nova egy ingyenes coin launchpad Solana-n, jobb mint pump.fun. Nem fix bonding curve + Raydium migrációs káosz, hanem Meteora Dynamic Bonding Curve (DBC) -> automatikus migráció DAMM v2 poolba. Dinamikus fee, jobb likviditás, kevesebb rug esély.

> Lord verzió - Norbert Csanya | Broxbourne, UK | 2026.10.17

---

## Miért jobb mint pump.fun?

| pump.fun | Nova (Meteora DBC) |
|---|---|
| fix curve + 1 SOL migráció Raydiumra, sokszor elcsúszik | te állítod a görbét, dinamikus fee |
| migrációs káosz | automatikus migráció DAMM v2-be |
| rug gyakori | jobb likviditás, kevesebb rug esély |

---

## Rug Detection - Core Feature

A Nova nem csak launchol, hanem szűr. Minden DBC launchra számolunk egy **Rug Score 0-100**-t.

### Adatok amiket logolunk (on-chain + off-chain ledger - HMRC kompatibilis)

**Python backend (FastAPI) indexeli a chain-t:**

1. **DBC Create**
   - dev wallet, creation time, curve params, fee config

2. **Buy / Sell**
   - wallet, amount, timestamp, price, holder delta

3. **Migrate (DBC -> DAMM v2)**
   - liquidity amount, pool address, LP lock status

### Rug Score faktorok

```python
# src/rug_detector.py - váz
score = 100  # indulás biztonságos

- top_10_holders_pct > 50%  -> -30 pont
- dev_holding > 15% migráció után -> -25 pont
- bundled wallets (1 dev -> 10+ wallet) -> -20 pont
- LP nem locked / burn-ölve DAMM v2-ben -> -20 pont
- snipers > 30% supply első 3 blokkban -> -15 pont
- sell tax / freeze authority még él -> -20 pont
- volume wash detection (ugyanaz a 3 wallet oda-vissza) -> -10 pont

0-30 = HIGH RISK (piros)
31-69 = MEDIUM (sárga)
70-100 = LOW RISK (zöld)
```

### Data Schema

`docs/data_schema.md`-ben:
- `trades` table: signature, wallet, side, amount, price, ts, pool
- `holders` table: mint, wallet, pct, is_dev, is_bundled_group
- `pools` table: mint, dbc_address, damm_v2_address, lp_locked, migrated_at
- `rug_scores` table: mint, score, factors_json, updated_at

Minden CSV exportálható könyveléshez.

---

## Tech Stack - MVP

```
Frontend (Next.js) 
   -> Meteora DBC SDK 
   -> Solana RPC (Helius)
   -> Backend Python FastAPI (indexer + rug detector + ledger)
   -> Hermes agent + DeepSeek v4 Flash (szűrés, leírás)
```

- **Free launch modell:** Platform fizeti a rent-et (0.002 SOL), nem a user. Bevétel a fee-ből jön vissza.

---

## UK Compliance - kritikus

- Ha te szeded a fee-t, te vagy FCA szerint "cryptoasset exchange provider" -> kell UK Ltd + FCA AML registration
- Minden tx log: on-chain + off-chain ledger (FastAPI)
- Financial Promotion: UK-ban nem ígérhetsz 100x-et
- Élesítés CSAK írásos jogi véleménnyel + FCA AML után. Addig testnet.

Javaslat: Büfé utánfutó (£4k trailer megvan) -> havi fix -> ebből Nova jogász. Cayman Foundation + UK dev cég kombó éleshez.

---

## 4 Fázis (ahogy bővítetted)

1. **Launchpad:** ingyen coin Meteora DBC-n -> DAMM v2
2. **Axiom-szerű terminál:** szűrő (új DBC launchok / migrált DAMM v2 / top holder %, rug score, volume), long/short, snipe, limit order. Te látod a chain-t belülről.
3. **Saját wallet mint Phantom:** non-custodial, benne launchpad + trading + portfólió
4. **Fizikális kártya:** crypto card, UK-ban FCA + EMI partner (Railsr / Striga)

---

## GitHub Repo struktúra

```
/src
  rug_detector.py       # rug score engine
  indexer.py            # Helius -> DB
  bundler_check.py      # bundled wallet detection
  damm_v2.py            # LP lock check
/docs
  data_schema.md
  api.md
/frontend
  (Next.js - később)
README.md
requirements.txt
```

---

## Következő lépés

- [ ] Testnet DBC create 3 coinnal
- [ ] Indexer -> rug score számolás élőben
- [ ] Dashboard: top holder %, bundled graph, LP lock
- [ ] CSV export HMRC-re

---

## Pitch - Anthropic Fellows angle

Transparency + compliance + Python logging + safety. A Nova logolása = auditálható launchpad, ez pont Fellows témába vág. Minden launch visszakövethető, nem black box.

---

Built by Lord Norbert Csanya, for UK, with safety first.
