# Deployment Guide - AI Form Filler

This guide provides step-by-step instructions for deploying the AI Form Filler application on various platforms.

## 📋 Prerequisites

- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- GitHub account
- Git installed on your local machine

## 🚀 Deployment Options

### 1. Streamlit Cloud (Recommended)

Streamlit Cloud offers the easiest deployment with direct GitHub integration.

#### Steps:
1. **Fork/Clone this repository** to your GitHub account
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub account**
4. **Select this repository** and set:
   - Main file path: `app.py`
   - Python version: `3.8+`
5. **Add secrets** in the Streamlit Cloud dashboard:
   - Go to app settings → Secrets
   - Add: `OPENAI_API_KEY = "sk-your-api-key-here"`
6. **Deploy!** Your app will be live in minutes

#### Advantages:
- ✅ Free hosting
- ✅ Automatic deployments on git push
- ✅ Built-in secrets management
- ✅ Custom domain support

---

### 2. Heroku Deployment

Deploy to Heroku for more control and custom configurations.

#### Setup Files Required:
Create these additional files in your project root:

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.11.0
```

#### Steps:
1. **Install Heroku CLI** ([Download here](https://devcenter.heroku.com/articles/heroku-cli))
2. **Login to Heroku:**
   ```bash
   heroku login
   ```
3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```
4. **Set environment variables:**
   ```bash
   heroku config:set OPENAI_API_KEY="sk-your-api-key-here"
   ```
5. **Deploy:**
   ```bash
   git push heroku main
   ```

#### Update app.py for Heroku:
Add this code to handle environment variables:
```python
import os
# Replace st.secrets["OPENAI_API_KEY"] with:
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
```

---

### 3. Docker Deployment

For containerized deployment on any platform.

#### Create Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run:
```bash
# Build image
docker build -t ai-form-filler .

# Run container
docker run -p 8501:8501 -e OPENAI_API_KEY="sk-your-api-key" ai-form-filler
```

---

### 4. AWS/GCP/Azure Deployment

For cloud platform deployment:

#### AWS (using EC2):
1. Launch EC2 instance (Ubuntu 20.04+)
2. Install Python and pip
3. Clone repository
4. Install dependencies
5. Set environment variables
6. Run with screen/tmux for persistence

#### GCP (using App Engine):
Create `app.yaml`:
```yaml
runtime: python39
env_variables:
  OPENAI_API_KEY: "sk-your-api-key-here"
```

Deploy:
```bash
gcloud app deploy
```

---

## 🔧 Configuration

### Environment Variables
All deployment methods need this environment variable:
- `OPENAI_API_KEY`: Your OpenAI API key

### Streamlit Configuration
For custom configurations, create `.streamlit/config.toml`:
```toml
[server]
port = 8501
maxUploadSize = 1000

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

## 🛠️ Troubleshooting

### Common Issues:

**1. API Key Not Found**
- Ensure the API key is correctly set in secrets/environment variables
- Check for typos in the variable name

**2. Module Not Found**
- Verify all dependencies are in requirements.txt
- Check Python version compatibility

**3. Port Already in Use**
- Change the port in your run command
- Kill existing processes on the port

**4. OpenAI API Errors**
- Verify API key validity
- Check your OpenAI account balance
- Ensure you have GPT-4 access

## 📊 Monitoring

### Streamlit Cloud:
- View logs in the Streamlit Cloud dashboard
- Monitor app performance and usage

### Heroku:
- View logs: `heroku logs --tail`
- Monitor app: `heroku ps`

### Docker:
- View logs: `docker logs <container_id>`
- Monitor resources: `docker stats`

## 🔄 Continuous Deployment

### GitHub Actions (for Heroku):
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Heroku
on:
  push:
    branches: [ main ]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

## 📈 Scaling

### For High Traffic:
- Use Heroku's auto-scaling
- Implement Redis for session management
- Add database for persistent storage
- Use CDN for static assets

## 🔐 Security Best Practices

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Implement rate limiting** for API calls
4. **Monitor API usage** to prevent abuse
5. **Use HTTPS** in production

## 📞 Support

For deployment issues:
- Check the [Streamlit documentation](https://docs.streamlit.io/)
- Visit [Streamlit Community](https://discuss.streamlit.io/)
- Review platform-specific documentation

---

**Happy Deploying!** 🚀 