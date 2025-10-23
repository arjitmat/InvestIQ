# InvestIQ - HuggingFace Spaces Deployment Guide

## Prerequisites

1. **HuggingFace Account:** Sign up at https://huggingface.co/
2. **HuggingFace CLI:** Install with `pip install huggingface_hub`
3. **API Keys Ready:**
   - NewsAPI: https://newsapi.org/
   - Reddit: https://www.reddit.com/prefs/apps
   - Gemini: https://aistudio.google.com/

## Step-by-Step Deployment

### 1. Create HuggingFace Space

1. Go to https://huggingface.co/new-space
2. Fill in details:
   - **Space name:** investiq (or your preferred name)
   - **License:** MIT
   - **Select the Space SDK:** Docker
   - **Visibility:** Public or Private
3. Click "Create Space"

### 2. Configure Environment Variables

1. Go to your Space Settings
2. Navigate to "Variables and Secrets"
3. Add the following secrets:

```
NEWSAPI_KEY=your_newsapi_key_here
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important:** Mark all as "Secret" (not "Variable") to keep them private.

### 3. Deploy to HuggingFace

```bash
# Navigate to project directory
cd /path/to/InvestIQ

# Install HuggingFace CLI if not already installed
pip install huggingface_hub

# Login to HuggingFace
huggingface-cli login
# Enter your HuggingFace token when prompted
# Get token from: https://huggingface.co/settings/tokens

# Add HuggingFace as a git remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push to HuggingFace (this will trigger the build)
git push hf main
```

### 4. Monitor Build Progress

1. Go to your Space page: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
2. Click on "Logs" tab to see build progress
3. Build typically takes 5-10 minutes (installs Node, Python deps, builds React)
4. Once complete, status will change to "Running"

### 5. Access Your App

Your app will be live at:
```
https://YOUR_USERNAME-YOUR_SPACE_NAME.hf.space
```

Or via the HuggingFace interface:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

## Troubleshooting

### Build Fails

**Check Logs:**
- Go to Logs tab in your Space
- Look for error messages

**Common Issues:**
1. **Missing dependencies:** Check requirements.txt and package.json
2. **Build timeout:** HF Spaces have build time limits (usually sufficient)
3. **Path issues:** Ensure Dockerfile paths are correct

### App Doesn't Load

**Check:**
1. **Port 7860:** App must run on port 7860 (HF Spaces default)
2. **Environment variables:** Verify all secrets are set correctly
3. **Health check:** Visit `/health` endpoint to test API

### API Errors

**Verify:**
1. All API keys are correct and active
2. No rate limiting on external APIs
3. Check backend logs for error details

## Updating Your Space

After initial deployment, push updates with:

```bash
git add .
git commit -m "Description of changes"
git push hf main
```

HuggingFace will automatically rebuild and redeploy.

## Local Testing (Optional)

Test Docker build locally before deploying:

```bash
# Build Docker image
docker build -t investiq-test .

# Run with environment variables
docker run -p 7860:7860 \
  -e NEWSAPI_KEY=your_key \
  -e REDDIT_CLIENT_ID=your_id \
  -e REDDIT_CLIENT_SECRET=your_secret \
  -e GEMINI_API_KEY=your_key \
  investiq-test

# Access at http://localhost:7860
```

## Performance Notes

**HuggingFace Spaces Free Tier:**
- ✅ No cold starts (always warm)
- ✅ Good CPU/RAM allocation
- ✅ Free SSL certificates
- ✅ Built-in monitoring
- ⚠️ May sleep after prolonged inactivity (easy to wake)

## Support

If you encounter issues:
1. Check HuggingFace Spaces documentation: https://huggingface.co/docs/hub/spaces
2. Review Space logs carefully
3. Test locally with Docker first
4. Verify all environment variables

---

Good luck with your deployment! 🚀
