# Supplier Entity Resolution

## 1. Summary
A major manufacturing company’s procurement department initiated a digitalization journey to clean up a cluttered,
duplicate, and outdated supplier database. Without a unified single source of truth, category managers were blocked 
from executing accurate analysis, driving cost-saving strategies for the upcoming fiscal year, and assessing 
supply chain sustainability due to internal resource constraints.

**This project transforms messy input records into a pristine, verified 1:1 master dataset.**

## 2. Commercial & Strategic Recommendations for the Client
The main focal point was identifying the noise, duplicate messy entries with unnecessary social media links and 
removing them delivering a ultra clean high signal master table built on four functional pillars that directly 
enable their cost strategy and supply chain digitalization

### 2.1 Traceability & System Integration (The "Anchor")
Input row key, veridion id, company name, company legal names, website url

### 2.2 Scale & Commercial Leverage (The "Negotiation Power")
Revenue, employee count, year founded

### 2.3 Spend Categorization (The "Spend Analysis Engine")
Main sector, sics codified industry

### 2.4 Geography & Compliance (The "Risk Management Filter")
Main country, main country code, main region, main city

## 3. Entity Resolution Methodology & Multi-Signal Scoring
Since Raw procurement data is notoriously inconsistent, featuring typos, 
omitted address lines, and mismatched legal suffixes. 
To solve this, a custom multi-signal scoring function was implemented.

The Hierarchy of Trust
The engine evaluates each candidate record against the client's input 
across multiple dimensions, assigning professional enterprise weights:

### 3.1 Company Name Similarity (40%): 
Evaluates token sort ratios across standard, legal, and commercial name fields 
(company_name, company_legal_names, company_commercial_names) to capture trade names vs formal corporate entities.

### 3.2 Country Alignment (25%): 
A strict geographic filter (main_country) 
ensuring international subsidiaries aren't incorrectly cross-matched.

### 3.3 Region & City Validators (20% combined): 
Local headquarters and regional branch matching with the purpose to fine-tune the country alignment and 
pinpoint the exact location.

### 3.4 Postcode & Street Address (15% combined): 
Micro-signals acting as granular tie-breakers since these are related to other higher priority signals such as
the country, region and city.

### Dynamic Counting Re-Normalization
In sparse enterprise datasets, fields like postcodes or regions are frequently missing. 
To prevent correct matches from being penalized with a zero score, the script features dynamic re-normalization: 
if a field is null or missing, it is excluded from the calculation, and automatically re-scaled to sum to 100%.

## 4. Data Quality Control & Confidence Analysis
Transparency and risk management are core pillars and the script automatically generates backend audit reports that
serve two main purposes:

### 4.1 Data Completeness & Missing Attribute Planning

Profiling fill rates across the resolved dataset allowed us to identify 
which attributes are most heavily affected by missing data

### 4.2 Operational Confidence Tiers
Confidence tiers high(>80%), medium(50%-80%) and low(<50%) were designed not merely for client facing 
transparency, but as an internal calibration tool for how much each score should counts and to give us insights 
that directly drove to the update of the name matching section expanding it to evaluate multiple names simultaneously.

## 5. Technical Architecture & Tech Stack
To keep the solution lightweight, reproducible, and easy to run in any cloud or local environment, the project is built on a clean, robust stack:

**Python (pandas & NumPy):** Core data manipulation, schema shaping, and vectorized transformation.\
**RapidFuzz:** High-performance string similarity scoring written in C++ for fast, accurate fuzzy matching.\
**SQLAlchemy:** Infrastructure-ready connection layer for relational database storage and bulk-loading.\
**GitHub:** Version control and professional repository structuring.

### Repository Layout
```text
supplier-entity-resolution/
├── README.md                   # General description of the project
├── main.py                     # End-to-end Python processing pipeline
├── requirements.txt            # Core dependencies
├── presales_data_sample.csv    # Raw client input dataset
├── presales_data.csv           # Final curated 1:1 master dataset for the client
└── data_attributes/            # Technical audit receipts for Veridion reviewers
    ├── confidence_analysis.csv # Match confidence breakdown
    └── data_qc_report.csv      # Data quality fill-rates and missing value counts