# Biome Internship Projects

This repository contains the tasks and projects completed during my internship at **Biome**. Each task focuses on a different aspect of data analysis, data quality, and machine learning operations (MLOps), with an emphasis on writing clean, modular, and production-oriented Python code.

---

## Repository Structure

```text
biome-internship-projects/
│
├── .github/
│   └── workflows/
│       └── flake8.yaml
│
├── README.md
│
├── Task1/
│   ├── data/
│   ├── notebook/
│   ├── src/
│   └── requirements.txt
│
├── Task2/
│   ├── data/
│   ├── src/
│   └── requirements.txt
│
└── Task3/
    ├── data/
    ├── src/
    └── requirements.txt
```

---

# Tasks Overview

## Task 1 – Weather Data Profiling

### Objective

Perform comprehensive data profiling on a weather dataset to understand its statistical properties, data quality, and feature distributions through descriptive statistics and visualizations.

### Features

* Dataset overview
* Data type inspection
* Missing value analysis
* Descriptive statistics for numerical features:

  * Mean
  * Median
  * Minimum
  * Maximum
  * First Quartile (Q1)
  * Third Quartile (Q3)
* Mode calculation for categorical features
* Numerical feature visualization
* Correlation analysis
* Modular and reusable profiling pipeline

### Technologies

* Python
* Pandas
* Matplotlib
* Seaborn

---

## Task 2 – Data Drift Detection Using Population Stability Index (PSI)

### Objective

Detect distribution changes between a baseline dataset and a new dataset using the **Population Stability Index (PSI)** implemented **from scratch** without relying on external drift detection libraries.

### Features

* Custom PSI implementation
* Numerical feature comparison
* Distribution visualization
* PSI calculation for each numerical feature
* Automated drift report generation

### Drift Interpretation

|         PSI Score | Interpretation    |
| ----------------: | ----------------- |
|        PSI < 0.10 | No Drift          |
| 0.10 ≤ PSI < 0.25 | Moderate Drift    |
|        PSI ≥ 0.25 | Significant Drift |

### Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn

---

## Task 3 – Weighted Data Rebalancing Strategy

### Objective

Simulate a real-world production scenario where a machine learning model is trained on historical data, but the incoming production data experiences significant distribution drift.

To address this problem, a weighted data combination strategy was implemented.

### Strategy

The algorithm combines:

* **30%** of the original (training) dataset
* **70%** of the drifted (production) dataset

The resulting dataset provides a smoother transition toward the new production distribution while preserving information from the original data.

### Features

* Load original dataset
* Load drifted dataset
* Apply configurable weighted sampling
* Generate a new combined dataset
* Export the final dataset as a CSV file

### Output

The generated CSV can be used for:

* Model retraining
* Continuous learning pipelines
* Dataset rebalancing
* Production model updates

---

## Task 4 - Predict 30-day readmission risk and identify actionable drivers

# Diabetes 130-US Hospitals: 30-Day Readmission Risk Prediction

A production-style machine learning pipeline that predicts whether a diabetic patient will be readmitted to the hospital within 30 days, built on the UCI Diabetes 130-US Hospitals dataset. The project covers the full lifecycle: data cleaning, feature engineering, encoding, model training, handling class imbalance, and model explainability with SHAP.

## Objective

Hospital readmissions within 30 days are a key quality and cost metric for healthcare providers. This project frames the problem as a binary classification task: predict whether a patient will be readmitted within 30 days (`1`) or not (`0`), using structured clinical and administrative data collected during a hospital encounter.

## Dataset

- **Source:** UCI Diabetes 130-US Hospitals dataset
- **Target column:** `readmitted`
- **Target transformation:**
  - `<30` → `1` (readmitted within 30 days)
  - `>30` or `NO` → `0`

## Pipeline Overview

### 1. Data Loading
Raw data loaded from CSV using pandas.

### 2. Preprocessing
- Replaced placeholder values (`?`) with proper missing values.
- Dropped non-informative or leakage-prone identifier columns: `encounter_id`, `patient_nbr`, `weight`.
- Removed invalid or terminal records:
  - Rows where `gender == "Unknown/Invalid"`
  - Rows where `discharge_disposition_id` indicates the patient expired (`11`, `19`, `20`)
- Converted categorical ID columns (`admission_type_id`, `discharge_disposition_id`, `admission_source_id`) into meaningful categories.
- Imputed missing values: `payer_code`, `medical_specialty`, and `race` filled with `"Unknown"`.
- Grouped rare/low-frequency categories in `medical_specialty`, `payer_code`, and `admission_source_id` to reduce dimensionality and noise.

### 3. Feature Engineering
New features created to capture clinical severity and utilization patterns:
- `total_visits`: aggregate of prior outpatient, inpatient, and emergency visits.
- `long_stay`: binary flag based on the 75th percentile of `time_in_hospital`.
- `high_medications`: binary flag based on the 75th percentile of `num_medications`.
- `multiple_diagnoses`: binary flag based on the 75th percentile of `number_diagnoses`.
- Diagnosis grouping for `diag_1`, `diag_2`, and `diag_3` into clinically meaningful categories (e.g., Circulatory, Diabetes, Respiratory).

### 4. Encoding
- **Binary encoding:** `gender`, `change`, `diabetesMed`
- **One-hot encoding:** `race`, `admission_type_id`, `discharge_disposition_id`, `admission_source_id`, `payer_code`, `medical_specialty`, diagnosis groups, medication columns, `max_glu_serum`, `A1Cresult`

### 5. Modeling
- **Split:** `train_test_split` with stratification on the target to preserve class ratio.
- **Scaling:** `StandardScaler` applied only for Logistic Regression, fit on training data and applied to test data. Tree-based models were left unscaled.
- **Models trained:**
  - Logistic Regression (baseline, interpretable)
  - Random Forest
  - XGBoost
- **Evaluation metrics:** Accuracy, Precision, Recall, F1-score, full classification report, and confusion matrix.

### 6. Handling Class Imbalance
Initial models showed poor recall on the minority (readmitted) class. Addressed using class balancing techniques (`class_weight` for Logistic Regression/Random Forest, `scale_pos_weight` for XGBoost) to improve minority class detection, since missing a true readmission is more costly than a false alarm in this domain.

### 7. Explainability (SHAP)
Used SHAP with the XGBoost model to interpret predictions at both global and local levels:
- Global feature importance (bar plot)
- Beeswarm plot for feature impact distribution

**Top contributing features:**
- `number_inpatient`
- `discharge_disposition_id_1`
- `number_diagnoses`
- `num_medications`
- `total_visits`
- `num_lab_procedures`
- `age`
- `diag_1_group_Circulatory`
- `time_in_hospital`

## Project Structure

```
src/
├── preprocessing.py       # Data cleaning and missing value handling
├── feature_engineering.py # Derived feature creation
├── encoding.py             # Binary and one-hot encoding logic
├── model.py                # Model training and evaluation
└── main.py                  # Pipeline entry point
```

## Key Lessons

- Never scale data before the train/test split, scaling on the full dataset leaks test information into training.
- Fit the scaler only on training data, then transform the test set with the same scaler.
- Tree-based models (Random Forest, XGBoost) do not require feature scaling.
- Accuracy alone is a misleading metric on imbalanced datasets like this one.
- Recall and F1-score matter more than accuracy here, since failing to flag a high-risk readmission has real clinical cost.
- SHAP is an effective tool for turning a black-box model into something clinically interpretable, which matters for trust and adoption in healthcare settings.

## Tech Stack

- **Language:** Python
- **Core libraries:** pandas, numpy, scikit-learn, XGBoost
- **Explainability:** SHAP
- **Visualization:** matplotlib / seaborn (for evaluation and SHAP plots)

## How to Run

```bash
# Clone the repository
git clone <repo-url>
cd <repo-folder>

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/main.py
```

## Future Improvements

- Experiment with LightGBM as an additional gradient boosting baseline.
- Add cross-validation for more robust performance estimates.
- Threshold tuning based on precision-recall tradeoff rather than default 0.5.
- Package preprocessing and feature engineering into a scikit-learn `Pipeline`/`ColumnTransformer` for cleaner deployment.
- Add unit tests for preprocessing and feature engineering functions.

## Author

Saim Ansari
Deputy Director, IEEE RAS Technical Team | BS Robotics and Intelligent Systems, Bahria University Islamabad
Portfolio: [saimansari.me](https://saimansari.me) | GitHub: [github.com/saim-ansari-tech](https://github.com/saim-ansari-tech)

---

## Task 5

# Speaker Recognition using ECAPA-TDNN

A deep learning-based speaker recognition system built using **PyTorch** and the **ECAPA-TDNN** architecture. The model is trained to classify speakers from their voice recordings using Log Mel Spectrogram features.

---

## Project Overview

This project implements an end-to-end speaker recognition pipeline consisting of:

- Audio preprocessing
- Log Mel Spectrogram extraction
- Custom PyTorch Dataset
- ECAPA-TDNN model
- Model training
- Model evaluation
- Performance visualization

The objective is to identify the speaker of an input audio sample from a predefined set of speakers.

---

## Features

- Custom PyTorch Dataset
- Log Mel Spectrogram feature extraction
- ECAPA-TDNN architecture
- Cross Entropy Loss
- Adam Optimizer
- Training and evaluation scripts
- Classification Report
- Confusion Matrix
- F1-Score visualization
- Model checkpoint saving

---

## Project Structure

```text
Task_5/
│
├── data/
│   ├── metadata_subset.csv
│   ├── train.csv
│   ├── val.csv
│   └── test.csv
│
├── src/
│   ├── blocks.py
│   ├── config.py
│   ├── dataset.py
│   ├── encode_labels.py
│   ├── evaluate_model.py
│   ├── model.py
│   ├── split_dataset.py
│   └── train.py
│
├── model/
│   └── ecapa_tdnn.pth
│
├── figures/
│   └── f1_scores.png
│
├── requirements.txt
```
---

## Dataset

The dataset contains voice recordings from **100 speakers**.

Dataset split:

| Split | Purpose |
|--------|----------|
| Training | Model learning |
| Validation | Hyperparameter tuning |
| Testing | Final performance evaluation |

Each speaker contains multiple audio recordings.

---

## Model Architecture

The project uses the **ECAPA-TDNN (Emphasized Channel Attention, Propagation and Aggregation Time Delay Neural Network)** architecture.

Pipeline:

```
Audio
   │
   ▼
Log Mel Spectrogram
   │
   ▼
TDNN Blocks
   │
   ▼
Statistics Pooling
   │
   ▼
Embedding Layer
   │
   ▼
Classifier
   │
   ▼
Predicted Speaker
```

---

## Training

Training uses:

- Cross Entropy Loss
- Adam Optimizer
- Mini-batch Gradient Descent

Training process:

```
Audio
      ↓
Mel Spectrogram
      ↓
ECAPA-TDNN
      ↓
Prediction
      ↓
CrossEntropyLoss
      ↓
Backpropagation
      ↓
Weight Update
```

---

## Evaluation

The trained model is evaluated on the test dataset using:

- Test Loss
- Test Accuracy
- Precision
- Recall
- F1 Score
- Classification Report
- Confusion Matrix

Evaluation is performed using:

```python
model.eval()

with torch.no_grad():
```

to disable gradient computation during inference.

---

## Experimental Results

### Training Performance

| Metric | Value |
|--------|---------|
| Final Training Accuracy | **96.93%** |

### Test Performance

| Metric | Value |
|--------|---------|
| Test Accuracy | **74.00%** |
| Test Loss | **1.0003** |

Average Classification Metrics:

| Metric | Score |
|---------|-------|
| Precision | **0.7989** |
| Recall | **0.7400** |
| F1 Score | **0.7389** |

---

## Visualizations

The evaluation generates:

- Confusion Matrix
- Classification Report
- Per-speaker F1 Score Plot

These visualizations help analyze which speakers are correctly recognized and which speakers are frequently confused.

---

## Installation

Clone the repository:

```bash
git clone <repository-link>
cd Task_5
```

Install dependencies:

```bash
pip install torch torchaudio librosa pandas numpy matplotlib scikit-learn
```

---

## Training

Run:

```bash
python train.py
```

The trained model will be saved as:

```
ecapa_tdnn.pth
```

---

## Evaluation

Run:

```bash
python evaluate.py
```

The script will display:

- Test Accuracy
- Test Loss
- Classification Report
- Confusion Matrix
- F1 Score Plot

---

## Technologies Used

- Python
- PyTorch
- Torchaudio
- Librosa
- NumPy
- Pandas
- Matplotlib
- Scikit-Learn

---

## Future Improvements

- Speaker Verification using embeddings
- Data augmentation
- Learning Rate Scheduler
- Early Stopping
- Mixed Precision Training
- ONNX model export
- Real-time microphone inference
- Deployment using FastAPI or Streamlit

---



## Task 6
# Voice Biometric Authentication System using ECAPA-TDNN

A Flask-based web application for **voice biometric authentication** using a pre-trained **ECAPA-TDNN** deep learning model. The system allows users to register their voice and later authenticate themselves by comparing voice embeddings using cosine similarity.

---

## Features

- User Registration
  - Register a unique username.
  - Upload a voice sample.
  - Generate and store speaker embeddings.

- User Authentication
  - Upload a new voice sample.
  - Generate a new embedding.
  - Compare with the stored embedding using cosine similarity.
  - Authenticate based on a configurable similarity threshold.

- Input Validation
  - Unique username validation.
  - Audio file validation.
  - Supported audio formats.
  - Flash messages for user feedback.

---

## Technologies Used

- Python
- Flask
- PyTorch
- Torchaudio
- NumPy
- Scikit-learn
- HTML

---

## Project Structure

```
voice_authentication/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── models/
│   ├── model.py
│   ├── blocks.py
│   └── ecapa_tdnn.pth
│
├── utils/
│   ├── embedding.py
│   ├── file_handler.py
│   ├── preprocessing.py
│   ├── similarity.py
│   └── storage.py
│
├── templates/
│   ├── home.html
│   ├── register.html
│   └── authenticate.html
│
├── uploads/
│
└── embeddings/
```

---

## System Workflow

### Registration

```
User
   │
   ▼
Upload Voice Sample
   │
   ▼
Audio Preprocessing
   │
   ▼
ECAPA-TDNN
   │
   ▼
Speaker Embedding
   │
   ▼
Save Embedding (.npy)
```

---

### Authentication

```
User
   │
   ▼
Upload Voice Sample
   │
   ▼
Generate New Embedding
   │
   ▼
Load Stored Embedding
   │
   ▼
Cosine Similarity
   │
   ▼
Threshold Comparison
   │
   ▼
Authentication Result
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/your-username/voice-authentication.git

cd voice-authentication
```

---

### Create Virtual Environment

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000/
```

---

## Supported Audio Formats

- WAV (Recommended)
- MP3

> **Note:** Windows Voice Recorder saves recordings as `.m4a`, which is not currently supported. Convert `.m4a` files to `.wav` before uploading.

---

## Authentication Threshold

The system authenticates users using cosine similarity.

```python
SIMILARITY_THRESHOLD = 0.75
```

This value can be adjusted based on experimental evaluation.

---

## Example Results

| Test Case | Similarity Score | Result |
|------------|----------------:|--------|
| Same Speaker | 0.8285 | Authentication Successful |
| Different Speaker | 0.7000 | Authentication Failed |

---

## Future Improvements

- Support M4A audio files.
- Automatic audio format conversion.
- Multiple voice samples per user.
- Database integration (SQLite/PostgreSQL).
- User management dashboard.
- Modern responsive UI.
- Docker deployment.
- HTTPS support.

---

## Task 7

# AI Influencer Discovery System

An AI-powered influencer recommendation system that combines Machine Learning, Semantic Search, and a Flask web application to help users discover relevant social media influencers based on their interests.

---

# Project Overview

The AI Influencer Discovery System helps users discover influencers related to their interests using three different approaches.

### 1. Topic Search

Users directly select a topic to view the highest-ranked influencers.

### 2. AI Recommendation

Users describe their interests in natural language. A trained Machine Learning classifier predicts the most relevant topic before recommending influencers.

### 3. Semantic Search

Users enter a free-text query. A pretrained Sentence Transformer model finds semantically similar posts and recommends the most relevant influencers.

The project combines Natural Language Processing (NLP), Machine Learning, Semantic Search, and an engagement-based influencer ranking algorithm.

---

# Features

- Data preprocessing pipeline
- Duplicate record removal
- Timestamp conversion
- English language filtering
- Text cleaning and normalization
- Stopword removal
- Word lemmatization
- TF-IDF feature extraction
- Multi-class text classification
- Automatic model comparison
- AI-based topic prediction
- Semantic search using Sentence Transformers
- Cosine similarity search
- Influencer ranking algorithm
- Flask web application
- Interactive web interface

---

# Supported Topics

- AI
- Finance
- Healthcare
- Fitness
- Travel
- Cricket

---

# System Architecture

```
                    User
                      │
      ┌───────────────┼────────────────┐
      │               │                │
      ▼               ▼                ▼
Topic Search   AI Recommendation   Semantic Search
      │               │                │
      │               ▼                ▼
      │      TF-IDF + ML Model   Sentence Transformer
      │               │                │
      └───────────────┴────────────────┘
                      │
                      ▼
            Influencer Ranking
                      │
                      ▼
          Top Influencer Recommendations
```

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Sentence Transformers
- PyTorch
- NLTK
- Flask
- Joblib

---

# Project Structure

```
AI_Influencer_Discovery/
│
├── artifacts/
│   ├── ranked_influencers.csv
│   ├── post_embeddings.npy
│   ├── tfidf_vectorizer.pkl
│   └── topic_classifier.pkl
│
├── data/
│
├── src/
│   ├── preprocessing.py
│   ├── trainer.py
│   ├── ranking.py
│   ├── inference.py
│   ├── semantic_search.py
│   └── main.py
│
├── templates/
│   ├── index.html
│   ├── topic.html
│   ├── recommend.html
│   └── semantic.html
│
├── static/
│   └── style.css
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Data Preprocessing

The preprocessing pipeline performs the following operations:

- Remove duplicate records
- Convert timestamps
- Merge post text and hashtags
- Detect language
- Keep only English posts
- Convert text to lowercase
- Remove URLs
- Remove mentions
- Remove emojis
- Remove punctuation
- Remove numbers
- Remove stopwords
- Lemmatize words

The cleaned text is stored in the **cleaned_text** column and is later used for both Machine Learning and Semantic Search.

---

# Machine Learning Pipeline

## Feature Extraction

TF-IDF Vectorizer

- Maximum Features: 10,000
- N-grams: (1,2)

## Models Evaluated

- Logistic Regression
- Linear Support Vector Classifier (LinearSVC)
- Multinomial Naive Bayes

The best-performing model is automatically selected and saved for inference.

---

# Semantic Search

Semantic Search is implemented using the pretrained Sentence Transformer model:

```
all-MiniLM-L6-v2
```

Workflow:

```
User Query
      │
      ▼
Sentence Transformer
      │
      ▼
Query Embedding
      │
      ▼
Cosine Similarity
      │
      ▼
Top Similar Posts
      │
      ▼
Influencer Ranking
      │
      ▼
Recommended Influencers
```

Embeddings are generated once from the cleaned posts and stored locally for efficient retrieval.

---

# Influencer Ranking

Each post receives an engagement score using:

```
Engagement Score =
0.5 × Likes
+ 0.3 × Comments
+ 0.2 × Shares
```

Verified accounts receive an additional 10% engagement bonus.

Each influencer is ranked using:

```
Influencer Score =
0.50 × Average Engagement
+ 0.30 × Post Count
+ 0.20 × log(Followers + 1)
```

The influencers are sorted in descending order of the final score.

---

# Web Application

The Flask application provides three modules:

### Topic Search

Select a topic to view the highest-ranked influencers.

### AI Recommendation

Describe your interests in natural language to receive topic-specific influencer recommendations.

### Semantic Search

Search using free text to discover semantically related posts and influencers.

---

# Running the Project

Clone the repository

```bash
git clone <repository-url>
```

Install dependencies

```bash
pip install -r requirements.txt
```

Generate artifacts

```bash
python src/main.py
```

Run the Flask application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# Example

### AI Recommendation

```
Describe what content you are interested in:

Deep learning is transforming healthcare.

Predicted Topic:

AI
```

---

### Semantic Search

```
Search Query:

Mental health is important for everyone.
```

The system retrieves the most semantically similar posts and recommends the highest-ranked influencers related to the query.

---

# Model Performance

The text classification model achieved approximately **99% accuracy** on the test dataset.

Evaluation metrics include:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix






## Task 8 - Multimodel Video Search AI

# VideoMind AI — Multimodal Video Understanding & Search

> **AI-powered video analysis pipeline** that extracts transcripts, generates summaries & chapters, describes visual scenes, and enables natural language semantic search across video content.

---

## Features

| Feature | Description |
|---------|-------------|
| **Video Upload** | Drag & drop or browse MP4, AVI, MOV, MKV files |
| **Scene Detection** | Automatic scene boundary detection using PySceneDetect |
| **Keyframe Extraction** | Extracts representative frames from each detected scene |
| **Audio Transcription** | Whisper Small for fast, accurate speech-to-text |
| **Scene Description** | SmolVLM2-2.2B-Instruct for visual understanding of keyframes |
| **Summary & Chapters** | AI-generated video summary with timestamped chapter markers |
| **Semantic Search** | Natural language queries to find exact moments in videos |
| **Question Answering** | Groq LLM (Llama 3.1) answers questions based on video content |
| **Vector Search** | Qdrant + Sentence Transformers for fast similarity search |

---


## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Upload   │────▶│  Flask Backend   │────▶│  Async Pipeline │
│   (Dashboard)   │     │  (app.py)        │     │  (Threading)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │                            │
                              ▼                            ▼
                        ┌──────────┐              ┌─────────────────┐
                        │  Qdrant  │◀─────────────│  ML Pipeline    │
                        │  Vector  │   Embeddings │  (12 Steps)     │
                        │  Store   │              │                 │
                        └──────────┘              │ 1. Scene Detect │
                              │                   │ 2. Keyframes    │
                              ▼                   │ 3. Audio Extract│
                        ┌──────────┐              │ 4. Whisper      │
                        │  Groq    │◀─────────────│ 5. VLM Scenes   │
                        │  LLM     │   Context    │ 6. Summary      │
                        │  (QA)    │              │ 7. Chapters     │
                        └──────────┘              │ 8. Chunking     │
                                                  │ 9. Embeddings   │
                                                  │ 10. Qdrant Store│
                                                  └─────────────────┘
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'src'` | Create `src/__init__.py` (empty file) |
| `File already exists in output path` | Delete `data/audio.wav` and restart |
| `CUDA out of memory` | Reduce batch size or use CPU: edit `transcription_audio.py` device to `"cpu"` |
| `Qdrant connection refused` | Start Qdrant with Docker, or app auto-falls back to in-memory |
| `GROQ_API_KEY not found` | Add key to `.env` file |
| Processing stuck at 5% | Check terminal logs for ML model errors |
| "Sorry I cannot find this information" | Lower similarity threshold in `app.py` or rephrase query |

---

## Performance Notes

| Component | GPU Time | CPU Time | VRAM |
|-----------|----------|----------|------|
| Whisper Small | ~30s | ~2min | ~2GB |
| SmolVLM2-2.2B | ~1-2min | ~5min | ~5GB |
| Scene Detection | ~10s | ~10s | Minimal |
| Embeddings | ~5s | ~5s | Minimal |
| **Total (5min video)** | **~3-5min** | **~10-15min** | **~7GB** |



## Future Enhancements

- [ ] Multi-video batch processing
- [ ] Real-time video streaming analysis
- [ ] Export results as PDF/Word reports
- [ ] User authentication & video history
- [ ] Support for more languages (multilingual Whisper)
- [ ] Fine-tuned VLM for specific domains
- [ ] WebSocket-based live progress instead of polling



## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, Tailwind CSS, Vanilla JavaScript, Material Symbols |
| **Backend** | Flask (Python) |
| **Scene Detection** | PySceneDetect + OpenCV |
| **Speech Recognition** | Faster-Whisper (OpenAI Whisper) |
| **Vision-Language** | HuggingFaceTB/SmolVLM2-2.2B-Instruct |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Vector Database** | Qdrant |
| **LLM** | Groq API (Llama 3.1 8B Instant) |
| **Audio Extraction** | FFmpeg (via audio_extract) |


## Project Structure

```
VideoMind-AI/
├── app.py                          # Flask application (routes, API)
├── .env                            # Environment variables (GROQ_API_KEY)
│
├── src/                            # Core ML pipeline modules
│   ├── __init__.py
│   ├── pipeline.py                 # Main processing orchestrator
│   ├── scenes_detector.py          # Scene boundary detection
│   ├── frames_extractor.py         # Keyframe extraction (OpenCV)
│   ├── audio_extractor.py          # Audio extraction (FFmpeg)
│   ├── transcription_audio.py      # Whisper transcription
│   ├── scene_description.py        # VLM scene descriptions
│   ├── summary_generator.py        # Summary & chapter generation
│   ├── text_chunker.py             # Transcript chunking
│   ├── embedding_generator.py      # Sentence transformer embeddings
│   ├── vector_store.py             # Qdrant vector database
│   ├── video_store.py              # JSON result persistence
│   ├── question_answering.py       # LLM-based QA
│   └── llm_generator.py            # Groq API client
│
├── templates/                      # Flask HTML templates
│   ├── index.html                  # Dashboard (upload + video list)
│   ├── processing.html             # Real-time processing status
│   ├── results.html                # Video analysis results
│   └── search.html                 # Semantic search interface
│
├── static/
│   ├── css/                        # Page stylesheets
│   │   ├── dashboard.css
│   │   ├── processing.css
│   │   ├── results.css
│   │   └── search.css
│   └── js/                         # Frontend logic
│       ├── dashboard.js            # Upload + video listing
│       ├── processing.js           # Progress polling
│       ├── results.js              # Results display
│       └── search.js               # Semantic search
│
└── data/                           # Generated data (auto-created)
    ├── uploads/                    # Uploaded videos
    ├── audio/                      # Extracted audio files
    ├── keyframes/                  # Scene keyframes
    └── videos/                     # JSON analysis results


## Usage Guide

### Upload a Video

1. Go to the **Dashboard** (`/`)
2. Drag & drop or click **Browse Files** to select a video
3. Click **Process Video**
4. You will be redirected to the **Processing** page with live progress

### Monitor Processing

- Watch real-time pipeline progress (12 steps)
- See live logs, elapsed time, and metadata updates
- Processing typically takes 2-5 minutes for a 5-minute video

### View Results

- **Video Player** — Play your uploaded video
- **Summary** — AI-generated video summary
- **Chapters** — Clickable timestamped chapter markers
- **Transcript** — Full timestamped transcript with search
- **Detected Scenes** — Visual scene descriptions with timestamps
- **Metadata** — Technical details (resolution, codec, models used)

### Semantic Search

1. Go to **Semantic Search** (`/search`)
2. Select a processed video from the dropdown
3. Type a natural language query, e.g.:
   - *"What is this video about?"*
   - *"When does the speaker mention AI?"*
   - *"Explain the part about transformers"*
4. Results show ranked matches with timestamps and confidence scores

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard page |
| `/processing` | GET | Processing status page |
| `/results` | GET | Results display page |
| `/search` | GET | Semantic search page |
| `/upload` | POST | Upload video, start async processing |
| `/status/<video_id>` | GET | Poll processing progress |
| `/video/<video_id>` | GET | Get full analysis results (JSON) |
| `/video_file/<video_id>` | GET | Stream original video file |
| `/ask` | POST | Semantic search / question answering |
| `/videos` | GET | List all processed videos |

### Example: Upload Video

```bash
curl -X POST -F "video=@myvideo.mp4" http://localhost:5000/upload
```

**Response:**
```json
{
  "success": true,
  "video_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Video uploaded. Processing started in background.",
  "status": "processing"
}
```

### Example: Ask a Question

```bash
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "question": "What is this video about?",
    "top_k": 5
  }'
```

**Response:**
```json
{
  "success": true,
  "video_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "question": "What is this video about?",
  "answer": "The video discusses the importance of business model feasibility analysis...",
  "sources": [
    {
      "start_time": 0.0,
      "end_time": 26.86,
      "text": "The speaker stresses the need for thorough business model feasibility analysis...",
      "score": 0.85
    }
  ]
}
=======
The application will run at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.


## Prerequisites

- **Python 3.10+**
- **CUDA-capable GPU** (recommended) or CPU fallback
- **Qdrant** running locally (or use in-memory fallback)
- **FFmpeg** installed and in PATH
- **Groq API Key** (free tier available)

---

## Installation

### 1. Clone & Setup Environment

```bash
git clone <your-repo-url>
cd VideoMind-AI

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install flask flask-cors
pip install faster-whisper transformers torch accelerate
pip install sentence-transformers qdrant-client
pip install scenedetect opencv-python-headless
pip install audio-extract python-dotenv
pip install groq
```

### 3. Configure Environment

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at: [https://console.groq.com](https://console.groq.com)

### 4. Start Qdrant (Optional)

```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant

# Or use in-memory fallback (data lost on restart)
# No action needed — the app falls back automatically
```



















## Task 9 - Sementic Document Search
# Semantic Document Search System

A semantic document search system that retrieves relevant document passages based on **meaning rather than exact keyword matching**.

Traditional keyword search can fail when users use different words to describe the same concept. For example, a user searching for:

> "How do I reset my password?"

may not find a document containing:

> "Account credential recovery steps"

even though the document is highly relevant.

This project solves this problem using **semantic embeddings** and **vector similarity search**. Documents are loaded, split into meaningful chunks, converted into vector embeddings, stored in a Qdrant vector database, and retrieved using natural-language queries.

An optional Gemini-powered RAG component generates a concise answer based only on the retrieved document context.

---

## Features

* Upload documents through a Flask web interface.
* Supports:

  * `.txt`
  * `.pdf`
  * `.docx`
* Automatic document type detection.
* Document loading using LangChain document loaders.
* Splitting of long documents into smaller meaningful chunks.
* Semantic embeddings using `all-MiniLM-L6-v2`.
* Local vector storage using Qdrant.
* Natural-language semantic search.
* Top-K relevant passages retrieval.
* Similarity scores for retrieved results.
* Gemini-powered AI answers based on retrieved context.
* Displays both:

  * AI-generated answer
  * Retrieved document passages

---

## System Architecture

```text
                    User
                     │
                     ▼
              Flask Web Interface
                     │
                     │ Upload Document
                     ▼
              File Type Detection
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
         TXT        PDF        DOCX
          │          │          │
          ▼          ▼          ▼
     TextLoader  PyPDFLoader  Docx2txtLoader
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
              Loaded Documents
                     │
                     ▼
       RecursiveCharacterTextSplitter
                     │
                     ▼
                Text Chunks
                     │
                     ▼
          Hugging Face Embeddings
          all-MiniLM-L6-v2
                     │
                     ▼
                Vector Embeddings
                     │
                     ▼
               Qdrant Vector DB
                     │
                     │
                     │ User Query
                     ▼
             Query Embedding
                     │
                     ▼
            Similarity Search
                     │
                     ▼
                Top-K Chunks
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
       Search Results     Gemini LLM
              │             │
              │             ▼
              │        AI Generated
              │           Answer
              │             │
              └──────┬──────┘
                     │
                     ▼
                Flask UI
```

---

## Project Workflow

### 1. Document Upload

The user uploads a supported document through the Flask web application.

Supported formats:

```text
.txt
.pdf
.docx
```

The application determines the document type based on its file extension.

---

### 2. Document Loading

LangChain document loaders are used to extract the content.

| File Type | Loader           |
| --------- | ---------------- |
| TXT       | `TextLoader`     |
| PDF       | `PyPDFLoader`    |
| DOCX      | `Docx2txtLoader` |

The output is converted into LangChain `Document` objects.

---

### 3. Document Splitting

Long documents are divided into smaller chunks using:

```python
RecursiveCharacterTextSplitter
```

The current configuration uses:

```text
Chunk Size: 500
Chunk Overlap: 50
```

Chunking improves retrieval because the embedding model can represent smaller, focused sections of the document.

---

### 4. Embedding Generation

Each document chunk is converted into a numerical vector using:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The embedding represents the semantic meaning of the text.

For example:

```text
Query:
How can I recover my account?

Document:
Steps for account credential recovery
```

Even though the exact words are different, their semantic meaning can be similar in vector space.

---

### 5. Vector Storage

The generated embeddings are stored in a local Qdrant vector database.

Qdrant runs locally using Docker.

The application connects to:

```text
http://localhost:6333
```

Qdrant is responsible for storing vectors and performing similarity searches.

---

### 6. Semantic Search

When the user enters a query:

```text
What are the requirements for weather forecasting?
```

the query is converted into an embedding using the same embedding model.

The query vector is then compared with the document vectors stored in Qdrant.

The system retrieves the most semantically similar document chunks.

The result contains:

```text
Document Chunk
Similarity Score
Metadata
```

---

### 7. AI Answer Generation

The retrieved chunks are passed to Gemini as context.

The LLM is instructed to answer the user's question using only the retrieved document context.

The final interface displays:

```text
AI Answer
    │
    ▼
Gemini-generated response

Search Results
    │
    ├── Retrieved Chunk 1
    ├── Retrieved Chunk 2
    └── Retrieved Chunk 3
```

This architecture follows the basic principles of a **Retrieval-Augmented Generation (RAG)** system.

---

## Technologies Used

### Backend

* Python
* Flask

### Document Processing

* LangChain
* `TextLoader`
* `PyPDFLoader`
* `Docx2txtLoader`
* `RecursiveCharacterTextSplitter`

### Embeddings

* Hugging Face
* Sentence Transformers
* `all-MiniLM-L6-v2`

### Vector Database

* Qdrant
* Docker

### LLM

* Google Gemini

### Frontend

* HTML
* CSS
* JavaScript

---


=======
```text
semantic_doc_search/
│
├── app.py
│
├── main.py
│
├── requirements.txt
│
├── .env
│
├── src/
│   ├── __init__.py
│   │
│   ├── document_loader.py
│   │
│   ├── document_splitter.py
│   │
│   ├── vector_store.py
│   │
│   ├── sementic_search.py
│   │
│   └── llm_generator.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── css/
│       └── style.css
│
└── data/
    └── documents/

---




### 5. Run the Application
=======
## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd semantic_doc_search
```

---

### 2. Create a Virtual Environment

Using Conda:

```bash
conda create -n semantic_doc_search python=3.12
```

Activate the environment:

```bash
conda activate semantic_doc_search
```

Or using Python's built-in virtual environment:

```bash
python -m venv venv
```

Activate on Windows:

```powershell
venv\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Qdrant Setup

Qdrant is used as the local vector database.

Make sure Docker Desktop is running.

Start Qdrant using:

```bash
docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
```

The Qdrant server will be available at:

```text
http://localhost:6333
```

To verify that the container is running:

```bash
docker ps
```

To stop Qdrant:

```bash
docker stop qdrant
```

To start it again:

```bash
docker start qdrant
```

---

## Gemini API Configuration

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit your `.env` file to GitHub.

Add the following to `.gitignore`:

```text
.env
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```


Open your browser: **http://localhost:5000**

---



---

## Using the Application

### Step 1: Upload a Document

Upload a supported document:

```text
TXT
PDF
DOCX
```

The system will:

```text
Upload
   ↓
Load Document
   ↓
Split Document
   ↓
Generate Embeddings
   ↓
Store Embeddings in Qdrant
```

---

### Step 2: Enter a Query

Enter a natural-language question.

Example:

```text
What are the basic requirements for weather trend forecasting?
```

---

### Step 3: Perform Semantic Search

The system will:

```text
Query
   ↓
Generate Query Embedding
   ↓
Search Qdrant
   ↓
Retrieve Top-K Chunks
```

---

### Step 4: Generate AI Answer

The retrieved chunks are provided to Gemini.

The model generates an answer based on the retrieved document context.

The interface displays:

```text
AI Answer
```

and:

```text
Search Results
```

with similarity scores.

---

## Example

### Document

A document contains:

```text
Basic Assessment

Data Cleaning & Preprocessing
Handle missing values, outliers, and normalize data.

Exploratory Data Analysis
Perform basic EDA to uncover trends, correlations, and patterns.

Model Building
Build a basic forecasting model and evaluate its performance.
```

### Query

```text
What are the requirements for the basic weather forecasting assessment?
```

### Semantic Search

The system retrieves relevant passages even if the query does not exactly match the document wording.

### AI Answer

The LLM generates an answer based on the retrieved context.

---

## RAG Pipeline

The complete Retrieval-Augmented Generation pipeline is:

```text
             DOCUMENT INGESTION
                     │
                     ▼
              Load Documents
                     │
                     ▼
               Split Documents
                     │
                     ▼
             Generate Embeddings
                     │
                     ▼
              Store in Qdrant
                     │
                     │
                     │
             USER QUERY
                     │
                     ▼
             Embed User Query
                     │
                     ▼
            Vector Similarity Search
                     │
                     ▼
              Retrieve Top-K
                     │
                     ▼
             Retrieved Context
                     │
                     ▼
                 Gemini
                     │
                     ▼
             Generated Answer
```

---



## License

MIT License — feel free to use, modify, and distribute.

---

## Credits

**Developed by:** Muhammad Saim Ansari  
**Organization:** Biome Analytics  
**Internship Project:** Multimodal Video Understanding & Search

**Powered by:**
- OpenAI Whisper
- Hugging Face SmolVLM
- Sentence Transformers
- Qdrant Vector Database
- Groq LLM Inference
- Flask Web Framework

---
=======
## Limitations

* The current system primarily supports unstructured text documents.
* CSV files are not currently included in the main document ingestion workflow.
* Retrieval quality depends on the selected embedding model.
* Very large documents may require optimized chunking strategies.
* Semantic similarity does not guarantee exact structured filtering.
* The system depends on the quality and relevance of retrieved chunks.
* The LLM is restricted to the retrieved context to reduce hallucinations.

---

## Future Improvements

Potential improvements include:

* Support for additional document formats.
* Improved document-specific chunking strategies.
* Metadata filtering.
* Hybrid keyword + semantic search.
* Reranking retrieved documents.
* Improved embedding models.
* Persistent document and collection management.
* Multi-document search.
* Document deletion and replacement.
* Query history.
* Streaming LLM responses.
* Authentication and user management.
* Production deployment.
* Evaluation using retrieval metrics such as Precision@K, Recall@K, and MRR.

---

## Key Concepts Demonstrated

This project demonstrates practical implementation of:

* Natural Language Processing
* Semantic Search
* Text Embeddings
* Vector Databases
* Nearest-Neighbor Search
* Document Chunking
* Retrieval-Augmented Generation (RAG)
* Large Language Models
* Flask Web Applications

---


# Code Quality

This repository follows Python coding best practices and includes automated code quality checks using **Flake8**.

GitHub Actions automatically runs linting on every push through the workflow located at:

```text
.github/workflows/flake8.yaml
```

---

# Requirements

Each task contains its own `requirements.txt` file containing the required Python dependencies.

Install the dependencies for a task using:

```bash
pip install -r requirements.txt
```

---

# Skills Demonstrated

* Python Programming
* Data Profiling
* Exploratory Data Analysis (EDA)
* Data Visualization
* Population Stability Index (PSI)
* Data Drift Detection
* Machine Learning Data Monitoring
* Dataset Rebalancing
* MLOps Concepts
* Git & GitHub
* GitHub Actions
* Flake8
* Modular Project Structure

---

# Internship

This repository serves as a collection of projects completed during my internship at **Biome**, demonstrating practical applications of data analysis, data quality assessment, and production-oriented machine learning workflows.


## Author

**Muhammad Saim Ansari**

BS Robotics and Intelligent Systems

Bahria University Islamabad

## License

This project is intended for educational and research purposes.