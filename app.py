import streamlit as st
from phi.tools.tavily import TavilyTools
from dotenv import load_dotenv
load_dotenv()  # This loads the environment variables from a .env file situated in the same directory as this script.

from assistant import get_research_assistant  # type: ignore

st.set_page_config(
page_title="Llama 3 Search Engine",
page_icon=":mag:",
)
st.title("Llama 3 Search Engine")
st.markdown("##### Powered by Groq")

def main() -> None:
    # Get model
    llm_model = st.sidebar.selectbox(
        "Select Model", options=["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768"]
    )
    # Set assistant_type in session state
    if "llm_model" not in st.session_state:
        st.session_state["llm_model"] = llm_model
    # Restart the assistant if assistant_type has changed
    elif st.session_state["llm_model"] != llm_model:
        st.session_state["llm_model"] = llm_model
        st.rerun()

    # Get topic for report
    input_topic = st.text_input(
        "What would you like to search?",
        value="Llama 3 models",
    )
    # Button to generate report
    generate_report = st.button("Search")
    if generate_report:
        st.session_state["topic"] = input_topic

    st.sidebar.markdown("## Trending Topics")
    if st.sidebar.button("Superfast Llama 3 inference on Groq Cloud"):
        st.session_state["topic"] = "Llama 3 on Groq Cloud"

    if st.sidebar.button("AI in Healthcare"):
        st.session_state["topic"] = "AI in Healthcare"

    if st.sidebar.button("Language Agent Tree Search"):
        st.session_state["topic"] = "Language Agent Tree Search"

    if st.sidebar.button("Chromatic Homotopy Theory"):
        st.session_state["topic"] = "Chromatic Homotopy Theory"

    if "topic" in st.session_state:
        report_topic = st.session_state["topic"]
        research_assistant = get_research_assistant(model=llm_model)
        tavily_search_results = None

        with st.status("Searching Web", expanded=True) as status:
            with st.container():
                tavily_container = st.empty()
                tavily_search_results = TavilyTools().web_search_using_tavily(report_topic)
                if tavily_search_results:
                    tavily_container.markdown(tavily_search_results)
            status.update(label="Web Search Complete", state="complete", expanded=False)

        if not tavily_search_results:
            st.write("Sorry report generation failed. Please try again.")
            return

        with st.spinner("Generating Report"):
            final_report = ""
            final_report_container = st.empty()
            for delta in research_assistant.run(tavily_search_results):
                final_report += delta  # type: ignore
                final_report_container.markdown(final_report)

    st.sidebar.markdown("---")
    if st.sidebar.button("Restart"):
        st.rerun()


main()

