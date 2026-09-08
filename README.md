# FoodGuardAI: AI-Based Food Adulteration and Quality Detection System

An end-to-end artificial intelligence and computer vision platform to evaluate packaged food products, detect potential adulteration indicators, screen harmful additives, and assess overall dietary quality.

---

## Key Features

1. **Barcode Scanning Module**:
   - Live camera barcode reader (`html5-qrcode`) with real-time detection.
   - Global product database lookup via **Open Food Facts REST API**.
   - Verified offline catalog fallback for fast testing (Maggi, Oreo, Lay's, Amul Ghee, test cases).

2. **Ingredient Label & OCR Module**:
   - Upload or snap packaging ingredient photos.
   - Dual OCR engine: Computer Vision preprocessing with **OpenCV** (CLAHE contrast equalization, bilateral denoising, adaptive Gaussian thresholding) and **Tesseract.js** in-browser WebAssembly OCR.
   - Editable extracted ingredient text area for user verification and tuning.

3. **Multi-Model Machine Learning Engine**:
   - 3,500+ realistic packaged food product dataset across 8 distinct categories.
   - Comparative evaluation across 4 algorithms:
     - **Gradient Boosting Classifier**: **99.86% F1-Score** (Top Model)
     - **Random Forest Classifier**: **99.71% F1-Score**
     - **Decision Tree Classifier**: **99.43% F1-Score**
     - **Logistic Regression**: **98.57% F1-Score**
   - Feature engineering: Bad Fat Index, Sugar-to-Fiber Ratio, and Additive Density Score.
   - Explainable predictions with positive vs negative risk driver breakdowns.

4. **Food Adulteration Detection & Regulatory Knowledge Base**:
   - Screens for non-permitted industrial dyes (**Metanil Yellow, Sudan I-IV**).
   - Screens for heavy metal colorants (**Lead Chromate** in turmeric).
   - Screens for synthetic milk concoctions (**Urea, Detergent, Caustic Soda**).
   - Screens for toxic adulterant oils (**Argemone Oil** in mustard oil).
   - Flags prohibited dough conditioners (**Potassium Bromate E924**).
   - Flags industrial trans fats and excessive chemical preservatives (**TBHQ, BHA/BHT, Benzoates**).

5. **Modern Dashboard UI**:
   - **Quality Score Gauge**: Animated score from 0 to 100.
   - **Risk Level Badges**: Safe / Low Risk, Moderate Risk, High Risk.
   - **Nutritional Traffic Light Profiling**: Sugar, Sodium, Saturated/Trans Fats, Energy, Protein, Fiber.
   - **Scan History**: Full audit trail with search and risk filters stored in SQLite.
   - **ML Benchmarks Explorer**: Interactive confusion matrix and feature importance charts.
   - **Safety Disclaimer**: Emphasizes AI preliminary screening vs certified laboratory chemical testing.

---

## Technology Stack

- **Frontend**: React 19, Vite, Tailwind CSS v4, Lucide Icons, Html5-Qrcode, Tesseract.js
- **Backend**: Python 3.14, FastAPI, Uvicorn, SQLAlchemy, Pydantic v2, Requests
- **Machine Learning & CV**: Scikit-learn, Pandas, NumPy, OpenCV, Joblib
- **Database**: SQLite (zero-config, self-contained persistence)

---

## Quick Start Guide

### 1. Start the Backend API
Run the batch file or terminal command:
```bash
run_backend.bat
```
Or manually:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
API documentation available at: `http://127.0.0.1:8000/docs`

### 2. Start the Frontend
Run the batch file or terminal command:
```bash
run_frontend.bat
```
Or manually:
```bash
cd frontend
npm run dev
```
Open browser at: `http://localhost:3000`

---

## Project Structure

```
FINALYEARPROJECT/
├── backend/
│   ├── app/
│   │   ├── main.py                     # FastAPI application & endpoints
│   │   ├── database.py                 # SQLite database configuration
│   │   ├── models.py                   # SQLAlchemy ScanRecord model
│   │   ├── schemas.py                  # Pydantic request/response schemas
│   │   └── services/
│   │       ├── adulteration_service.py # Adulteration rules & knowledge base
│   │       ├── ocr_service.py          # OpenCV computer vision filters
│   │       └── openfoodfacts_service.py# Open Food Facts API & offline catalog
│   ├── ml/
│   │   ├── dataset_generator.py        # Generates 3,500 labeled products
│   │   ├── train_models.py             # Trains & compares 4 ML algorithms
│   │   ├── predict.py                  # Inference engine & explainability
│   │   ├── data/
│   │   │   └── food_products_dataset.csv
│   │   └── models/
│   │       ├── best_food_quality_model.joblib
│   │       └── model_comparison_metrics.json
│   └── test_backend.py                 # Automated backend verification test
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.jsx              # Navigation header
│   │   ├── pages/
│   │   │   ├── Home.jsx                # Landing page & quick test samples
│   │   │   ├── BarcodeScanner.jsx      # Live camera & manual barcode input
│   │   │   ├── IngredientScanner.jsx   # OCR image upload & presets
│   │   │   ├── ProductAnalysis.jsx     # Score gauge, risk & adulterant alerts
│   │   │   ├── ScanHistory.jsx         # SQLite history log & filters
│   │   │   └── ModelExplorer.jsx       # Benchmark charts & confusion matrix
│   │   ├── App.jsx                     # Core application coordinator
│   │   ├── main.jsx
│   │   └── index.css                   # Tailwind CSS setup
│   ├── package.json
│   └── vite.config.js
├── run_backend.bat                     # Windows launch script for API
├── run_frontend.bat                    # Windows launch script for React UI
└── README.md
```
