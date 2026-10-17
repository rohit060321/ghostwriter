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

## Deploy to Render

You can deploy GhostWriter AI to [Render](https://render.com/) on the free tier. The project includes a pre-configured `render.yaml` Blueprint and `start.sh` runner that hosts both FastAPI and Streamlit seamlessly in a single Web Service.

### Option 1: 1-Click Deploy via Render Blueprint (Recommended)

1. Push your latest code to GitHub:
   ```powershell
   git push origin main
   ```
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** > **Blueprint**.
4. Connect your `ghostwriter` repository.
5. Render will detect `render.yaml`.
6. In the environment setup, set **`GROQ_API_KEY`** (get a free key at [Groq Console](https://console.groq.com/keys)). This powers open-weight Gemma inference 24/7 in the cloud without needing Ollama or your PC running.
7. Click **Apply**. Render will automatically build and launch your app.

### Option 2: Manual Web Service Setup

1. In Render Dashboard, click **New +** > **Web Service**.
2. Select and connect your repository.
3. Configure the settings:
   - **Name**: `ghostwriter-ai`
   - **Environment / Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash start.sh`
   - **Plan**: `Free`
4. Under **Environment Variables**, add:
   - `GROQ_API_KEY`: *(Your key from console.groq.com)*
   - `GROQ_MODEL`: `gemma2-9b-it`
5. Click **Create Web Service**.

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
