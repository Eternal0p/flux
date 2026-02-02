# 🚀 Quick Start - AI Sprint Brain

This guide will get you up and running in **15 minutes**.

---

## ⚡ Speed Run Setup

### 1. Install Dependencies (2 min)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Get Gemini API Key (3 min)

1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### 3. Quick Google Cloud Setup (5 min)

**Option A: Use Existing Google Account**
1. Go to https://console.cloud.google.com
2. Create project: "ai-sprint-brain"
3. Enable APIs:
   - Search "Drive API" → Enable
   - Search "Sheets API" → Enable
4. Create Service Account:
   - Go to "Credentials" → "Create Credentials" → "Service Account"
   - Name: `ai-sprint-brain-sa`
   - Create key (JSON) → Download
   - Rename to `service_account.json`

### 4. Create Drive Folder & Sheet (3 min)

**Google Drive**:
1. Create folder: "AI Sprint Brain Evidence"
2. Share with service account email (from JSON: `client_email`)
3. Grant "Editor" access
4. Copy folder ID from URL

**Google Sheets**:
1. Create new sheet: "AI Sprint Brain Tasks"
2. Share with same service account email
3. Grant "Editor" access
4. Copy sheet ID from URL

### 5. Create .env File (2 min)

Create `.env` in project root:

```env
GEMINI_API_KEY=paste_your_gemini_api_key
GOOGLE_DRIVE_FOLDER_ID=paste_drive_folder_id
GOOGLE_SHEETS_ID=paste_sheet_id
GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
```

### 6. Run! (instant)

```bash
streamlit run app.py
```

Open browser to http://localhost:8501

---

## 🎯 First Test

1. **Upload a test file**:
   - Go to "📤 Upload" page
   - Drag any image/PDF
   - Add note: "Test upload"
   - Click "Upload & Analyze"

2. **Check the results**:
   - Verify file in Google Drive folder
   - Check task in Google Sheet
   - View task on Sprint Board

3. **Generate output**:
   - Mark task as "Done" on board
   - Go to "⚡ Generate"
   - Try generating test cases

---

## ❓ Troubleshooting

### "Missing Credentials" Error

**Check**:
- `.env` file exists in project root
- All 4 variables are set
- `service_account.json` exists
- No typos in variable names

**Fix**:
```bash
# Verify files exist
ls .env service_account.json

# Check .env content
cat .env
```

### "Permission Denied"

**Issue**: Service account can't access Drive/Sheets

**Fix**:
1. Go to Google Drive folder
2. Click "Share"
3. Verify service account email is listed
4. Change to "Editor" (not "Viewer")
5. Repeat for Google Sheet

### Module Import Errors

**Fix**:
```bash
# Ensure virtual environment is active
# Should see (venv) in terminal

# Reinstall
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📖 Next Steps

After setup works:

1. **Read the full docs**:
   - [README.md](README.md) - Complete guide
   - [docs/API_SETUP.md](docs/API_SETUP.md) - Detailed setup
   - [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Deploy online

2. **Customize**:
   - Adjust file size limits in `config.py`
   - Modify AI prompts in `prompts/templates.py`
   - Update UI styling in `app.py`

3. **Deploy**:
   - Push to GitHub
   - Deploy to Streamlit Cloud (free)
   - Share with your team

---

## 💬 Common Questions

**Q: Do I need a credit card?**
A: Only for Google Cloud (won't be charged if you stay in free tier)

**Q: How much does this cost?**
A: $0 if you stay within free tier limits

**Q: Can I use my work Google account?**
A: Yes, but check with your IT department first

**Q: What if I hit API limits?**
A: Free tier is generous. You're unlikely to hit limits with normal use.

**Q: Can I deploy this for my team?**
A: Yes! Deploy to Streamlit Cloud and share the URL.

**Q: Is my data secure?**
A: Data is stored in YOUR Google Drive/Sheets. You control access.

---

## 🆘 Still Stuck?

**Check**:
1. Python version: `python --version` (need 3.9+)
2. Virtual environment active: See `(venv)` in terminal
3. All files in correct locations
4. Service account has Editor access to both Drive and Sheets

**Get Help**:
- Review error messages carefully
- Check Google Cloud Console for API quotas
- Verify service account permissions

---

**Happy coding! 🧠🚀**

Once you see the app running, you're ready to upload your first evidence and let AI do the work!
