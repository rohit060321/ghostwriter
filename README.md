# GhostWriter AI — The Side Hustle Autopilot

Turn product details into a ready-to-use marketing kit with an open-weight AI model. GhostWriter AI is designed for independent sellers, home businesses, creators, and freelancers who need affordable product copy without depending on a paid, closed-model API.

## Features

- Generates a product title and short/full descriptions.
- Creates a platform-friendly social caption, hashtags, promotional message, and alternative hooks.
- Lets users choose platform, tone, and output language.
- Exports the result as a Markdown file.
- Uses Gemma through Ollama, so inference can run locally.
- Includes a FastAPI backend and Streamlit frontend.

## Architecture

```text
User
 |
 v
Streamlit UI (app.py)
 |
 | POST /generate
 v
FastAPI backend (main.py)
 |
 | POST /api/generate
 v
Ollama running Gemma (gemma3:1b)
 |
 v
Generated sales kit -> UI -> Markdown download
```

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/)
- Enough RAM to run the model you choose

## Run locally on Windows

Open PowerShell in the project folder.

### 1. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Install and run Gemma

Install Ollama from https://ollama.com/ and then run:

```powershell
ollama pull gemma3:1b
```

Keep Ollama running. Its local API normally listens at `http://127.0.0.1:11434`.

### 3. Start the backend

Open a PowerShell terminal in the project folder:

```powershell
uvicorn main:app --reload
```

Check `http://127.0.0.1:8000/health`. API documentation is at `http://127.0.0.1:8000/docs`.

### 4. Start the frontend

Open a second PowerShell terminal, activate the same virtual environment, and run:

```powershell
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Configuration

Defaults use a local Ollama instance and the `gemma3:1b` model. To use another Ollama model, set an environment variable before starting the backend:

```powershell
$env:OLLAMA_MODEL="your-installed-model-name"
uvicorn main:app --reload
```

To change the backend URL for the frontend:

```powershell
$env:GHOSTWRITER_API_URL="http://127.0.0.1:8000"
streamlit run app.py
```

## Open innovation: why it matters

A locally hosted open-weight model gives small sellers a way to generate copy without paying for each request to a closed AI API. Local inference can keep product information on the user's own computer and makes it easier to swap supported models as needs change. The application is useful offline after the model has been downloaded, provided Ollama and the app are running locally. Model license terms still apply; review the license of the specific model before commercial use.

## Business model

Possible future pricing:
- Free: a limited number of sales kits.
- Creator: monthly plan for batch generation, saved brand voice, and reusable templates.
- Small-business plan: team workspaces and product catalog integration.

These are proposed plans, not active billing features.

## Current limitations

- The app generates text from user-provided product details; it does not currently analyze uploaded product images or voice recordings.
- It does not publish directly to Etsy, Instagram, or WhatsApp.
- It does not validate market prices or guarantee sales.
- A user should review every generated claim before publishing.
- Local inference performance depends on the computer and model.

## Roadmap

- Add image understanding with a compatible vision model.
- Add voice-note transcription.
- Add brand voice profiles and batch product generation.
- Add user feedback and optional evaluation of output quality.
- Add deployment configuration for a hosted backend.

## Contributing

Issues and pull requests are welcome. Keep the local-first workflow and transparent model configuration in mind.

## License

MIT. See `LICENSE`.
