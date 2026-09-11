# Supplier Entity Resolution

## 1. Summary
A major manufacturing company’s **Procurement department** initiated a digitalization journey to clean up a cluttered,
duplicate, and outdated supplier database. Without a unified single source of truth, category managers were blocked 
from executing accurate spend analysis, driving cost-saving strategies for the upcoming fiscal year, and assessing 
supply chain sustainability (ESG) due to internal resource constraints.

This project transforms messy input records into a pristine, verified 1:1 master dataset.

## 2. Entity Resolution Methodology & Multi-Signal Scoring

Since Raw procurement data is notoriously inconsistent, featuring typos, 
omitted address lines, and mismatched legal suffixes. 
To solve this, a custom multi-signal scoring function was implemented in 
main.py rather than relying on brittle exact-match rules.

The Hierarchy of Trust
The engine evaluates each candidate record against the client's input 
across multiple dimensions, assigning professional enterprise weights:

### 2.1 Company Name Similarity (40%): 
Evaluates token sort ratios across standard, legal, and commercial name fields 
(company_name, company_legal_names, company_commercial_names) to capture trade names vs. formal corporate entities.

### 2.2 Country Alignment (25%): 
A strict geographic filter (main_country) 
ensuring international subsidiaries aren't incorrectly cross-matched.

### 2.3Region & City Validators (20% combined): 
Local headquarters and regional branch matching with the purpose to fine-tune the country alignment and 
pinpoint the exact location.

### 2.4 Postcode & Street Address (15% combined): 
Micro-signals acting as granular tie-breakers since these are related to other higher priority signals such as
the country, region and city.

