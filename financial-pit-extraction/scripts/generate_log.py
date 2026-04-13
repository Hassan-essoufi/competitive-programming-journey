"""
Generates a human-readable Data Extraction Log (Markdown + CSV) from an output file.
Run after extract_pit.py to produce the deliverable log.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "output"
LOG_DIR    = Path(__file__).parent.parent / "logs"


def generate_log(csv_path: Path):
    df  = pd.read_csv(csv_path)
    row = df.iloc[0]

    md = f"""# Data Extraction Log

## 1. Identification
| Field              | Value |
|--------------------|-------|
| Company gvkey      | `{row.get('gvkey', 'N/A')}` |
| Reference date     | `{row.get('reference_date', 'N/A')}` |
| Fiscal period end  | `{row.get('datadate', 'N/A')}` |
| Fiscal year        | `{row.get('fyear', 'N/A')}` |
| Extraction time    | `{row.get('extraction_timestamp', 'N/A')}` (UTC) |

## 2. Dataset & Table
| Field         | Value |
|---------------|-------|
| Platform      | WRDS  |
| Database      | Compustat Fundamentals Annual |
| Table         | `comp.funda` |
| Data format   | `datafmt = 'STD'`  (standard) |
| Consolidation | `consol  = 'C'`    (consolidated) |
| Pop. source   | `popsrc  = 'D'`    (domestic) |
| Ind. format   | `indfmt  = 'INDL'` (industrial) |

## 3. Target Field
| Field         | Value |
|---------------|-------|
| Field name    | `ebit` |
| Description   | Earnings Before Interest and Taxes |
| Derivation    | None — direct database field |
| Substitution  | None |

## 4. Point-in-Time Rules
| Rule   | Condition                          | Purpose |
|--------|------------------------------------|---------|
| PIT-1  | `datadate <= reference_date`       | Fiscal period must have closed before reference date |
| PIT-2  | `rdq <= reference_date`            | Filing must have been publicly available before reference date |

## 5. Selection Rule (when multiple records exist)
```sql
ORDER BY rdq DESC, datadate DESC
LIMIT 1
```
Selects the **most recently filed** fiscal period that was available as of the reference date.

## 6. Extracted Value
| Metric | Value |
|--------|-------|
| EBIT   | `{row.get('ebit', 'N/A')}` (USD thousands, Compustat convention) |
| Filing date (rdq) | `{row.get('rdq', 'N/A')}` |

## 7. Reproducibility
- Query is fully deterministic given `gvkey` and `reference_date`
- No manual overrides or post-processing applied
- Output file: `{csv_path.name}`
- Log generated: `{datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")}` (UTC)
"""

    log_path = LOG_DIR / f"extraction_log_{row.get('gvkey', 'unknown')}_{row.get('reference_date', 'unknown')}.md"
    log_path.write_text(md)
    print(f"Log written to: {log_path}")
    return log_path


if __name__ == "__main__":
    csvs = sorted(OUTPUT_DIR.glob("ebit_pit_*.csv"))
    if not csvs:
        print("No output CSV found. Run extract_pit.py first.")
    else:
        generate_log(csvs[-1])
