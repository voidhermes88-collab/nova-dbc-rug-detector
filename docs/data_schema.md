# Data Schema - Nova Ledger

HMRC kompatibilis, on-chain + off-chain

## trades
- signature (PK)
- mint
- wallet
- side: buy/sell
- amount
- price_sol
- timestamp
- pool_address
- block_slot

## holders
- mint
- wallet
- balance
- pct
- is_dev: bool
- bundled_group_id: int | null

## pools
- mint (PK)
- dbc_address
- damm_v2_address | null
- curve_params_json
- lp_locked: bool
- lp_burned_pct
- migrated_at | null
- created_at

## rug_scores
- mint (FK)
- score 0-100
- risk: HIGH/MEDIUM/LOW
- factors_json
- updated_at

Export: CSV napi bontásban -> könyvelés
