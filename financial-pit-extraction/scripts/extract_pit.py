"""
Point-in-Time (PIT) Financial Data Extraction
Target field : EBIT
Source       : WRDS / Compustat Fundamentals Annual (funda)
Constraint   : fiscal period end <= reference_date
               data_date (availability/filing date) <= reference_date
"""

import pandas as pd
import wrds
import logging
from datetime import datetime, date
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
REFERENCE_DATE = date(2023, 12, 31)   # <-- change this
GVKEY          = "001690"             # <-- Compustat gvkey for target company
OUTPUT_DIR     = Path(__file__).parent.parent / "data" / "output"
LOG_DIR        = Path(__file__).parent.parent / "logs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

EXTRACTION_TIMESTAMP = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    filename=LOG_DIR / f"extraction_{EXTRACTION_TIMESTAMP.replace(':', '-')}.log",
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
)
log = logging.getLogger(__name__)

# ── Query ─────────────────────────────────────────────────────────────────────
QUERY = """
    SELECT
        gvkey,
        datadate,        -- fiscal period end date
        fyear,           -- fiscal year
        fyr,             -- fiscal year-end month
        datafmt,         -- data format (STD / non-STD)
        consol,          -- consolidation level (C = consolidated)
        popsrc,          -- population source (D = domestic)
        indfmt,          -- industry format (INDL / FS)
        ebit,            -- Earnings Before Interest and Taxes (direct field)
        rdq              -- report/filing date (availability date)
    FROM comp.funda
    WHERE gvkey = '{gvkey}'
      AND datadate  <= '{ref}'     -- fiscal period end  ≤ reference date  (PIT rule 1)
      AND rdq       <= '{ref}'     -- filing date        ≤ reference date  (PIT rule 2)
      AND ebit IS NOT NULL         -- exclude missing EBIT rows
      AND datafmt  = 'STD'         -- standard format only
      AND consol   = 'C'           -- consolidated statements only
      AND popsrc   = 'D'           -- domestic population source
      AND indfmt   = 'INDL'        -- industrial format
    ORDER BY rdq DESC, datadate DESC
    LIMIT 1                        -- most recently available record as of reference date
""".format(gvkey=GVKEY, ref=REFERENCE_DATE)


def run_extraction():
    log.info("=== Extraction started ===")
    log.info("Reference date    : %s", REFERENCE_DATE)
    log.info("Target gvkey      : %s", GVKEY)
    log.info("Dataset / table   : comp.funda (WRDS Compustat Fundamentals Annual)")
    log.info("EBIT field code   : ebit  (no derivation, direct DB field)")
    log.info("PIT rule 1        : datadate <= reference_date")
    log.info("PIT rule rule 2   : rdq      <= reference_date")
    log.info("Selection rule    : ORDER BY rdq DESC, datadate DESC LIMIT 1")
    log.info("Extraction time   : %s (UTC)", EXTRACTION_TIMESTAMP)

    db  = wrds.Connection()
    log.info("WRDS connection established")

    df = db.raw_sql(QUERY)
    db.close()

    if df.empty:
        log.error("No records found — check gvkey or reference date.")
        raise ValueError("No PIT record found for the given parameters.")

    row = df.iloc[[0]].copy()
    row["extraction_timestamp"] = EXTRACTION_TIMESTAMP
    row["reference_date"]       = str(REFERENCE_DATE)
    row["pit_rule_datadate"]    = "datadate <= reference_date"
    row["pit_rule_rdq"]         = "rdq <= reference_date"
    row["selection_rule"]       = "ORDER BY rdq DESC, datadate DESC LIMIT 1"
    row["source_table"]         = "comp.funda"
    row["ebit_derivation"]      = "none — direct DB field"

    out_path = OUTPUT_DIR / f"ebit_pit_{GVKEY}_{REFERENCE_DATE}.csv"
    row.to_csv(out_path, index=False)

    log.info("Output written to  : %s", out_path)
    log.info("Row count          : 1")
    log.info("EBIT value         : %s", row["ebit"].values[0])
    log.info("Fiscal period end  : %s", row["datadate"].values[0])
    log.info("Filing date (rdq)  : %s", row["rdq"].values[0])
    log.info("=== Extraction complete ===")

    print(row.to_string(index=False))
    return row


if __name__ == "__main__":
    run_extraction()
