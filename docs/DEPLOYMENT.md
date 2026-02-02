# 🚀 Deployment Guide - AI Sprint Brain

## Overview

This guide covers deploying AI Sprint Brain to zero-cost platforms.

---

## Option 1: Streamlit Community Cloud (Recommended)

### Prerequisites
- GitHub account
- Your code pushed to a GitHub repository

### Steps

1. **Prepare Your Repository**
   ```bash
   # Make sure .gitignore is set up correctly
   git add .
   git commit -m "Initial commit of AI Sprint Brain"
   git push origin main
   ```

2. **Visit Streamlit Community Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub

3. **Deploy New App**
   - Click "New app"
   - Select your repository
   - Set **Main file path**: `app.py`
   - Click "Advanced settings"

4. **Configure Secrets**
   
   In the Secrets section, add your credentials:
   
   ```toml
   GEMINI_API_KEY = "your_gemini_api_key_here"
   GOOGLE_DRIVE_FOLDER_ID = "your_drive_folder_id_here"
   GOOGLE_SHEETS_ID = "your_sheets_id_here"
   GOOGLE_SERVICE_ACCOUNT_JSON = "service_account.json"
   ```
   
   **Important**: You also need to add the service account JSON content. Create a file upload or paste the entire JSON as a multi-line string.

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be live! 🎉

### Custom Domain (Optional)

Streamlit Community Cloud provides a free subdomain:
```
https://your-app-name.streamlit.app
```

---

## Option 2: Replit

### Steps

1. **Create New Repl**
   - Go to [replit.com](https://replit.com)
   - Click "Create Repl"
   - Choose "Python" template
   - Name it "ai-sprint-brain"

2. **Upload Your Code**
   - Upload all files from your project
   - Or clone from GitHub using the Import feature

3. **Configure Environment**
   
   Click on "Secrets" (lock icon in left sidebar):
   
   ```
   GEMINI_API_KEY=your_key_here
   GOOGLE_DRIVE_FOLDER_ID=your_folder_id
   GOOGLE_SHEETS_ID=your_sheet_id
   GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
   ```

4. **Upload Service Account JSON**
   - Upload `service_account.json` directly to the project root

5. **Run Configuration**
   
   Create/edit `.replit` file:
   ```toml
   run = "streamlit run app.py"
   
   [env]
   PORT = "8080"
   ```

6. **Deploy**
   - Click "Run"
   - Repl will start serving your app
   - Use the provided URL to access

---

## Option 3: Self-Hosted (Your Own Server)

### Requirements
- Ubuntu/Debian server
- Python 3.9+
- Nginx (optional, for reverse proxy)

### Steps

1. **SSH into Your Server**
   ```bash
   ssh user@your-server-ip
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/ai-sprint-brain.git
   cd ai-sprint-brain
   ```

3. **Set Up Python Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your credentials
   ```
   
   Upload `service_account.json` via SCP:
   ```bash
   scp service_account.json user@your-server-ip:~/ai-sprint-brain/
   ```

5. **Run with nohup**
   ```bash
   nohup streamlit run app.py --server.port 8501 &
   ```

6. **Set Up Nginx Reverse Proxy (Optional)**
   
   Create `/etc/nginx/sites-available/ai-sprint-brain`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```
   
   Enable and restart:
   ```bash
   sudo ln -s /etc/nginx/sites-available/ai-sprint-brain /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

---

## Post-Deployment Checklist

- [ ] App loads without errors
- [ ] All credentials are configured
- [ ] Upload page works (test with small file)
- [ ] Files appear in Google Drive
- [ ] Tasks appear in Google Sheets
- [ ] Sprint Board displays tasks
- [ ] Generate page creates outputs
- [ ] Mobile responsiveness works

---

## Troubleshooting

### App Won't Start

**Check Logs**:
- Streamlit Cloud: View logs in deployment dashboard
- Replit: Check console output
- Self-hosted: Check `streamlit.log`

**Common Issues**:
- Missing dependencies: Verify `requirements.txt`
- Port conflicts: Use different port
- Python version: Ensure 3.9+

### "Missing Credentials" Error

- Verify all environment variables are set
- Check service account JSON is valid
- Ensure no typos in variable names

### Google API Errors

- Verify APIs are enabled in Google Cloud Console
- Check service account has correct permissions
- Ensure Drive folder and Sheet are shared with service account

---

## Security Best Practices

1. **Never Commit Secrets**
   - Keep `.env` and `service_account.json` in `.gitignore`
   - Use platform-specific secrets management

2. **Rotate API Keys Regularly**
   - Generate new Gemini API key every 90 days
   - Update in deployment secrets

3. **Monitor Usage**
   - Check Google Cloud Console for API usage
   - Set up billing alerts (though you should stay in free tier)

4. **Restrict Service Account**
   - Only grant necessary permissions
   - Never share service account email publicly

---

## Scaling Considerations

### Free Tier Limits

**Streamlit Community Cloud**:
- 1 GB RAM per app
- Limited CPU
- Public apps only (private requires Teams plan)

**Gemini API Free Tier**:
- 60 requests per minute
- Rate limiting may apply

**Google Drive/Sheets**:
- 15 GB free storage (Drive)
- API quotas apply

### If You Outgrow Free Tier

1. **Upgrade to Streamlit Teams**: $20/month for private apps
2. **Gemini API Paid Tier**: Pay-as-you-go pricing
3. **Self-Host**: Full control, pay for server only

---

## Monitoring & Maintenance

### Health Checks

Create a simple monitoring script:

```python
import requests

url = "https://your-app.streamlit.app"
response = requests.get(url)

if response.status_code == 200:
    print("✅ App is healthy")
else:
    print(f"❌ App returned {response.status_code}")
```

Run via cron job (every 5 minutes):
```bash
*/5 * * * * /path/to/health_check.py
```

### Backup

**Google Sheets** (automatic via Google):
- File > Version history

**Drive Folder**:
- Download all files periodically
- Use Google Takeout for full backup

---

## Next Steps

After deployment:
1. Test the upload flow with real files
2. Share the app URL with your team
3. Set up a bookmark on your phone for mobile access
4. Configure notifications (optional)

**Your AI Sprint Brain is now live! 🧠🚀**
