# ⚡ FLUX

**Intelligent Task Management** · *Made by -eternal*

A **zero-cost**, multimodal task management system powered by AI. Upload evidence from anywhere and let AI handle analysis, organization, and documentation.

## ✨ Features

### 🚌 The Commuter Flow (Mobile)
- Upload evidence from your phone while commuting
- Support for **videos, PDFs, images, spreadsheets**
- Add quick voice-to-text context notes
- AI instantly analyzes and creates structured tasks

### 💻 The Deep Work Flow (Desktop)
- Kanban board for task management
- AI-generated summaries for all evidence
- Generate TestRail-compatible CSVs
- Create professional requirement documents
- Draft weekly Scrum update emails

### 🤖 AI Intelligence Layer
- Powered by **Gemini 3.0 Pro** (multimodal)
- Video temporal analysis for bug flows
- PDF requirement extraction
- Spreadsheet data summarization
- Image OCR and visual defect detection

### ☁️ Zero-Cost Architecture
- Frontend: **Streamlit** (Community Cloud or Replit)
- Intelligence: **Gemini 3.0 Pro** (Free tier)
- Storage: **Google Drive** (2TB)
- Database: **Google Sheets** (Free)

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.9+** installed
2. **Google Cloud Project** with:
   - Drive API enabled
   - Sheets API enabled
   - Service Account created
3. **Gemini API Key** from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Installation

1. **Clone/Download this project**
   ```bash
   cd eternal-flow
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up credentials** (see below)

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

---

## 🔑 Credentials Setup

### Step 1: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the API key

### Step 2: Create Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select existing)
3. Enable **Google Drive API**:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Drive API"
   - Click "Enable"
4. Enable **Google Sheets API**:
   - Same process as above
5. Create Service Account:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in name (e.g., "flux-service")
   - Click "Create and Continue"
   - Grant "Editor" role
   - Click "Done"
6. Generate JSON Key:
   - Click on your service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Choose "JSON" format
   - Download the file
   - **Save as `service_account.json` in the project root**

### Step 3: Set Up Google Drive Folder

1. Open [Google Drive](https://drive.google.com)
2. Create a new folder (e.g., "FLUX Evidence")
3. **Share the folder** with your service account email:
   - Right-click folder > "Share"
   - Paste service account email (found in JSON file: `client_email`)
   - Grant "Editor" access
4. Copy the folder ID from the URL:
   - Open the folder
   - URL looks like: `https://drive.google.com/drive/folders/FOLDER_ID_HERE`
   - Copy the `FOLDER_ID_HERE` part

### Step 4: Set Up Google Sheet

1. Create a new [Google Sheet](https://sheets.google.com)
2. Name it (e.g., "FLUX Tasks")
3. **Share with service account** (same process as Drive folder)
4. Copy the sheet ID from the URL:
   - URL looks like: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
   - Copy the `SHEET_ID_HERE` part

### Step 5: Create .env File

Create a file named `.env` in the project root:

```env
# Google AI Studio API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Google Drive Folder ID
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id_here

# Google Sheets ID
GOOGLE_SHEETS_ID=your_google_sheets_id_here

# Path to Service Account JSON
GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
```

**Replace the placeholder values** with your actual credentials.

---

## 📱 Usage

### Upload Evidence

1. Open the app and navigate to **📤 Upload**
2. Choose a file (video, PDF, image, or spreadsheet)
3. Optionally add context notes
4. Click **Upload & Analyze**
5. AI will:
   - Upload to Google Drive
   - Analyze the content
   - Create a task in your Sprint Board

### Manage Tasks

1. Go to **📋 Sprint Board**
2. View tasks organized by status:
   - **In Review** - Newly uploaded
   - **Passed In Review** - Passed initial review
   - **In Stage** - Being tested/staged
   - **Passed In Stage** - Passed staging
   - **Done** - Completed and deployed
3. Update status by selecting from dropdown
4. Click evidence links to view files in Drive

### Generate Outputs

1. Navigate to **⚡ Generate**
2. Choose output type:
   - **Test Cases CSV** - For TestRail/Jira import
   - **Requirement Doc** - Professional PDF
   - **Scrum Email** - Weekly summary
3. Click generate and download

---

## 🌐 Deployment

### Streamlit Community Cloud (Recommended)

1. Push your code to GitHub (**without `.env` or `service_account.json`**)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Set **Main file path**: `app.py`
6. Click "Advanced settings"
7. Add **Secrets** (your `.env` content):
   ```toml
   GEMINI_API_KEY = "your_key"
   GOOGLE_DRIVE_FOLDER_ID = "your_id"
   GOOGLE_SHEETS_ID = "your_id"
   GOOGLE_SERVICE_ACCOUNT_JSON = "service_account.json"
   ```
8. Also add the **full JSON content** of your service account file as a multi-line secret
9. Deploy!

### Replit

1. Create a new Repl and upload your code
2. Add **Secrets** in the Secrets tab (left sidebar)
3. Add each environment variable
4. For `service_account.json`, upload the file directly
5. Run with `streamlit run app.py`

---

## 📂 Project Structure

```
eternal-flow/
├── app.py                      # Main Streamlit app
├── config.py                   # Configuration & credentials
├── requirements.txt            # Python dependencies
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
│
├── pages/
│   ├── 1_📤_Upload.py         # Upload interface
│   ├── 2_📋_Sprint_Board.py   # Kanban board
│   └── 3_⚡_Generate.py        # Output generation
│
├── services/
│   ├── google_drive.py        # Drive integration
│   ├── google_sheets.py       # Sheets integration
│   └── gemini_processor.py    # AI processing
│
├── prompts/
│   └── templates.py           # AI prompt templates
│
└── utils/
    ├── file_validator.py      # File validation
    └── logger.py              # Logging utilities
```

---

## 🎯 Supported File Types

| Category | Extensions | AI Analysis |
|----------|-----------|-------------|
| **Videos** | `.mp4`, `.mov` | Temporal flow analysis, bug steps extraction |
| **Documents** | `.pdf` | Requirement extraction, constraint identification |
| **Spreadsheets** | `.xlsx`, `.csv` | Data summarization, priority item detection |
| **Images** | `.png`, `.jpg`, `.jpeg` | OCR, visual defect detection |

---

## 🛠️ Troubleshooting

### "Missing Credentials" Error

- Ensure `.env` file exists with all 4 variables
- Check that `service_account.json` exists in project root
- Verify folder/sheet IDs are correct

### "Permission Denied" on Drive/Sheets

- Ensure you shared the folder AND sheet with service account email
- Grant "Editor" access (not just "Viewer")

### Slow AI Processing

- Large video files take longer to process
- PDF processing depends on file size
- First upload may be slower due to API warm-up

### Module Import Errors

- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.9+ required)

---

## 💡 Pro Tips

1. **Batch Uploads**: Upload multiple files during your commute
2. **Descriptive Filenames**: Use clear names like `login-bug-2024-02-01.mp4`
3. **Context Notes**: Always add context for better AI analysis
4. **Weekly Reviews**: Use Generate page every Friday for Scrum updates
5. **Evidence Links**: Bookmark your Drive folder for quick access

---

## 📄 License

MIT License - Feel free to use and modify!

---

## 🙏 Credits

Built with:
- [Streamlit](https://streamlit.io) - Web framework
- [Google Gemini](https://ai.google.dev) - AI intelligence
- [Google Drive API](https://developers.google.com/drive) - File storage
- [Google Sheets API](https://developers.google.com/sheets) - Database

---

## 🤝 Support

Issues? Questions? Open a GitHub issue or check the troubleshooting section above.

**Happy Sprinting! 🚀**
