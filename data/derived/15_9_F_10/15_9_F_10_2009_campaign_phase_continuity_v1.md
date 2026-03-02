# 15/9/F/10 — 2009 Campaign Phase Continuity (v1)

Input: `/content/drive/MyDrive/LW_DTRE/derived/15_9_F_10/15_9_F_10_campaign_events_typed.jsonl`
Events: 1075
Days with classified activity: 71

## Phase blocks

| Block | Start | End | Days | Dominant phase |
|---:|---|---|---:|---|
| 1 | 2009-04-07 | 2009-04-08 | 2 | DRILLING |
| 2 | 2009-04-09 | 2009-04-09 | 1 | WAITING |
| 3 | 2009-04-10 | 2009-05-17 | 38 | DRILLING |
| 4 | 2009-05-18 | 2009-05-18 | 1 | EQUIPMENT_FAILURE |
| 5 | 2009-05-19 | 2009-06-04 | 17 | DRILLING |
| 6 | 2009-06-05 | 2009-06-14 | 10 | WAITING |
| 7 | 2009-06-15 | 2009-06-16 | 2 | DRILLING |

## Notes

- Dominant phase per day is the most frequent `event_type` (excluding UNKNOWN/blank).
- Blocks collapse consecutive days with the same dominant phase.
