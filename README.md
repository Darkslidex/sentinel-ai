# Sentinel AI

**A portfolio demo that brings three independent "AI for security" modules under one dashboard:** computer-vision perimeter detection, a machine-learning fraud classifier and a Streamlit monitoring interface.

> **Status: showcase, not a production product.** The three modules work on their own but **are not connected to each other**, and part of the dashboard uses simulated data. See [What is real and what is demo](#what-is-real-and-what-is-demo) before judging it.

## The three modules

### 1. Vision Sentinel (the strongest piece)
Perimeter intrusion detector built on **YOLOv8**. It watches a webcam or RTSP stream, defines a **polygonal restricted zone** and, when a person enters it, saves an evidence capture to `data/captures/` with a 3-second cooldown so the disk does not fill up. The check uses the bottom-center of the person's bounding box (the feet) with `cv2.pointPolygonTest`, which is the right geometry for perimeter detection.
→ `src/vision/detector.py`

### 2. Anti-Fraud Engine
Fraud classifier using **Random Forest + SMOTE** to balance the minority class. It trains, predicts and reports metrics, but **only on synthetic data** generated with `make_classification` (about 1% fraud). It does not ingest real transactions.
→ `src/fraud/engine.py` · demo in `notebooks/test_fraud_engine.py`

### 3. Command Center (Streamlit dashboard)
Monitoring UI with the vision feed, an evidence history and a "forensic replay" that re-injects real images from the history. It includes an attack simulation that adds rows to a session table.
→ `src/api/app.py` (a **Streamlit** app, not an HTTP API)

## Run it

Requires **Python 3.10+**.

```bash
git clone https://github.com/Darkslidex/sentinel-ai.git
cd sentinel-ai
pip install -r requirements.txt

streamlit run src/api/app.py          # dashboard
python notebooks/test_fraud_engine.py # fraud engine demo (synthetic data)
```

The interface and console output are in Spanish.

## What is real and what is demo

**Real and working:**
- Intrusion detection in a polygonal ROI with evidence capture (`VisionSentinel`).
- Training and metrics of the `FraudDetector`, on synthetic data.
- The forensic replay re-injects real images from the history.

**Simulated or cosmetic (not computed live):**
- The "real-time transaction pulse" chart is fed by `np.random`, not by the fraud engine.
- The dashboard metrics ("model health 99.2%", "precision 0.97", "recall 0.99", "F1 0.98") are **hard-coded literals**.
- "Protected capital" is a fixed formula (`$13950 + captures × 500`), not a calculation from real events.
- The "async" refresh is synchronous (`time.sleep(1)` + `st.rerun()`).
- The fraud engine is **not imported** by the dashboard: the two pieces are disconnected.

## About the fraud metrics

SMOTE is applied **only to the training split**; the test split keeps the original class distribution (about 1% fraud), so synthetic samples never leak into evaluation. An earlier version balanced the data before splitting, which inflated the results; that was fixed.

On the bundled synthetic data both the plain model and the SMOTE model score close to 1.00, because `make_classification` produces easily separable classes. The demo shows the pattern (split first, balance only the training data, report per-class metrics), not real-world fraud performance.

## Security

YOLO checkpoints are deserialized with pickle, so `VisionSentinel` only accepts official Ultralytics weights (an allowlist) and does not patch `torch.load` globally.

## Architecture

- Clean modular split by domain: `src/vision`, `src/fraud`, `src/api`.
- Well-encapsulated `FraudDetector` (`is_trained` state, reusable model and SMOTE, logging in the core).
- Evidence capture with a time-based cooldown (`save_evidence`).

## Next steps

1. **Connect the pieces:** feed the dashboard with real `FraudDetector` metrics and real `VisionSentinel` events instead of `np.random` and literals.
2. **Real fraud data:** replace `make_classification` with a realistic public dataset.
3. **Pin dependencies:** fix exact `torch` and `ultralytics` versions after testing the detector.
4. **Real tests:** `notebooks/test_fraud_engine.py` is a demo script, not a unit test suite.

## Stack

Python · Ultralytics YOLOv8 · OpenCV · NumPy · scikit-learn · imbalanced-learn · pandas · Streamlit

## License

Portfolio project by **Félix Lezama**.
