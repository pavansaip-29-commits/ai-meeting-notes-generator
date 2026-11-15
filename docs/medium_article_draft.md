# Building an AI-Powered Meeting Notes and Action Item Generator with Python, Streamlit and Ollama

*By [Your Name] | Practical AI Engineering Project*

## 1. Introduction

Meetings are an important part of teamwork, but converting long discussions into clear notes takes time. A person must listen to the discussion, identify important decisions, remember who accepted each task and record deadlines. Important details can be missed, especially when several people speak or the meeting transcript contains errors.

In this project, I built an AI-powered Meeting Notes and Action Item Generator. The application accepts a text transcript and uses the Gemma 3 4B language model through Ollama to produce a structured meeting summary and a list of action items. Streamlit provides the user interface.

The project is designed as a practical workflow-assistance tool. It supports note preparation, but a human should review the output before sharing or assigning work.

## 2. Problem statement

Manually preparing meeting notes can be repetitive and time-consuming. It can also be difficult to separate a confirmed decision from an idea that was only discussed. Action owners and deadlines may be missing or unclear.

**Objective:** Build a local application that processes a meeting transcript and generates a concise summary, key discussion points, decisions, open questions, risks and structured action items.

## 3. Tools and technologies

- **Python:** application logic and transcript processing.
- **Streamlit:** interactive web interface.
- **Ollama:** local runtime that exposes the model through an HTTP API.
- **Gemma 3 4B:** language model used to interpret the transcript.
- **Requests:** sends the transcript to the local Ollama API.
- **Pandas:** displays extracted action items in a table.
- **Pytest:** tests preprocessing and output utility functions.
- **VS Code and GitHub:** development and version control.

No paid cloud LLM API key is required for the default local setup.

## 4. System architecture

[ADD YOUR ARCHITECTURE DIAGRAM HERE]

The workflow contains these stages:

1. **Transcript input:** The user pastes meeting text or uploads a `.txt` file.
2. **Preprocessing:** The application normalizes line endings and repeated whitespace and checks that the transcript is not empty or too long.
3. **LLM request:** Python sends the transcript and extraction instructions to Ollama's `/api/chat` endpoint.
4. **Model processing:** Gemma 3 4B identifies the topic, summary, decisions and possible action items.
5. **Structured output:** The request asks Ollama to return a JSON object with defined fields.
6. **Output normalization:** Python checks the returned structure and supplies safe defaults for missing fields.
7. **Presentation:** Streamlit displays notes and provides JSON and CSV downloads.

## 5. Implementation

### Step 1: Install and prepare the tools

I installed Python, VS Code and Ollama on Windows. I downloaded the model with:

```powershell
ollama pull gemma3:4b
```

I created a Python virtual environment and installed the project dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Step 2: Connect Python to Ollama

Ollama provides a local HTTP API. The application sends a request to:

```text
http://localhost:11434/api/chat
```

The request includes the model name, system and user messages, `stream: false`, and a JSON schema. Structured output helps the application receive predictable fields instead of an unstructured paragraph.

### Step 3: Process the transcript

The preprocessing function performs conservative cleanup. It normalizes line endings, removes repeated spaces and reduces excessive blank lines. It does not attempt to rewrite sentences or guess missing words, because doing so could change the meeting's meaning.

### Step 4: Extract meeting information

The prompt instructs the model to distinguish decisions from proposals and to extract only action items supported by the transcript. When an owner or deadline is missing, the expected value is `Not specified`. Each action item also contains an evidence phrase to help a person check it against the transcript.

### Step 5: Display and export results

Streamlit displays the summary, discussion points, decisions, open questions, risks and action items. The user can download the full result as JSON and action items as CSV.

[ADD SCREENSHOT: INPUT SCREEN]

[ADD SCREENSHOT: GENERATED SUMMARY AND DECISIONS]

[ADD SCREENSHOT: ACTION ITEMS TABLE]

## 6. Testing and observations

I tested the application with three sample transcripts:

| Test | Transcript characteristics | What to inspect |
|---|---|---|
| 1 | Product launch planning with named owners and dates | Summary, owners and deadlines |
| 2 | Website bug review with an unconfirmed cause | Whether the model avoids presenting a guess as a fact |
| 3 | Noisy transcript with uncertain dates and unclear speaker attribution | Whether uncertainty and missing owners are preserved |

**Actual test results — complete this after running the app:**

| Test | Summary quality | Action extraction quality | Errors or omissions |
|---|---|---|---|
| Product launch | [ADD YOUR OBSERVATION] | [ADD YOUR OBSERVATION] | [ADD YOUR OBSERVATION] |
| Bug review | [ADD YOUR OBSERVATION] | [ADD YOUR OBSERVATION] | [ADD YOUR OBSERVATION] |
| Noisy transcript | [ADD YOUR OBSERVATION] | [ADD YOUR OBSERVATION] | [ADD YOUR OBSERVATION] |

Measured response time: [ADD ACTUAL TIME AND COMPUTER SPECIFICATIONS]

Do not fill this section with assumed results. Compare every generated task with the source transcript and note any incorrect or missing information.

## 7. Challenges and limitations

- **Missing context:** A transcript may not explain what a pronoun such as "it" refers to.
- **Transcription errors:** Incorrect words or names can change the meaning of a discussion.
- **Speaker attribution:** If speaker labels are missing or wrong, the model may assign a task to the wrong person.
- **Ambiguous deadlines:** Phrases such as "later this week" may not identify an exact date.
- **Model limitations:** A small local model may omit details, misunderstand complex discussions or generate unsupported content.
- **Long transcripts:** This demo limits input to 30,000 characters. Longer meetings should be split into sections and reviewed carefully.
- **Human verification:** Generated notes are suggestions, not an authoritative meeting record.

## 8. Lessons learned

This project demonstrated how a local language model can be integrated into a Python application. I learned how to call an LLM through an HTTP API, provide structured output instructions, validate model responses and present the results in a Streamlit interface.

I also learned that a fluent summary is not necessarily a correct summary. Action owners, deadlines and decisions must be checked against the original transcript. Showing missing information explicitly is safer than guessing.

## 9. Future improvements

- Add audio transcription using a speech-to-text model.
- Support PDF, DOCX and audio uploads.
- Add transcript chunking for long meetings.
- Allow users to edit and approve extracted tasks.
- Add meeting history with secure storage.
- Evaluate extraction quality using a labelled test dataset.

## 10. Conclusion

The AI-Powered Meeting Notes and Action Item Generator demonstrates a practical use of language models in everyday work. By combining Python, Streamlit, Ollama and Gemma 3 4B, the application turns a transcript into structured notes and possible next steps.

The system can reduce repetitive note preparation, but it should remain a human-reviewed assistant. Accurate transcripts, clear speaker labels and verification are important for reliable results.

## 11. References

1. Ollama API documentation — https://docs.ollama.com/api
2. Ollama structured outputs — https://ollama.com/blog/structured-outputs
3. Streamlit documentation — https://docs.streamlit.io/
4. Gemma 3 model library — https://ollama.com/library/gemma3

## Project links

- GitHub repository: [ADD YOUR PUBLIC GITHUB URL]
- Medium article: [ADD YOUR PUBLIC MEDIUM URL]
