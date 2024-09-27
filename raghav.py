import streamlit as st
import requests

st.title("Job Description Matcher")
st.write("Upload a PDF of your resume and paste the job description. The app will analyze the fit.")

api_url = st.text_input("Enter API URL", value="http://localhost:8000/relevant_resume_jd_info")
st.warning("Currently, using local URL. Replace it , when deployed")
pdf_file = st.file_uploader("Upload your resume (PDF format)", type="pdf")
job_description = st.text_area("Enter Job Description", height=200)

# When the user clicks the submit button
if st.button("Submit"):
    if pdf_file and job_description and api_url:
        pdf_content = pdf_file.read()

        if not pdf_content:
            st.error("Uploaded PDF file is empty. Please upload a valid resume.")
        else:
            with st.spinner("Processing... this may take a while (20-30 seconds)."):
                files = {
                    'file': (pdf_file.name, pdf_content, 'application/pdf')  # Ensure proper format
                }
                data = {
                    'job_description': job_description  # Job description
                }

                try:
                    response = requests.post(api_url, files=files, data=data)

                    if response.status_code == 200:
                        result = response.json()
                        st.success("Success!")

                  
                        st.session_state.result = result

                       
                        required_work_experience = result['work_experience']['required_workExperience']
                        total_years = result['work_experience']['total_years']
                        experience_score = result['work_experience']['experience_score']
                        score_explanation = result['work_experience']['score_explanation']
                        list_of_suggestions = result['final_suggestions']['list_of_suggestions']
                        cosine_similarity = result['cosine_similarity']

                      
                        st.subheader("Relevant Information")
                        st.write(f"**Required Work Experience:** {required_work_experience}")
                        st.write(f"**Total Years of Experience:** {total_years}")
                        st.write(f"**Experience Score:** {experience_score}")
                        st.write(f"**Score Explanation:** {score_explanation}")
                        st.write(f"**Cosine Similarity:** {cosine_similarity:.2f}")
                        st.write("**Suggestions:**")
                        for suggestion in list_of_suggestions:
                            st.write(f"- {suggestion}")

                    else:
                        st.error(f"Error from API: {response.status_code}, {response.text}")

                except Exception as e:
                    st.error(f"Failed to connect to the API. Error: {e}")

    else:
        st.warning("Please upload both your resume, provide the job description, and specify the API URL.")

if 'result' in st.session_state:
    if st.button("See Entire JSON Response"):
        st.json(st.session_state.result)
