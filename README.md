# colombo retail market data pipeline: automated audit summary

## executive overview
> **key finding:** an analysis of 22,445 weekly retail price data points across colombo districts reveals an overall supply chain price volatility rate of **65.50%**. static procurement contracts face significant risk from localized price spreads.

---

## core metrics and risk analysis

### top 5 items with highest market price variance
the table below shows the average volatility index (price spread divided by average price) for the most unstable commodities in the dataset.

| commodity item | average volatility index | risk classification |
| :--- | :---: | :--- |
| Gotukola | 1.19 | high risk supply variance |
| Betel Leaves ( Average ) | 1.15 | high risk supply variance |
| Raddish | 0.96 | high risk supply variance |
| Drumstick | 0.91 | high risk supply variance |
| Kohila Yams | 0.88 | high risk supply variance |

---

### structural stability trends over time
the percentage of items experiencing severe price spreads (above 30% variance between maximum and minimum market rates) tracked by year:

* **year 2020:** 53.81% of monitored items showed extreme volatility
* **year 2021:** 57.25% of monitored items showed extreme volatility
* **year 2022:** 70.98% of monitored items showed extreme volatility
* **year 2023:** 71.64% of monitored items showed extreme volatility
* **year 2024:** 73.75% of monitored items showed extreme volatility

---
## pipeline operational status
* **ingestion mode:** automated batch processing via glob
* **transformation engine:** pandas and numpy vectorized arrays
* **target storage:** incremental updates to centralized master repository
