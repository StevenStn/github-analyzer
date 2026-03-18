import streamlit as st
import pandas as pd
from github_api import fetch_all_data
from scorer import get_score_breakdown
from report import generate_report

st.set_page_config(
    page_title="GitHub Repository Analyzer",
    page_icon="",
    layout="wide"
)

st.title("GitHub Repository Intelligence Analyzer")
st.markdown("Analyze GitHub repositories — activity, complexity, and learning difficulty.")

# Input
st.subheader("Enter GitHub Repository URLs")
default_repos = "\n".join([
    "https://github.com/c2siorg/Webiu",
    "https://github.com/c2siorg/b0bot",
    "https://github.com/OWASP/Nettacker",
    "https://github.com/tensorflow/tensorflow",
    "https://github.com/facebook/react",
])
urls_input = st.text_area("One URL per line", value=default_repos, height=150)
token_input = st.text_input("GitHub Token (optional — increases rate limit)", type="password")

if st.button("Analyze Repositories"):
    urls = [u.strip() for u in urls_input.strip().split("\n") if u.strip()]
    if not urls:
        st.error("Please enter at least one URL.")
    else:
        # Inject token
        if token_input:
            import github_api
            github_api.GITHUB_TOKEN = token_input
            github_api.HEADERS["Authorization"] = f"token {token_input}"

        results = []
        progress = st.progress(0)
        status = st.empty()

        for i, url in enumerate(urls):
            status.text(f"Fetching {url}...")
            data = fetch_all_data(url)
            score = get_score_breakdown(data)
            results.append(score)
            progress.progress((i + 1) / len(urls))

        status.text("Done!")
        report = generate_report(results)

        # Summary metrics
        s = report["summary"]
        st.subheader("Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Repos Analyzed", report["successful"])
        col2.metric("Avg Activity", s["avg_activity_score"])
        col3.metric("Avg Complexity", s["avg_complexity_score"])
        col4.metric("Beginner", s["beginner_count"])
        col5.metric("Intermediate", s["intermediate_count"])

        # Difficulty breakdown
        st.subheader("Difficulty Distribution")
        diff_data = {
            "Difficulty": ["Beginner", "Intermediate", "Advanced"],
            "Count": [s["beginner_count"], s["intermediate_count"], s["advanced_count"]]
        }
        st.bar_chart(pd.DataFrame(diff_data).set_index("Difficulty"))

        # Detailed table
        st.subheader("Detailed Results")
        successful = report["repositories"]
        if successful:
            df = pd.DataFrame(successful)[[
                "repo", "difficulty", "activity_score",
                "complexity_score", "stars", "forks",
                "commits", "contributors", "last_updated"
            ]]
            df.columns = [
                "Repo", "Difficulty", "Activity",
                "Complexity", "Stars", "Forks",
                "Commits", "Contributors", "Last Updated"
            ]

            def color_difficulty(val):
                colors = {
                    "Beginner": "background-color: #1D9E75; color: white",
                    "Intermediate": "background-color: #378ADD; color: white",
                    "Advanced": "background-color: #D85A30; color: white"
                }
                return colors.get(val, "")

            styled = df.style.applymap(color_difficulty, subset=["Difficulty"])
            st.dataframe(styled, use_container_width=True)

        # Per-repo detail
        st.subheader("Per Repository Details")
        for repo in successful:
            with st.expander(f"{repo['repo']} — {repo['difficulty']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Activity Score", repo["activity_score"])
                    st.metric("Stars", repo["stars"])
                    st.metric("Commits", repo["commits"])
                    st.metric("Last Updated", repo["last_updated"])
                with col2:
                    st.metric("Complexity Score", repo["complexity_score"])
                    st.metric("Forks", repo["forks"])
                    st.metric("Contributors", repo["contributors"])
                    st.metric("Difficulty", repo["difficulty"])
                st.write(f"**Languages:** {', '.join(repo['languages'])}")
                st.write(f"**Description:** {repo['description']}")
                st.write(f"**URL:** {repo['url']}")

        # Errors
        if report["errors"]:
            st.subheader("Failed Repos")
            for err in report["errors"]:
                st.error(err.get("error", "Unknown error"))

        # Download JSON
        import json
        st.download_button(
            label="Download Full Report (JSON)",
            data=json.dumps(report, indent=2),
            file_name="github_analysis_report.json",
            mime="application/json"
        )