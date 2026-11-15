import json
import pandas as pd
import streamlit as st
from pathlib import Path

from src.meeting_ai import (
    analyze_transcript,
    check_ollama_connection,
    clean_transcript,
    result_to_csv,
)

st.set_page_config(
    page_title="AI Meeting Notes Generator",
    page_icon="📝",
    layout="wide",
)

st.title("📝 AI-Powered Meeting Notes & Action Item Generator")
st.caption("Local meeting transcript analysis using Ollama + Gemma 3 4B")

with st.sidebar:
    st.header("⚙️ Settings")
    ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")
    model_name = st.text_input("Model name", value="gemma3:4b")
    st.markdown("---")
    st.markdown("**Privacy note**")
    st.caption(
        "This app sends the transcript to your local Ollama service. "
        "Use only sample or consented transcripts. Do not expose the local "
        "Ollama service to the public internet."
    )
    if st.button("Check Ollama connection", use_container_width=True):
        ok, message = check_ollama_connection(ollama_url, model_name)
        if ok:
            st.success(message)
        else:
            st.error(message)

sample_files = {
    "Product launch planning": "product_launch.txt",
    "Website bug review": "website_bug_review.txt",
    "Unclear / noisy meeting": "noisy_meeting.txt",
}

def load_selected_sample():
    choice = st.session_state.get("sample_choice", "-- Choose a sample --")
    if choice in sample_files:
        sample_path = Path(__file__).parent / "samples" / sample_files[choice]
        st.session_state["transcript_input"] = sample_path.read_text(encoding="utf-8")

st.session_state.setdefault("transcript_input", "")
st.selectbox(
    "Try a sample transcript",
    ["-- Choose a sample --", *sample_files.keys()],
    key="sample_choice",
    on_change=load_selected_sample,
)

uploaded = st.file_uploader("Or upload a transcript (.txt)", type=["txt"])
if uploaded is not None:
    st.session_state["transcript_input"] = uploaded.getvalue().decode("utf-8", errors="replace")

transcript = st.text_area(
    "Meeting transcript",
    height=260,
    key="transcript_input",
    placeholder="Paste a meeting transcript here. Include speaker names when possible.",
    help="For best results, include speaker names and preserve explicit task owners and dates.",
)

col_a, col_b = st.columns([1, 4])
with col_a:
    analyze_clicked = st.button("✨ Generate meeting notes", type="primary", use_container_width=True)
with col_b:
    st.caption(f"Characters: {len(transcript):,} / 30,000")

if analyze_clicked:
    cleaned = clean_transcript(transcript)
    if not cleaned:
        st.warning("Please paste or upload a transcript first.")
    elif len(cleaned) > 30000:
        st.error("This demo accepts up to 30,000 characters. Split a longer transcript into sections.")
    else:
        with st.spinner(f"Gemma is analyzing the transcript using {model_name}..."):
            try:
                result = analyze_transcript(cleaned, ollama_url, model_name)
                st.session_state["meeting_result"] = result
                st.session_state["source_transcript"] = cleaned
                st.success("Analysis completed. Review the output before sharing it.")
            except Exception as exc:
                st.error(f"Could not analyze the transcript: {exc}")
                st.info(
                    "Check that Ollama is running, the model is installed, "
                    "and the model name is exactly gemma3:4b."
                )

result = st.session_state.get("meeting_result")
if result:
    st.markdown("---")
    st.header("📌 Generated meeting notes")
    st.warning(
        "AI-generated notes may omit context or misinterpret speech. "
        "Verify every owner, date, decision and task against the original transcript."
    )

    st.subheader(result.get("meeting_title", "Meeting"))
    st.caption(f"Meeting date: {result.get('meeting_date', 'Not specified')}")

    st.markdown("### Summary")
    st.write(result.get("summary", ""))

    left, right = st.columns(2)
    with left:
        st.markdown("### Key discussion points")
        for item in result.get("key_points", []):
            st.markdown(f"- {item}")
        st.markdown("### Decisions")
        decisions = result.get("decisions", [])
        if decisions:
            for item in decisions:
                st.markdown(f"- {item}")
        else:
            st.caption("No explicit decisions extracted.")
    with right:
        st.markdown("### Open questions")
        questions = result.get("open_questions", [])
        if questions:
            for item in questions:
                st.markdown(f"- {item}")
        else:
            st.caption("No open questions extracted.")
        st.markdown("### Risks and blockers")
        risks = result.get("risks_or_blockers", [])
        if risks:
            for item in risks:
                st.markdown(f"- {item}")
        else:
            st.caption("No risks or blockers extracted.")

    st.markdown("### Action items")
    actions = result.get("action_items", [])
    if actions:
        df = pd.DataFrame(actions)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇️ Download action items as CSV",
            data=result_to_csv(actions),
            file_name="meeting_action_items.csv",
            mime="text/csv",
        )
    else:
        st.info("No explicit action items were identified in this transcript.")

    st.download_button(
        "⬇️ Download complete notes as JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name="meeting_notes.json",
        mime="application/json",
    )
    with st.expander("View source transcript used for this analysis"):
        st.text(st.session_state.get("source_transcript", ""))
