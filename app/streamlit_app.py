"""
Keratoconus Severity Staging - Streamlit Web Application
Interactive web app for predicting keratoconus severity using Pentacam parameters.
"""

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="KC Severity Predictor",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-box {
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin: 2rem 0;
    }
    .stage-0 { background-color: #d4edda; border: 2px solid #28a745; }
    .stage-1 { background-color: #d1ecf1; border: 2px solid #17a2b8; }
    .stage-2 { background-color: #fff3cd; border: 2px solid #ffc107; }
    .stage-3 { background-color: #f8d7da; border: 2px solid #fd7e14; }
    .stage-4 { background-color: #f5c6cb; border: 2px solid #dc3545; }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    """Load the trained model."""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.parent  # Go up one level from app/ to project root
    model_path = script_dir / "models" / "rf_kc_severity.pkl"
    
    # Debug: show the path being checked
    st.sidebar.write(f"🔍 Looking for model at: {model_path}")
    st.sidebar.write(f"📁 File exists: {model_path.exists()}")
    
    if model_path.exists():
        return joblib.load(model_path)
    else:
        st.error(f"❌ Model file not found at: {model_path}")
        st.error("Please run: python run_pipeline.py")
        st.stop()


def get_severity_info(stage: int):
    """Get clinical information for each severity stage."""
    info = {
        0: {
            "name": "Stage 0 - Normal",
            "description": "Clear cornea with normal thickness and visual acuity",
            "color": "#28a745",
            "class": "stage-0"
        },
        1: {
            "name": "Stage 1 - Mild KC",
            "description": "Fleischer's ring may be present, mild corneal thinning",
            "color": "#17a2b8",
            "class": "stage-1"
        },
        2: {
            "name": "Stage 2 - Moderate KC",
            "description": "Fleischer's ring and Vogt's striae, evident thinning",
            "color": "#ffc107",
            "class": "stage-2"
        },
        3: {
            "name": "Stage 3 - Advanced KC",
            "description": "Munson's sign, significant thinning with faint scarring",
            "color": "#fd7e14",
            "class": "stage-3"
        },
        4: {
            "name": "Stage 4 - Severe KC",
            "description": "Corneal scarring and opacities, evident Munson's sign",
            "color": "#dc3545",
            "class": "stage-4"
        }
    }
    return info.get(stage, info[0])


def create_gauge_chart(stage: int):
    """Create a gauge chart for severity visualization."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=stage,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Severity Stage", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 4], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 1], 'color': '#d4edda'},
                {'range': [1, 2], 'color': '#d1ecf1'},
                {'range': [2, 3], 'color': '#fff3cd'},
                {'range': [3, 4], 'color': '#f8d7da'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': stage
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="white",
        font={'color': "darkblue", 'family': "Arial"}
    )
    
    return fig


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">👁️ Keratoconus Severity Staging System</div>', 
                unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Automated Severity Classification using Machine Learning</div>', 
                unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/visible.png", width=80)
        st.title("About")
        st.info("""
        This application predicts keratoconus severity (Stages 0-4) using three corneal parameters:
        
        - **Rm_B**: Posterior radius of curvature
        - **Rm_F**: Anterior radius of curvature
        - **Pachy_Min**: Thinnest pachymetry
        
        **Model Performance:**
        - Accuracy: ~78%
        - Method: Random Forest
        - Features: 3
        """)
        
        st.warning("⚠️ **Disclaimer**: Educational tool using synthetic data. Not for clinical diagnosis.")
        
        st.markdown("---")
        st.markdown("**Clinical Stages:**")
        st.caption("""
        • Stage 0: Normal cornea
        • Stage 1: Mild KC
        • Stage 2: Moderate KC
        • Stage 3: Advanced KC
        • Stage 4: Severe KC
        """)
    
    # Main content
    st.markdown("## 📊 Enter Corneal Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Posterior Radius (Rm_B)")
        rm_b = st.slider(
            "Rm_B (mm)",
            min_value=4.0,
            max_value=8.0,
            value=6.5,
            step=0.1,
            help="Posterior corneal surface curvature radius"
        )
        st.caption(f"Current: **{rm_b} mm**")
    
    with col2:
        st.markdown("### Anterior Radius (Rm_F)")
        rm_f = st.slider(
            "Rm_F (mm)",
            min_value=5.0,
            max_value=9.0,
            value=7.8,
            step=0.1,
            help="Anterior corneal surface curvature radius"
        )
        st.caption(f"Current: **{rm_f} mm**")
    
    with col3:
        st.markdown("### Thinnest Pachymetry")
        pachy_min = st.slider(
            "Pachy_Min (µm)",
            min_value=200,
            max_value=600,
            value=520,
            step=5,
            help="Minimum corneal thickness"
        )
        st.caption(f"Current: **{pachy_min} µm**")
    
    st.markdown("---")
    
    # Predict button
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        predict_button = st.button("🔍 Predict Severity", type="primary", use_container_width=True)
    
    if predict_button:
        # Prepare input (unscaled - direct values)
        input_data = pd.DataFrame({
            'Rm_B': [rm_b],
            'Rm_F': [rm_f],
            'Pachy_Min': [pachy_min]
        })
        
        # Make prediction
        with st.spinner("Analyzing corneal parameters..."):
            try:
                prediction = model.predict(input_data)[0]
                probabilities = model.predict_proba(input_data)[0]
            except Exception as e:
                st.error(f"Prediction error: {str(e)}")
                st.info("Please retrain the model: python run_pipeline.py")
                st.stop()
        
        # Get severity info
        severity = get_severity_info(int(prediction))
        
        # Display results
        st.markdown("## 📋 Prediction Results")
        
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.markdown(f"""
            <div class="prediction-box {severity['class']}">
                <h2 style="color: {severity['color']}; margin: 0;">{severity['name']}</h2>
                <p style="font-size: 1.1rem; margin-top: 1rem;">{severity['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Clinical recommendations
            st.markdown("### 💊 Clinical Recommendations")
            if prediction == 0:
                st.success("✅ Normal cornea. Regular follow-up recommended.")
            elif prediction == 1:
                st.info("ℹ️ Mild KC. Consider corneal cross-linking consultation. Spectacles or soft contact lenses.")
            elif prediction == 2:
                st.warning("⚠️ Moderate KC. Corneal cross-linking recommended. Rigid contact lenses may be needed.")
            elif prediction == 3:
                st.warning("⚠️ Advanced KC. Corneal cross-linking and specialty contact lenses. Consider surgical options.")
            else:
                st.error("🚨 Severe KC. Surgical intervention likely required (corneal ring implant or transplant).")
        
        with col_res2:
            # Gauge chart
            st.plotly_chart(create_gauge_chart(int(prediction)), use_container_width=True)
            
            # Probability distribution
            st.markdown("### 📊 Confidence Distribution")
            prob_df = pd.DataFrame({
                'Stage': [f'Stage {i}' for i in range(5)],
                'Probability': probabilities * 100
            })
            
            fig_bar = go.Figure(data=[
                go.Bar(
                    x=prob_df['Stage'],
                    y=prob_df['Probability'],
                    marker_color=['#28a745', '#17a2b8', '#ffc107', '#fd7e14', '#dc3545'],
                    text=[f'{p:.1f}%' for p in prob_df['Probability']],
                    textposition='auto'
                )
            ])
            fig_bar.update_layout(
                title="Prediction Confidence by Stage",
                xaxis_title="Severity Stage",
                yaxis_title="Probability (%)",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p><strong>Keratoconus Severity Staging System</strong> | Educational & Research Tool</p>
        <p>Machine Learning-based automated classification</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
