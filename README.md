# Machine Learning & Big Data — Project Portfolio

**University of Naples Federico II**  
Polytechnic and Basic Sciences School · Department of Industrial Engineering  
Master's Degree in Autonomous Vehicle Engineering  
**Course:** Machine Learning and Big Data · Academic Year 2024-2025  
**Author:** Mustafa Oner — D18000070

---

## Repository Structure

```
├── big_data/                  # IMDb Top-1000 · MongoDB Analysis
│   ├── imdb_mongo.py          # ETL + aggregation pipeline script
│   └── Big_Data_Report.pdf    # Project report
│
├── machine_learning/          # Supervised Classification · Adult & Forest Cover
│   ├── adult_income/
│   │   └── adult_classification.py
│   ├── forest_cover/
│   │   └── forest_classification.py
│   └── ML_Report.pdf          # Project report
│
└── README.md
```

---

## Project 1 — Big Data: IMDb Top-1000 MongoDB Analysis

### Overview
The IMDb Top-1000 film dataset is loaded into **MongoDB** and analysed through aggregation pipelines. The goal is to extract meaningful insights about genres, directors, actors and the relationship between critical ratings and box-office revenue.

### Why MongoDB?
- **Flexible documents** — film records contain arrays (genres, cast) and optional fields; BSON documents handle this natively without join tables.
- **Schema-on-read** — missing fields do not block loading; `None` is assigned safely.
- **Server-side aggregation** — `$unwind`, `$group`, `$sort` run in the database, minimising data transfer.

### Document Schema
```json
{
  "title": "Inception",
  "year": 2010,
  "certificate": "PG-13",
  "runtime_minutes": 148,
  "genre": ["Action", "Adventure", "Sci-Fi"],
  "rating": 8.8,
  "meta_score": 74,
  "director": "Christopher Nolan",
  "cast": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page", "Tom Hardy"],
  "votes": 2000000,
  "gross": 829895144
}
```

### Indexes
| Field | Purpose |
|---|---|
| `genre` (multikey) | Speeds aggregation by genre |
| `director` | Top directors query |
| `cast` (multikey) | Actor appearance counts |
| `rating` + `gross` (compound) | Correlation analysis |

### Key Findings
| # | Query | Finding |
|---|---|---|
| 1 | Genre distribution | **Drama** dominates with 700+ titles |
| 2 | Average rating by genre | **War, Western, Film-Noir** avg ~8.0 |
| 3 | Top directors | Hitchcock (14), Spielberg (13), Miyazaki (11) |
| 4 | Most frequent actors | De Niro (17), Hanks, Pacino |
| 5 | Rating–Revenue correlation | Pearson r ≈ **0.18** — weak positive |

📎 [Project Notebook on Google Drive](https://drive.google.com/file/d/14AVbdk189z85_XyrpfiGrgd37VPTWW35/view)

---

## Project 2 — Machine Learning: Supervised Classification

### Overview
Two classification tasks are studied end-to-end — from EDA to hyperparameter tuning — to compare how data complexity, class imbalance and feature types affect the full ML workflow.

---

### 2a — Adult Income Classification (Binary)

**Dataset:** UCI Adult / Census-Income (~32,000 rows, 14 features)  
**Target:** Does a person earn > $50K/year?

#### Pipeline Summary
| Step | Detail |
|---|---|
| Missing values | Mode imputation for `workclass`, `occupation`, `native_country` |
| Encoding | One-Hot Encoding (nominal) + ordinal mapping for `education` (1–16) |
| Scaling | `StandardScaler` on all numeric columns |
| Feature engineering | `capital_net = capital_gain − capital_loss` |
| Feature selection | RFECV → kept 34/54 features (~20% faster training) |
| Split | 80/20 stratified |

#### Results
| Metric | Logistic Regression | Random Forest |
|---|---|---|
| Accuracy | 0.81 | **0.82** |
| Weighted F1 | 0.82 | **0.83** |
| ROC-AUC | 0.909 | **0.915** |

**Best config — Random Forest:** `n_estimators=400`, `max_depth=None`, `bootstrap=True`

---

### 2b — Forest Cover Type Classification (Multi-class)

**Dataset:** UCI Covertype (581,012 rows, 54 features)  
**Target:** 7 tree species (Cover_Type)

#### Pipeline Summary
| Step | Detail |
|---|---|
| Missing values | None — dataset is complete |
| Encoding | Binary flags already 0/1 |
| Scaling | `StandardScaler` applied only for Logistic Regression |
| Feature engineering | `Roadway_to_Elevation`, `slope_ratio` |
| Feature selection | RFECV → kept 35/54 features (~40% faster training) |
| Split | 70/30 stratified |

#### Results
| Metric | Random Forest | Logistic Regression |
|---|---|---|
| Accuracy | **0.95** | 0.72 |
| Macro F1 | **0.93** | 0.51 |
| Weighted F1 | **0.95** | 0.71 |

**Best config — Random Forest:** `n_estimators=500`, `max_depth=None`, `max_features='sqrt'`

---

### Comparative Reflection

| Aspect | Adult Income | Forest Cover |
|---|---|---|
| Task type | Binary classification | 7-class classification |
| Dataset size | ~32K rows | ~581K rows |
| Class imbalance | Moderate (24% positive) | Strong (classes 1&2 ≈ 85%) |
| Key metric | ROC-AUC | Macro F1 |
| Best model | Random Forest (0.915 AUC) | Random Forest (0.93 F1) |

**General lessons learned:**
- Match preprocessing to data — encode and scale only where needed.
- Tree ensembles generalise well across both small and large datasets with minimal tuning.
- Always include a linear baseline to confirm whether non-linearity is actually required.
- Choose evaluation metrics that reflect the business/domain need, not just overall accuracy.

---

## Setup & Requirements

```bash
pip install pymongo pandas scikit-learn matplotlib seaborn
```

MongoDB must be running locally (default: `mongodb://localhost:27017`) for the Big Data project.

---

## License
This repository is submitted as academic coursework for the Machine Learning and Big Data course at the University of Naples Federico II. All datasets used are publicly available (UCI ML Repository, IMDb).
