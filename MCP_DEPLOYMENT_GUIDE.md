# MCP Server Deployment & Configuration Guide

## 📋 Overview

This guide walks you through deploying your Model Context Protocol (MCP) server and connecting it to GitHub Copilot. After completion, you'll have a valid MCP server URL to use in any project.

---

## 🎯 Quick Start (5 minutes)

### Step 1: Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your GitHub token:
```bash
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_REPO_OWNER=myou260312-eng
GITHUB_REPO_NAME=skills-integrate-mcp-with-copilot
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Start Local MCP Server

```bash
python mcp_server.py
```

**Output:**
```
✅ MCP Server started at http://0.0.0.0:3000
🚀 MCP Server is running. Press Ctrl+C to stop.
```

### Step 4: Verify Server is Running

```bash
curl http://localhost:3000/mcp/
```

You should see JSON with available tools and resources.

---

## 🚀 Deploy to Production

### Option 1: Railway.app (Recommended - Free Tier Available)

**Why Railway?**
- ✅ Free tier available
- ✅ Auto-deploys from GitHub
- ✅ Public URL instantly
- ✅ Environment variables UI

**Steps:**

1. Visit [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `skills-integrate-mcp-with-copilot` repo
4. In the Railway dashboard:
   - Add environment variables (from `.env`)
   - Railway auto-detects `mcp_server.py` and runs it
5. **Name your service:** `mdabul-project` (this will create your URL)
6. Get your public URL from the Railway dashboard

**Your MCP Server URL:**
```
https://mdabul-project.railway.app/mcp/
```

### Option 2: Heroku (Requires Payment)

```bash
heroku login
heroku create mdabul-mcp-server
echo "web: python mcp_server.py" > Procfile
git add Procfile
git commit -m "Add Procfile for Heroku"
git push heroku main
heroku config:set GITHUB_TOKEN=ghp_xxxx
heroku open
```

### Option 3: Docker (Any Cloud Provider)

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["python", "mcp_server.py"]
```

**Build & Run:**
```bash
docker build -t vane-mcp-server .
docker run -p 3000:3000 \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -e MCP_ENABLED=true \
  vane-mcp-server
```

---

## 🔌 Connect to GitHub Copilot

### In VS Code (Local or Codespace)

1. **Update `.vscode/mcp.json`:**

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://mdabul-project.railway.app/mcp/"
    }
  }
}
```

2. **Click the Start button** in `.vscode/mcp.json`
3. **Authenticate** when prompted
4. **Verify tools appear:**
   - Open Copilot Chat
   - Click 🛠️ icon
   - You should see GitHub tools (list_issues, create_issue, etc.)

---

## 📊 Configuration Reference

### `config.py` Settings

| Setting | Default | Purpose |
|---------|---------|----------|
| `MCP_ENABLED` | `true` | Enable/disable MCP |
| `CONFIDENCE_HIGH_THRESHOLD` | `0.85` | High confidence barrier |
| `API_TIMEOUT` | `3.5s` | External API timeout |
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `TEMPERATURE` | `0.0` | LLM determinism (0=strict) |

### Environment Variables

```bash
# Required
GITHUB_TOKEN=ghp_xxxx              # GitHub Personal Access Token
GITHUB_REPO_OWNER=your-username    # Repo owner
GITHUB_REPO_NAME=repo-name         # Repo name

# Optional
MCP_ENABLED=true                   # Enable/disable MCP (default: true)
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
DEBUG_MODE=false                   # Verbose logging
VANE_ROOT_ID=custom-id             # Custom workspace ID
```

---

## 🧪 Test Your MCP Server

### Test with cURL (Local)

```bash
# List server capabilities
curl http://localhost:3000/mcp/

# Test list_issues tool
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "list_issues",
    "parameters": {"state": "open", "limit": 5}
  }'

# Test create_issue tool
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_issue",
    "parameters": {
      "title": "Test Issue",
      "body": "Test from MCP",
      "labels": ["test"]
    }
  }'
```

### Test with cURL (Production)

```bash
# Test production server
curl https://mdabul-project.railway.app/mcp/

# Test list_issues tool on production
curl -X POST https://mdabul-project.railway.app/ \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "list_issues",
    "parameters": {"state": "open", "limit": 5}
  }'
```

### Test with Copilot Chat

In VS Code Copilot Chat:
```
@github List all open issues in my repository
```

Copilot should use your MCP server to fetch and display issues.

---

## ✅ Use This MCP Server in Other Projects

**Yes! You can reuse this MCP server in any GitHub project.**

### Step 1: Copy `.vscode/mcp.json` to Your Project

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://mdabul-project.railway.app/mcp/"
    }
  }
}
```

### Step 2: Update Environment Variables

In your project, create `.env` (or set in Railway/Codespaces):
```bash
GITHUB_TOKEN=your_token_here
GITHUB_REPO_OWNER=your_username
GITHUB_REPO_NAME=your_repo_name
```

### Step 3: Use in Copilot Chat

Open Copilot Chat in any project and use:
```
@github List all issues in my repository
@github Create a new issue titled "Bug: Something broken"
@github Show repository information
```

**The same MCP server instance handles requests for ANY repository you configure!**

---

## 🔍 Troubleshooting

### Server won't start
```bash
# Check Python version (3.8+ required)
python --version

# Check for port conflicts
lsof -i :3000

# Run with verbose logging
DEBUG_MODE=true python mcp_server.py
```

### Copilot can't connect
- Verify `.vscode/mcp.json` URL is correct and accessible
- Check GitHub token is valid: `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user`
- Restart VS Code: `Cmd+R` (Mac) or `Ctrl+Shift+F5` (Windows/Linux)
- Check server logs: `tail -f workspaces/*/logs/vane_agent.log`

### Tools not appearing in Copilot
- Click Start button in `.vscode/mcp.json` again
- Reload VS Code
- Clear browser cache if using web version
- Check server is returning capabilities: `curl https://mdabul-project.railway.app/mcp/`

### MCP Server not accessible in other projects
- Ensure the Railway URL is public (it is by default)
- Check firewall/proxy isn't blocking the connection
- Verify GITHUB_TOKEN in `.env` is valid for the target repository
- Test connectivity: `curl https://mdabul-project.railway.app/mcp/`

---

## ✅ Completion Checklist

- [ ] Environment configured (`.env` file)
- [ ] Local server runs: `python mcp_server.py`
- [ ] Server responds to `curl http://localhost:3000/mcp/`
- [ ] Deployed to Railway as `mdabul-project`
- [ ] Production URL accessible: `https://mdabul-project.railway.app/mcp/`
- [ ] `.vscode/mcp.json` updated with production URL
- [ ] Copilot Chat shows GitHub tools
- [ ] Can test with sample prompts
- [ ] Tested in another project repository

---

## 📝 Your MCP Server URLs

### Development (Local Testing)
```
http://localhost:3000/mcp/
```

### Production (Railway - Shared Across All Projects)
```
https://mdabul-project.railway.app/mcp/
```

### Use in Any Project's `.vscode/mcp.json`
```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://mdabul-project.railway.app/mcp/"
    }
  }
}
```

---

## 🎓 Next Steps

1. ✅ Deploy your MCP server to Railway as `mdabul-project`
2. ✅ Verify URL works: `https://mdabul-project.railway.app/mcp/`
3. ✅ Use this URL in your primary project
4. ✅ Copy `.vscode/mcp.json` to other projects
5. ✅ Test Copilot Chat integration in each project
6. ✅ Extend tools in `mcp_server.py` for your use cases
7. ✅ Share the URL with your team for collaborative use

---

## 📚 Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitHub Copilot Extensions](https://docs.github.com/en/copilot)
- [Railway Docs](https://docs.railway.app/)
- [GitHub API Reference](https://docs.github.com/en/rest)
