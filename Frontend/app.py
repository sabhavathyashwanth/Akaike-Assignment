import streamlit as st
import pandas as pd
import base64
import requests
import json
import os

# Backend API URL (set via environment variable in Hugging Face Spaces settings)
API_URL = os.environ.get("API_URL", "http://localhost:7860/api")

# Create the Streamlit app
def main():
    st.set_page_config(
        page_title="Financial News Analyzer",
        page_icon="📊",
        layout="wide"
    )

    st.title("📈 Financial News Analyzer")
    st.markdown("""
    This app analyzes recent news articles for publicly-traded companies and provides sentiment analysis, 
    topic extraction, and comparative analysis. It also generates a summary in Hindi with audio.
    """)

    # Get user input
    company_input = st.text_input("Enter company stock symbols (e.g., TSLA, GOOGL, AAPL):", "AAPL")
    companies = [symbol.strip().upper() for symbol in company_input.split(",")]

    if st.button("Analyze News"):
        if not companies or companies[0] == "":
            st.error("Please enter at least one company symbol.")
        else:
            for company in companies:
                st.markdown(f"## 📊 Processing {company}")
                progress_bar = st.progress(0)
                status_text = st.empty()

                # First API call - fetch news data
                status_text.text(f"🔍 Fetching news for {company}...")
                response = requests.post(f"{API_URL}/news/fetch", json={"company": company})
                progress_bar.progress(50)  # Set to 50% after fetch

                if response.status_code == 200:
                    csv_b64 = response.json()["file"]
                    status_text.text(f"✅ Raw news data fetched")

                    # Second API call - analyze the news data
                    status_text.text(f"🔬 Analyzing news data for {company}...")
                    analysis_response = requests.post(
                        f"{API_URL}/news/analyze",
                        json={"company": company, "file": csv_b64}
                    )
                    progress_bar.progress(100)  # Set to 100% after analysis

                    if analysis_response.status_code == 200:
                        result = analysis_response.json()
                        output_data = result["output_data"]
                        audio_b64 = result["audio_file"]
                        output_file = result["output_file"]
                        json_str = result["json_str"]

                        status_text.text(f"✅ Analysis complete!")

                        # Display the results in tabs
                        tab1, tab2, tab3, tab4 = st.tabs(["Summary", "Articles", "Comparative Analysis", "Raw Data"])

                        with tab1:
                            st.subheader("Final Sentiment Analysis")
                            st.write(output_data["Final Sentiment Analysis"])

                            st.subheader("Hindi Translation")
                            st.write(output_data["Hindi Translation"])

                            # Audio player
                            st.audio(base64.b64decode(audio_b64), format="audio/mp3")

                            # Download link for audio
                            audio_link = f'<a href="data:audio/mp3;base64,{audio_b64}" download="{company}_news_summary_hindi.mp3">Download Hindi Audio Summary</a>'
                            st.markdown(audio_link, unsafe_allow_html=True)

                        with tab2:
                            st.subheader("Article Analysis")
                            for idx, article in enumerate(output_data["Articles"]):
                                with st.expander(f"{idx + 1}. {article['Title']}"):
                                    st.write(f"*Summary:* {article['Summary']}")
                                    st.write(f"*Sentiment:* {article['Sentiment']}")
                                    st.write(
                                        f"*Topics:* {', '.join(article['Topics']) if article['Topics'] else 'No topics identified'}")

                        with tab3:
                            st.subheader("Sentiment Distribution")
                            sentiment_dist = output_data["Comparative Sentiment Score"]["Sentiment Distribution"]
                            sentiment_df = pd.DataFrame({
                                "Sentiment": list(sentiment_dist.keys()),
                                "Count": list(sentiment_dist.values())
                            })
                            st.bar_chart(sentiment_df.set_index("Sentiment"))

                            st.subheader("Topic Analysis")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write("*Common Topics:*")
                                common_topics = output_data["Comparative Sentiment Score"]["Topic Analysis"][
                                    "Common Topics"]
                                if common_topics:
                                    for topic in common_topics:
                                        st.write(f"- {topic}")
                                else:
                                    st.write("No common topics found.")

                            with col2:
                                st.write("*Unique Topics:*")
                                unique_topics = output_data["Comparative Sentiment Score"]["Topic Analysis"][
                                    "Unique Topics"]
                                if unique_topics:
                                    for topic in unique_topics:
                                        st.write(f"- {topic}")
                                else:
                                    st.write("No unique topics found.")

                            st.subheader("Contradictions")
                            contradictions = output_data["Comparative Sentiment Score"]["Contradictions"]
                            if contradictions:
                                for contradiction in contradictions:
                                    st.write(f"- *{contradiction['Topic']}:* {contradiction['Contradiction']}")
                            else:
                                st.write("No contradictions found.")

                            st.subheader("Coverage Differences")
                            differences = output_data["Comparative Sentiment Score"]["Coverage Differences"]
                            if differences:
                                for i, diff in enumerate(differences[:5]):  # Show first 5 differences
                                    st.write(f"*Difference {i + 1}:*")
                                    st.write(f"- {diff['Comparison']}")
                                    st.write(f"- {diff['Impact']}")
                            else:
                                st.write("No significant coverage differences found.")

                        with tab4:
                            st.subheader("Raw JSON Output")
                            st.json(output_data)

                            # Download button for JSON
                            st.download_button(
                                label="Download JSON",
                                data=json_str,
                                file_name=output_file,
                                mime="application/json"
                            )
                    else:
                        try:
                            error_msg = analysis_response.json().get('error', 'Unknown error')
                            st.error(f"❌ Error analyzing data: {error_msg}")
                        except ValueError:
                            st.error(f"❌ Error analyzing data: Server error (Status {analysis_response.status_code})")
                else:
                    try:
                        error_msg = response.json().get('error', 'Unknown error')
                        st.error(f"❌ {error_msg}")
                    except ValueError:
                        st.error(f"❌ Server error (Status {response.status_code})")

if __name__ == "__main__":
    main()