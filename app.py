import streamlit as st
from src.helper import extract_text_from_pdf, ask_groq
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs


st.set_page_config(page_title="Job Recommender", page_icon=":briefcase:", layout="wide")
st.title("Job Recommender")
st.markdown(
    "Welcome to the Job Recommender! This app helps you find job listings based on your resume."
)

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file:
    with st.spinner("Processing your resume..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
            st.success("Resume processed successfully!")
            # st.text_area("Extracted Resume Text", value=resume_text, height=300)
        except Exception as e:
            st.error(f"Error processing resume: {e}")
    with st.spinner("Summarizing your resume..."):
        try:
            prompt = f"Summarize the following resume highlighting the skills,education and experience:\n\n{resume_text}"
            summary = ask_groq(prompt)
            st.success("Resume summary generated successfully!")
            st.text_area("Resume Summary", value=summary, height=600)
        except Exception as e:
            st.error(f"Error generating summary: {e}")
    with st.spinner("Finding skill gaps..."):
        try:
            prompt = f"analyse this resume and highlight missing skills,certifications and experience for better job opportunities:\n\n{resume_text}"
            skill_gaps = ask_groq(prompt)
            st.success("Skill gaps identified successfully!")
            st.text_area("Identified Skill Gaps", value=skill_gaps, height=600)
        except Exception as e:
            st.error(f"Error identifying skill gaps: {e}")
    with st.spinner("Finding future roadmap..."):
        try:
            prompt = f"Based on the resume, suggest a future roadmap for the next 3 months to improve skills , job prospects ,projects and career:\n\n{resume_text}"
            roadmap = ask_groq(prompt)
            st.success("Roadmap generated successfully!")
            st.text_area("Suggested Roadmap", value=roadmap, height=600)
        except Exception as e:
            st.error(f"Error generating roadmap: {e}")

    # Display nicely formatted results
    # st.subheader("Resume Analysis Results")
    # st.markdown("### Resume Summary")
    # st.write(summary)
    # st.markdown(
    #     f"<div style='background-color: #f0f0f0; padding: 15px; border-radius: 5px;'>{resume_text}</div>",
    #     unsafe_allow_html=True,
    # )
    # st.markdown("### Identified Skill Gaps")
    # st.write(skill_gaps)
    # st.markdown(
    #     f"<div style='background-color: #f0f0f0; padding: 15px; border-radius: 10px;'>{skill_gaps}</div>",
    #     unsafe_allow_html=True,
    # )
    # st.markdown("### Suggested Roadmap")
    # st.write(roadmap)
    # st.markdown(
    #     f"<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>{roadmap}</div>",
    #     unsafe_allow_html=True,
    # )
    st.success("All tasks completed successfully!")

    if st.button("Fetch Job Listings"):
        with st.spinner("Fetching job listings..."):
            try:
                search_summary = ask_groq(
                    f"Based on the resume summary, what job titles should I search for?Give me comma seperated list only,no explaination.\n\n Summary: {summary}",
                    max_tokens=40,
                )
                search_query = search_summary.replace(
                    "\n", ""
                ).strip()  # Use the summary as the search query

                st.success(f"Job listings fetched successfully!:{search_query}")
                with st.spinner("Displaying job listings..."):
                    #     linkedin_jobs = fetch_linkedin_jobs(search_query, rows=35)
                    naukri_jobs = fetch_naukri_jobs(search_query, rows=60)
                # st.subheader("LinkedIn Job Listings")
                # if linkedin_jobs:
                #     for job in linkedin_jobs:
                #         st.write(f"**Title:** {job.get('title')}")
                #         st.write(f"**Company:** {job.get('company')}")
                #         st.write(f"**Location:** {job.get('location')}")
                #         st.write(f"**Link:** [View Job]({job.get('link')})")
                #         st.markdown("---")
                # else:
                #     st.warning("No LinkedIn jobs found.")

                st.subheader("Naukri Job Listings")
                if naukri_jobs:
                    for job in naukri_jobs:
                        st.write(f"**Title:** {job.get('title')}")
                        st.write(f"**Company:** {job.get('company')}")
                        st.write(f"**Location:** {job.get('location')}")
                        st.write(f"**Link:** [View Job]({job.get('jdURL')})")
                        st.markdown("---")
                else:
                    st.warning("No Naukri jobs found.")

            except Exception as e:
                st.error(f"Error fetching job listings: {e}")
