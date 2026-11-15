# AI-Powered Meeting Notes and Action Item Generator

A local AI application built with **Python, Streamlit, Ollama and Gemma 3 4B**. It converts a meeting transcript into a concise summary, discussion points, decisions, open questions, risks and structured action items.

## Features

- Paste a transcript or upload a `.txt` file.
- Conservative text preprocessing.
- Local LLM inference through the Ollama HTTP API.
- Structured JSON output.
- Action items include task, owner, deadline, status and transcript evidence.
- Download meeting notes as JSON and action items as CSV.
- Three sample transcripts and basic unit tests.

## Requirements

- Windows 10/11
- Python 3.10 or newer
- VS Code
- Ollama for Windows
- Gemma 3 4B model (`gemma3:4b`)

## 1. Install Python and VS Code

Install Python from https://www.python.org/downloads/ and VS Code from https://code.visualstudio.com/.
During Python installation, enable **Add Python to PATH**. In VS Code, install the Microsoft Python extension.

## 2. Install Ollama and download Gemma 3 4B

Install Ollama for Windows from https://ollama.com/download.

Open PowerShell or the VS Code terminal and run:

```powershell
ollama pull gemma3:4b
ollama list
ollama run gemma3:4b
```

Wait for the model prompt. Type a short question to confirm it responds, then type `/bye` to exit.

Ollama normally exposes its local API at `http://localhost:11434`.

## 3. Open the project in VS Code

Extract the ZIP file. In VS Code choose **File → Open Folder** and select `ai_meeting_notes_generator`.

Open **Terminal → New Terminal**. Run:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use this command for the current terminal session:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Alternative: use Command Prompt terminal and run `.venv\Scripts\activate.bat`.

## 4. Run the app

Make sure Ollama is running. If required, start it from the Windows Start menu or run `ollama serve` in a separate terminal.

In the project terminal:

```powershell
streamlit run app.py
```

Streamlit will show a local address, usually `http://localhost:8501`. Open it in your browser.

In the sidebar, keep:
- Ollama URL: `http://localhost:11434`
- Model name: `gemma3:4b`

Click **Check Ollama connection**, select a sample transcript, then click **Generate meeting notes**.

## 5. Test the project

Try all three samples:
1. `product_launch.txt` — explicit owners and deadlines.
2. `website_bug_review.txt` — investigation tasks and a decision that is still pending.
3. `noisy_meeting.txt` — ambiguous dates, unclear audio and unassigned tasks.

Review whether the model:
- Captures the central topic.
- Separates decisions from proposals.
- Extracts only explicit action items.
- Leaves missing owners and deadlines as `Not specified`.
- Avoids inventing a root cause or commitment.

Do not claim a test passed until you run it and inspect the actual output. Record the actual output, response time and mistakes in your article.

Run unit tests:

```powershell
pytest -q
```

These tests check local preprocessing, output normalization and CSV export. They do not test the quality of Gemma's generated summaries.

## 6. Troubleshooting

**Connection refused / cannot reach Ollama**
- Confirm Ollama is running.
- Open `http://localhost:11434` in a browser. The service may return a short message that it is running.
- Run `ollama list`.

**Model not found**
- Run `ollama pull gemma3:4b`.
- Use the exact tag `gemma3:4b` in the app.

**Model is slow**
- First model load can take longer.
- Close memory-heavy applications and use shorter transcripts.
- Performance depends on RAM, CPU/GPU and model quantization.

**PowerShell cannot activate the virtual environment**
- Use the process-scoped execution policy command above, or switch to Command Prompt.

**JSON/API error**
- Update Ollama to a current version and retry.
- Check the terminal error and verify the model responds with `ollama run gemma3:4b`.

## Privacy and responsible use

Use sample, synthetic or consented transcripts only. The application sends text to the Ollama service configured in the sidebar. With the default local address, inference runs on the same computer; do not expose Ollama's API port publicly. If you deploy Streamlit to a cloud host, review where the transcript is processed and stored before using real meeting data.

Always verify generated notes against the original transcript. The model can miss context, confuse speakers, misread transcription errors or produce incorrect tasks. The evidence field is a review aid, not a guarantee.

## Repository structure

```text
ai_meeting_notes_generator/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── src/
│   ├── __init__.py
│   └── meeting_ai.py
├── samples/
│   ├── product_launch.txt
│   ├── website_bug_review.txt
│   └── noisy_meeting.txt
├── tests/
│   └── test_meeting_ai.py
└── docs/
    ├── architecture.mmd
    └── medium_article_draft.md
```

## Suggested screenshots

Capture your own screenshots after running the application:
1. Streamlit home screen with the transcript input.
2. Product launch transcript loaded before generation.
3. Generated summary, key points and decisions.
4. Action items table showing task, owner and deadline.
5. CSV/JSON download controls.
6. VS Code terminal showing `streamlit run app.py` and successful `pytest -q`.

On Windows use **Win + Shift + S**. Do not use fabricated output screenshots. Blur personal or confidential meeting information.

## Medium publication

Use `docs/medium_article_draft.md` as a starting draft. Replace every `[ADD ...]` placeholder with your real screenshots, test observations, response times and GitHub URL before publishing.

## References

- Ollama API documentation: https://docs.ollama.com/api
- Ollama structured outputs: https://ollama.com/blog/structured-outputs
- Streamlit documentation: https://docs.streamlit.io/
- Gemma models: https://ollama.com/library/gemma3

## License

For academic demonstration and learning. Add a license if your instructor or repository requires one.
