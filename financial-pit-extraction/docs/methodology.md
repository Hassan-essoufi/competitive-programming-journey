# PIT Extraction Methodology

## What is Point-in-Time (PIT)?

A PIT extraction simulates what an analyst would have known on a given **reference date** — no data that was filed or revised after that date is used. This eliminates **look-ahead bias**.

## Two-date enforcement

| Date field | Compustat field | Rule |
|------------|-----------------|------|
| Fiscal period end | `datadate` | must be ≤ reference date |
| Filing / availability date | `rdq` | must be ≤ reference date |

Using only `datadate` is **not sufficient** — a company may file months after its fiscal year ends. `rdq` is the date the data became publicly available.

## EBIT — field choice

`ebit` is used directly from `comp.funda`. It is **not derived** (i.e., we do not compute `oiadp + xint` or any other formula). If `ebit` is NULL for a record, that record is excluded.

## Selection rule

When multiple qualifying rows exist (e.g., restatements), the row with the **most recent `rdq`** (and then most recent `datadate` as tiebreaker) is selected. This reflects the most up-to-date filing available as of the reference date.

## Filters applied

| Filter | Value | Reason |
|--------|-------|--------|
| `datafmt` | `STD` | Exclude non-standardized entries |
| `consol`  | `C`   | Consolidated financials only |
| `popsrc`  | `D`   | Domestic (primary) population |
| `indfmt`  | `INDL`| Industrial format (excludes banks/insurers) |

## Output schema

| Column | Description |
|--------|-------------|
| `gvkey` | Compustat company identifier |
| `datadate` | Fiscal period end date |
| `fyear` | Fiscal year |
| `ebit` | EBIT in USD thousands |
| `rdq` | Report/filing date |
| `reference_date` | The reference date used for PIT filtering |
| `extraction_timestamp` | UTC timestamp of extraction |
| `pit_rule_datadate` | PIT rule applied on datadate |
| `pit_rule_rdq` | PIT rule applied on rdq |
| `selection_rule` | Record selection logic |
| `source_table` | Source DB table |
| `ebit_derivation` | Confirms no derivation was used |
