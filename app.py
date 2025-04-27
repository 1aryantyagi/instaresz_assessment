import streamlit as st
from main import MasterAgent

# Instantiate MasterAgent
master_agent = MasterAgent()

# Custom CSS for styling
st.markdown("""
    <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
        }
        .health-btn {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .analyze-btn {
            background-color: #2196F3;
            color: white;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
        }
        .card {
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .subheader {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .error {
            color: #D32F2F;
        }
        .success {
            color: #388E3C;
        }
    </style>
""", unsafe_allow_html=True)

# Streamlit App
st.markdown('<div class="title">Company Analysis App</div>', unsafe_allow_html=True)

# Health Check Button
if st.button("Check Server Health", key="health_check", help="Check if the server is running smoothly"):
    st.success("Everything is fine ✅", icon="✅")

# Input for Company Name
company_name = st.text_input("Enter Company Name:")

# Analyze Company Button
if st.button("Analyze Company", key="analyze", help="Click to analyze the company's data"):
    if company_name.strip() == "":
        st.markdown('<p class="error">Please enter a company name.</p>', unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing..."):
            analysis, use_cases, resources = master_agent.execute_workflow(company_name)

            # Display Results
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Analysis")

            # Format analysis as bullet points
            analysis_text = f"""
            **Industry:** {analysis.get('industry', 'N/A')}\n\n
            **Market Position:** {analysis.get('market_position', 'N/A')}\n\n
            **Key Offerings:**
            {''.join([f'- {item}\\n' for item in analysis.get('key_offerings', [])])}\n\n
            **Strategic Focus:**
            {''.join([f'- {item}\\n' for item in analysis.get('strategic_focus', [])])}
            """
            st.markdown(analysis_text)
            st.markdown('</div>', unsafe_allow_html=True)

            # Use Cases Section
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Use Cases")

            for i, use_case in enumerate(use_cases, 1):
                with st.expander(f"Use Case {i}: {use_case.get('use_case', '')}", expanded=False):
                    st.markdown(f"**Market Trend:** {use_case.get('market_trend', 'N/A')}")
                    st.markdown("**Implementation Steps:**")
                    for j, step in enumerate(use_case.get('implementation_steps', []), 1):
                        st.markdown(f"{j}. {step}")
                        
            st.markdown('</div>', unsafe_allow_html=True)

            # Resources Section
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Resources")

            for i, resource in enumerate(resources, 1):
                with st.expander(f"Resource {i}: Implementation Details", expanded=False):
                    if resource.get('implementation_plan'):
                        st.markdown("**Implementation Plan:**")
                        for step in resource.get('implementation_plan', []):
                            st.markdown(f"**Step {step.get('step', '')}:** {step.get('description', '')}")
                    
                    if resource.get('models'):
                        st.markdown("**Recommended Models:**")
                        for model in resource.get('models', []):
                            st.markdown(f"- [{model.get('name', '')}]({model.get('url', '')}) ({model.get('platform', '')})")
                    
                    if resource.get('research_papers'):
                        st.markdown("**Research Papers:**")
                        for paper in resource.get('research_papers', []):
                            authors = ", ".join(paper.get('authors', []))
                            st.markdown(f"- **{paper.get('title', '')}** by {authors}  \n[{paper.get('url', '')}]")

            st.markdown('</div>', unsafe_allow_html=True)
