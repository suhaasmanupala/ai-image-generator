# 🚀 Deployment Guide

## Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - FREE)

#### Prerequisites
- GitHub account
- Your code pushed to GitHub repository

#### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In Streamlit Cloud dashboard, go to your app settings
   - Click "Secrets"
   - Add your API key:
   ```toml
   HUGGINGFACE_API_KEY = "hf_your_actual_token_here"
   ```
   - Save

4. **Done!** Your app will be live at: `https://your-app-name.streamlit.app`

---

### Option 2: Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps:

1. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create App**
   ```bash
   heroku create your-app-name
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set HUGGINGFACE_API_KEY=hf_your_token_here
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

6. **Open App**
   ```bash
   heroku open
   ```

---

### Option 3: Docker

#### Create Dockerfile

Already included in project. To deploy:

1. **Build Image**
   ```bash
   docker build -t ai-image-generator .
   ```

2. **Run Container**
   ```bash
   docker run -p 8501:8501 \
     -e HUGGINGFACE_API_KEY=hf_your_token_here \
     ai-image-generator
   ```

3. **Access at** http://localhost:8501

#### Deploy to Docker Hub

```bash
docker tag ai-image-generator your-username/ai-image-generator
docker push your-username/ai-image-generator
```

---

### Option 4: AWS EC2

#### Steps:

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Open port 8501 in security group

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip
   pip3 install -r requirements.txt
   ```

4. **Set Environment Variable**
   ```bash
   export HUGGINGFACE_API_KEY=hf_your_token_here
   ```

5. **Run App**
   ```bash
   nohup streamlit run app.py &
   ```

6. **Access at** http://your-ec2-ip:8501

---

### Option 5: Google Cloud Run

#### Steps:

1. **Create Dockerfile** (already included)

2. **Build and Push**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/ai-image-gen
   ```

3. **Deploy**
   ```bash
   gcloud run deploy ai-image-gen \
     --image gcr.io/PROJECT_ID/ai-image-gen \
     --platform managed \
     --set-env-vars HUGGINGFACE_API_KEY=hf_your_token_here
   ```

---

## 🔒 Security Checklist Before Deployment

- [ ] API key is in environment variables (not hardcoded)
- [ ] `.env` file is in `.gitignore`
- [ ] No sensitive data in code
- [ ] HTTPS enabled (automatic on most platforms)
- [ ] Rate limiting considered
- [ ] Error messages don't expose sensitive info

---

## 📊 Post-Deployment

### Monitor Your App
- Check logs regularly
- Monitor API usage
- Track error rates
- Review user feedback

### Optimize Performance
- Enable caching where possible
- Monitor response times
- Scale resources if needed
- Consider CDN for static assets

### Maintenance
- Keep dependencies updated
- Monitor Hugging Face API status
- Backup generation history if needed
- Update documentation

---

## 🆘 Troubleshooting

### App won't start
- Check logs for errors
- Verify all dependencies installed
- Confirm API key is set correctly

### Slow performance
- Check API rate limits
- Consider upgrading hosting plan
- Optimize image sizes

### API errors
- Verify token is valid
- Check Hugging Face status
- Review rate limit usage

---

## 💰 Cost Considerations

### Free Options
- **Streamlit Cloud**: Free tier available
- **Heroku**: Free tier (with limitations)
- **AWS**: Free tier for 12 months

### Paid Options
- **Streamlit Cloud Pro**: $20/month
- **Heroku Standard**: $7/month
- **AWS EC2**: ~$10/month
- **Google Cloud Run**: Pay per use

---

## 🎉 Recommended: Streamlit Cloud

**Why?**
- ✅ Completely free
- ✅ Easy setup (5 minutes)
- ✅ Automatic HTTPS
- ✅ GitHub integration
- ✅ Built-in secrets management
- ✅ Auto-deploy on git push
- ✅ No server management

**Perfect for this project!**

---

## 📝 Next Steps After Deployment

1. Share your app URL
2. Gather user feedback
3. Monitor usage patterns
4. Add new features
5. Scale as needed

Good luck with your deployment! 🚀
