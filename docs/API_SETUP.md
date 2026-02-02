# 🔧 Google Cloud API Setup Guide

Complete step-by-step guide to setting up Google Cloud credentials for AI Sprint Brain.

---

## Prerequisites

- Google Account
- Credit card (for Google Cloud - won't be charged for free tier usage)

---

## Step 1: Create Google Cloud Project

1. **Visit Google Cloud Console**
   - Go to [console.cloud.google.com](https://console.cloud.google.com)
   - Sign in with your Google account

2. **Create New Project**
   - Click the project dropdown (top left, next to "Google Cloud")
   - Click "New Project"
   - Enter project name: `ai-sprint-brain`
   - Organization: Leave as "No organization" (unless you have one)
   - Click "Create"

3. **Select Your Project**
   - Wait for project creation (takes a few seconds)
   - Select your project from the dropdown

---

## Step 2: Enable Required APIs

### Enable Google Drive API

1. In the search bar, type "Drive API"
2. Click "Google Drive API"
3. Click "Enable"
4. Wait for activation

### Enable Google Sheets API

1. In the search bar, type "Sheets API"
2. Click "Google Sheets API"
3. Click "Enable"
4. Wait for activation

---

## Step 3: Create Service Account

1. **Navigate to Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Or search for "Credentials" in the search bar

2. **Create Credentials**
   - Click "Create Credentials" (top of page)
   - Select "Service Account"

3. **Service Account Details**
   - **Service account name**: `ai-sprint-brain-sa`
   - **Service account ID**: (auto-generated)
   - **Description**: "Service account for AI Sprint Brain app"
   - Click "Create and Continue"

4. **Grant Access** (Optional for basic setup)
   - Role: Select "Editor" (or leave empty for now)
   - Click "Continue"

5. **Grant User Access** (Optional)
   - Skip this step
   - Click "Done"

---

## Step 4: Generate JSON Key

1. **Find Your Service Account**
   - You'll see your service account in the list
   - Email looks like: `ai-sprint-brain-sa@PROJECT_ID.iam.gserviceaccount.com`

2. **Create Key**
   - Click on the service account email
   - Go to the "Keys" tab
   - Click "Add Key" > "Create new key"

3. **Download JSON**
   - Select "JSON" as key type
   - Click "Create"
   - Key will download automatically as `PROJECT_ID-xxxxx.json`

4. **Rename and Store**
   - Rename the file to `service_account.json`
   - Copy it to your project root folder
   - **IMPORTANT**: Never commit this file to Git!

---

## Step 5: Set Up Google Drive Folder

1. **Open Google Drive**
   - Go to [drive.google.com](https://drive.google.com)

2. **Create Folder**
   - Click "New" > "Folder"
   - Name: `AI Sprint Brain Evidence`
   - Click "Create"

3. **Share Folder with Service Account**
   - Right-click the folder > "Share"
   - In the "Add people" field, paste your service account email:
     ```
     ai-sprint-brain-sa@PROJECT_ID.iam.gserviceaccount.com
     ```
   - Change permission from "Viewer" to "Editor"
   - Uncheck "Notify people"
   - Click "Share"

4. **Get Folder ID**
   - Open the folder
   - Look at the URL:
     ```
     https://drive.google.com/drive/folders/1aBcD2EfG3HiJ4KlM5nOp6QrS7tUv8WxY
     ```
   - Copy the ID part: `1aBcD2EfG3HiJ4KlM5nOp6QrS7tUv8WxY`
   - Save this for your `.env` file

---

## Step 6: Set Up Google Sheet

1. **Create New Sheet**
   - Go to [sheets.google.com](https://sheets.google.com)
   - Click "Blank" to create new spreadsheet
   - Name it: `AI Sprint Brain Tasks`

2. **Share Sheet with Service Account**
   - Click "Share" button (top right)
   - Add your service account email (same as above)
   - Set permission to "Editor"
   - Uncheck "Notify people"
   - Click "Share"

3. **Get Sheet ID**
   - Look at the URL:
     ```
     https://docs.google.com/spreadsheets/d/1XyZ2aBc3DeF4gHi5JkL6mNo7PqR8StU9vWx/edit
     ```
   - Copy the ID part: `1XyZ2aBc3DeF4gHi5JkL6mNo7PqR8StU9vWx`
   - Save this for your `.env` file

---

## Step 7: Get Gemini API Key

1. **Visit Google AI Studio**
   - Go to [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account

2. **Create API Key**
   - Click "Create API Key"
   - Select your Google Cloud project (the one you created earlier)
   - Click "Create API key in existing project"
   - Or click "Create API key in new project" if preferred

3. **Copy Key**
   - Your API key will be displayed
   - Click the copy icon
   - Save this for your `.env` file
   - **IMPORTANT**: Keep this key secret!

---

## Step 8: Create .env File

In your project root, create a file named `.env`:

```env
# Paste your actual values here (remove the angle brackets)

# From Google AI Studio
GEMINI_API_KEY=AIzaSy...your_actual_key_here

# From Google Drive folder URL
GOOGLE_DRIVE_FOLDER_ID=1aBcD2EfG3HiJ4KlM5nOp6QrS7tUv8WxY

# From Google Sheets URL
GOOGLE_SHEETS_ID=1XyZ2aBc3DeF4gHi5JkL6mNo7PqR8StU9vWx

# Path to your service account JSON file
GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
```

**Replace** the placeholder values with your actual credentials!

---

## Verification Checklist

Before running the app, verify:

- [ ] Google Cloud project created
- [ ] Drive API enabled
- [ ] Sheets API enabled
- [ ] Service account created
- [ ] Service account JSON downloaded and renamed to `service_account.json`
- [ ] Drive folder created and shared with service account (Editor access)
- [ ] Google Sheet created and shared with service account (Editor access)
- [ ] Gemini API key generated
- [ ] `.env` file created with all 4 variables
- [ ] `service_account.json` in project root
- [ ] Both files are in `.gitignore`

---

## Common Issues

### "Permission Denied" Errors

**Symptom**: Can't upload to Drive or write to Sheets

**Solution**:
1. Double-check you shared both Drive folder AND Sheet with service account
2. Ensure permission is "Editor", not "Viewer"
3. Wait 1-2 minutes for permissions to propagate

### "Invalid Credentials" Error

**Symptom**: App can't authenticate

**Solution**:
1. Verify service account JSON is valid
2. Check file is named exactly `service_account.json`
3. Ensure file path in `.env` is correct

### "API Not Enabled" Error

**Symptom**: Error about disabled API

**Solution**:
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" > "Library"
3. Search for the API mentioned in error
4. Click "Enable"

### "Quota Exceeded" Error

**Symptom**: Too many requests

**Solution**:
1. You likely hit free tier limits
2. Wait for quota to reset (usually 1 minute)
3. Consider implementing rate limiting in code

---

## Security Best Practices

### Protect Your Credentials

1. **Never commit to Git**
   ```bash
   # Ensure these are in .gitignore:
   .env
   service_account.json
   ```

2. **Restrict Service Account Permissions**
   - Only grant Drive and Sheets access
   - Don't use overly broad roles

3. **Rotate Keys Regularly**
   - Generate new service account key every 90 days
   - Delete old keys in Google Cloud Console

4. **Monitor Usage**
   - Check Google Cloud Console > IAM & Admin > Service Accounts
   - Review activity logs periodically

### API Key Management

- Store Gemini API key securely
- Use environment variables (never hardcode)
- Don't share in screenshots or videos
- Revoke and regenerate if exposed

---

## Cost Monitoring

### Free Tier Limits

**Google Drive API**:
- 1 billion queries/day
- You won't hit this with normal use

**Google Sheets API**:
- 100 requests per 100 seconds per user
- 500 requests per 100 seconds per project

**Gemini API**:
- 60 requests per minute (free tier)
- Rate limits apply

### How to Stay Free

1. **Don't abuse APIs**: Implement reasonable rate limiting
2. **Monitor usage**: Check Cloud Console billing
3. **Set up alerts**: Configure budget alerts at $0

---

## Next Steps

After completing this setup:

1. Run the app: `streamlit run app.py`
2. Check for credential validation on home page
3. Try uploading a test file
4. Verify file appears in Drive folder
5. Check task appears in Google Sheet

**You're all set! 🎉**

---

## Additional Resources

- [Google Cloud Console](https://console.cloud.google.com)
- [Google AI Studio](https://makersuite.google.com)
- [Drive API Documentation](https://developers.google.com/drive)
- [Sheets API Documentation](https://developers.google.com/sheets)
- [Gemini API Documentation](https://ai.google.dev)
