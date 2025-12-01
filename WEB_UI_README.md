# Notebook to Code Pipeline - Web UI

## Running the Web Interface

### Option 1: Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Set up environment**:
   Create a `.env` file with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Run the Streamlit app**:
   ```bash
   uv run streamlit run app.py
   ```

4. **Access the UI**:
   Open your browser to `http://localhost:8501`

### Option 2: Deploy to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Add Streamlit web UI"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Add `GOOGLE_API_KEY` in Secrets (Advanced settings)

3. **Access your deployed app**:
   Streamlit will provide a public URL

### Option 3: Deploy to Google Cloud Run

1. **Create Dockerfile** (already included if you ran the pipeline):
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY . .
   
   RUN pip install uv && uv sync
   
   EXPOSE 8501
   
   CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and deploy**:
   ```bash
   gcloud run deploy notebook-pipeline \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your_key_here
   ```

## Using the Web UI

### Features

1. **Upload Notebook**: Drag and drop or browse for `.ipynb` files
2. **PII Security Check**: Automatic detection of sensitive information
3. **Progress Tracking**: Real-time progress bar showing pipeline stages
4. **Generated Output**: View directory structure and download as ZIP
5. **Clear OUTPUT**: Button to clean up previous runs

### Workflow

1. Enter your Google API Key in the sidebar
2. Upload a Jupyter notebook
3. Review the PII security check
4. Click "Run Pipeline"
5. Monitor progress through the multi-agent stages:
   - Parser Agent (20%)
   - Architect Agent (35%)
   - Refactorer Agent (40-55%)
   - DevOps Agent (45-60%)
   - Reviewer Agent (50-65%)
6. Download the generated code as a ZIP file

### Pipeline Stages

- **Parser**: Extracts code and documentation from notebook
- **Architect**: Designs production-ready folder structure
- **Refactorer**: Generates modular, clean Python code
- **DevOps**: Creates Dockerfile, CI/CD configs
- **Reviewer**: Reviews code quality and approves/provides feedback

### Output

The generated code includes:
- `src/` - Python modules
- `tests/` - Unit tests
- `Dockerfile` - Container configuration
- `requirements.txt` - Dependencies
- `.github/workflows/` - CI/CD pipeline
- `README.md` - Documentation

## Troubleshooting

### "Please enter your Google API Key"
- Add your API key in the sidebar
- Or set `GOOGLE_API_KEY` in `.env` file

### "PII Detected"
- Review the detected sensitive information
- Remove or anonymize PII from your notebook
- Re-upload the cleaned notebook

### "Max rounds reached"
- The reviewer found issues in 3 rounds
- Download the generated code anyway
- Review the feedback in the logs
- Manually fix the issues

## Architecture

The web UI wraps the existing multi-agent pipeline:
- **Frontend**: Streamlit (Python)
- **Backend**: Google ADK with Gemini 2.0 Flash
- **Agents**: Parser, Architect, Refactorer, DevOps, Reviewer
- **Session Management**: In-memory session service

## Development

To modify the UI:
1. Edit `app.py`
2. Streamlit will auto-reload on save
3. Test locally before deploying

## Security

- API keys are never logged or stored
- PII detection runs before processing
- All processing happens server-side
- Generated code is stored temporarily

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review the walkthrough documentation
- Ensure Google API Key has Gemini access
