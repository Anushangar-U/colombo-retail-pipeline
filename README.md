# Colombo Retail Market Data Pipeline

A lightweight data pipeline and audit tool that ingests weekly retail price observations collected across Colombo districts, performs cleaning and volatility metric calculation, and produces concise operational metrics and insights for procurement and analytics teams.

**Problem solved**
- Detects items and weeks with unusually large local price spreads that indicate supply-chain risk for procurement or inventory planning.

**Solution overview**
- Ingest raw weekly price CSVs, clean and normalize prices, compute a `volatility_index` (price spread ÷ average price), flag records with index > 0.30 as `is_highly_volatile`, and produce both a consolidated `cleaned_master.csv` and human-readable summaries.

**Tech used**
- Python 3.8+
- pandas, numpy
- CSV files for input / output

Core scripts
- `pipeline.py` — initial ingestion and cleaning of `raw/retail_prices.csv` into `cleaned_master.csv`
- `automate_pipeline.py` — incremental ingestion of CSVs placed in `incoming_data/` and incremental update of `cleaned_master.csv`
- `generate_readme_metrics.py` — exports a markdown summary to `project_summary.md`
- `get_insights.py` — prints a quick console insights report from `cleaned_master.csv`

Key findings (example output)
- Total sample size (current master): 22,445 records
- Overall market volatility rate: 65.50% (fraction of records flagged as highly volatile)
- Top unstable commodities (sample): Gotukola, Betel Leaves (Average), Raddish, Drumstick, Kohila Yams
- Yearly trend: market volatility has risen from ~54% in 2020 to ~74% in 2024 (see `project_summary.md`)

These metrics are produced by `generate_readme_metrics.py` and written to `project_summary.md`.

How to run (quick)
1. Create and activate a Python virtual environment, then install dependencies:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install pandas numpy
```

2. Ensure the raw dataset is available at `raw/retail_prices.csv` (sample included).

3. Produce the baseline cleaned master dataset:

```bash
python pipeline.py
```

4. Integrate any new incoming files placed into `incoming_data/` (incremental):

```bash
python automate_pipeline.py
```

5. Generate the human-readable summary (writes `project_summary.md`):

```bash
python generate_readme_metrics.py
```

6. Print a short insights report to console:

```bash
python get_insights.py
```

Configuration and notes
- Scripts currently use absolute paths rooted at the repository directory. Edit the `base_path` or `raw_data_path` variables at the top of scripts to run elsewhere, or refactor to use environment variables or CLI args for portability.
- Consider adding a `requirements.txt` with pinned versions, and lightweight unit tests for the cleaning/metric functions.

Outputs
- `cleaned_master.csv` — consolidated cleaned dataset
- `project_summary.md` — markdown summary produced by `generate_readme_metrics.py`

Want me to:
- add a `requirements.txt` and simple `run.sh`/`run.ps1` helpers?
- refactor paths into a small `config.py` for portability?

---

Maintained to help run, reproduce, and interpret the pipeline outputs.