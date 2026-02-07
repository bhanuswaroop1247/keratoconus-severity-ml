# Keratoconus Severity Staging using Machine Learning

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4+-orange.svg)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌐 Live Demo

**[Try the Live Application →](https://your-app-name.streamlit.app)** *(Update after deployment)*

---

## 📋 Overview

An end-to-end machine learning system for automated keratoconus severity staging (Stages 0-4) using corneal tomography parameters. This project demonstrates a complete ML pipeline from data generation through model deployment.

### Key Features
- ✅ **~78% Cross-Validation Accuracy** with Random Forest classification
- ✅ **Minimal Features**: Only 3 corneal parameters required
- ✅ **Complete Pipeline**: Data → Preprocessing → Training → Web App
- ✅ **Interactive Deployment**: Streamlit web application
- ✅ **Production-Ready**: Modular, documented, reproducible code

---

## 🎯 Clinical Context

**Keratoconus (KC)** is a progressive corneal disease causing:
- Corneal thinning and irregular curvature
- Visual impairment and astigmatism
- Potential vision loss if untreated

**This system provides:**
- Automated severity classification (5 stages)
- Standardized diagnostic support
- Early detection capability

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Complete Pipeline
```bash
python run_pipeline.py
```
⏱️ Takes 5-10 minutes to complete all steps

### 3. Launch Web Application
```bash
streamlit run app/streamlit_app.py
```
Opens at `http://localhost:8501`

---

## 📊 Dataset

### Synthetic Pentacam Data
Uses synthetically generated corneal tomography data based on published clinical ranges.

**Specifications:**
- **Features**: 3 key Pentacam parameters
- **Samples**: 650 corneas
- **Classes**: 5 severity stages (0-4)
- **Distribution**: Balanced across all stages

**Selected Features:**
- **Rm_B**: Posterior radius of curvature
- **Rm_F**: Anterior radius of curvature
- **Pachy_Min**: Thinnest pachymetry

---

## 🏗️ Project Structure

```
keratoconus-severity-ml/
│
├── data/
│   ├── raw/                      # Synthetic data
│   └── processed/                # Preprocessed data
│
├── src/
│   ├── data_generator.py         # Data generation
│   ├── preprocessing.py          # Data cleaning
│   ├── feature_selection.py      # Feature selection
│   ├── train.py                  # Model training
│   └── evaluate.py               # Performance evaluation
│
├── models/
│   ├── rf_kc_severity.pkl        # Trained model
│   └── *.png                     # Visualizations
│
├── app/
│   └── streamlit_app.py          # Web interface
│
├── .streamlit/
│   └── config.toml               # Streamlit config
│
├── run_pipeline.py               # Master script
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## 🔬 Methodology

### 1. Data Generation
Synthetic data with severity-dependent distributions:
- **Stage 0** (Normal): Pachy_Min ~520µm, Rm_B ~6.5mm
- **Stage 4** (Severe): Pachy_Min ~400µm, Rm_B ~4.9mm

### 2. Preprocessing
- Simple data validation
- Feature extraction
- No complex scaling needed

### 3. Feature Selection
Uses 3 clinically relevant features:
- `Rm_B` - Posterior radius of curvature
- `Rm_F` - Anterior radius of curvature
- `Pachy_Min` - Thinnest pachymetry

### 4. Model Training
- **Algorithm**: Random Forest
- **Validation**: 6-fold cross-validation
- **Hyperparameters**: Optimized via GridSearchCV

### 5. Performance

| Metric | Score |
|--------|-------|
| Cross-Val Accuracy | ~78% |
| Training Accuracy | 100% |

---

## 📱 Web Application

### Features
- Input sliders for 3 corneal parameters
- Real-time severity prediction
- Confidence visualization with gauge chart
- Probability distribution bar chart
- Clinical recommendations per stage

### Test Cases

| Stage | Rm_B | Rm_F | Pachy_Min |
|-------|------|------|-----------|
| 0 (Normal) | 6.4 mm | 7.7 mm | 518 µm |
| 2 (Moderate) | 5.7 mm | 7.0 mm | 448 µm |
| 4 (Severe) | 4.6 mm | 6.0 mm | 395 µm |

---

## 💻 Technical Stack

- **Language**: Python 3.9+
- **ML Framework**: scikit-learn
- **Data**: pandas, numpy
- **Visualization**: matplotlib, seaborn, plotly
- **Web**: Streamlit
- **Deployment**: Streamlit Community Cloud

---

## 🌐 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**:
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Deploy**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Set main file: `app/streamlit_app.py`
   - Deploy!

3. **Your app will be live at**: `https://your-username-keratoconus-severity-ml.streamlit.app`

---

## 📝 For Your Resume

```
• Developed end-to-end ML system for keratoconus severity staging achieving 
  78% cross-validation accuracy using Random Forest on corneal tomography data

• Engineered complete data pipeline with synthetic data generation (650 samples), 
  feature selection (3 key parameters), and 6-fold cross-validation

• Deployed production-ready Streamlit web application on Streamlit Cloud with 
  real-time prediction, interactive visualizations, and clinical decision support

• Established industry-standard GitHub repository with modular Python codebase 
  and comprehensive documentation following software engineering best practices

• Skills: Python, scikit-learn, Streamlit, Machine Learning, Data Visualization, 
  Cloud Deployment, Healthcare AI
```

---

## 🎓 Skills Demonstrated

1. **Machine Learning**: Classification, ensemble methods, cross-validation
2. **Feature Engineering**: Selection, dimensionality reduction
3. **Data Science**: Synthetic data generation, model evaluation
4. **Software Engineering**: Modular design, documentation, reproducibility
5. **Web Development**: Full-stack deployment with Streamlit
6. **Cloud Deployment**: Streamlit Community Cloud
7. **Domain Knowledge**: Healthcare AI, medical diagnostics

---

## ⚠️ Disclaimer

This system uses synthetically generated data for educational and research purposes. It is:
- ✅ Suitable for ML methodology demonstration
- ✅ Valid for academic projects and portfolios
- ❌ **NOT** for clinical diagnosis without validation on real data
- ❌ **NOT** a substitute for professional medical evaluation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Pudi Bhanu Swaroop**  
Ophthalmic Engineering Student, IIT Hyderabad

- 📧 Email: op24mtech11001@iith.ac.in
- 💼 LinkedIn: https://www.linkedin.com/in/bhanu-swaroop-pudi-927a701aa/
- 🐙 GitHub: https://github.com/bhanuswaroop1247

---

## 🙏 Acknowledgments

- Pentacam corneal tomography standards
- scikit-learn community
- Streamlit framework
- IIT Hyderabad

---

**⭐ Star this repository if you found it helpful!**

**🌐 [View Live Demo](https://your-app-name.streamlit.app)** *(Update after deployment)*
