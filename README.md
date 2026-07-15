# Vane MCP Server - GitHub Copilot Integration

A production-ready **Model Context Protocol (MCP) server** that extends GitHub Copilot with GitHub repository management capabilities. Enables AI-driven issue tracking, repository information retrieval, and seamless GitHub integration.

## ✨ Features

- 🔌 **HTTP-based MCP Server** - Universal compatibility with AI tools
- 🚀 **GitHub Integration** - Native GitHub tool support (list issues, create issues, get repo info)
- 🎯 **Agent-Ready Architecture** - Built on Vane agent framework with workspace isolation
- 📊 **Semantic Caching** - Intelligent context management with confidence thresholds
- 🔧 **Configurable** - Centralized configuration with environment variable support
- 📝 **Production-Ready** - Railway/Docker deployment guides included
- 🔄 **Reusable** - Single MCP server instance serves multiple projects

## 🚀 Quick Start

### Local Development (5 minutes)

```bash
# 1. Clone and setup
git clone https://github.com/myou260312-eng/skills-integrate-mcp-with-copilot
cd skills-integrate-mcp-with-copilot

# 2. Configure environment
cp .env.example .env
# Edit .env with your GITHUB_TOKEN

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start MCP server
python mcp_server.py
```

**Output:**
```
✅ MCP Server started at http://0.0.0.0:3000
🚀 MCP Server is running. Press Ctrl+C to stop.
```

### Verify Server

```bash
curl http://localhost:3000/mcp/
```

## 🌐 Production URL

```
https://mdabul-project.railway.app/mcp/
```

Use this URL in any project's `.vscode/mcp.json`:

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

## 📚 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Server status and capabilities |
| `/mcp/` | GET | MCP tools and resources |
| `/` | POST | Execute MCP tools |

## 🛠️ Available Tools

### `list_issues`
List GitHub issues from your repository.

**Parameters:**
- `state` (string): "open", "closed", or "all"
- `labels` (array): Filter by labels
- `limit` (integer): Max results (default: 10)

**Example:**
```bash
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "list_issues",
    "parameters": {"state": "open", "limit": 5}
  }'
```

### `create_issue`
Create a new GitHub issue.

**Parameters:**
- `title` (string, required): Issue title
- `body` (string): Issue description
- `labels` (array): Labels to add

**Example:**
```bash
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_issue",
    "parameters": {
      "title": "New Feature Request",
      "body": "Description here",
      "labels": ["enhancement"]
    }
  }'
```

### `get_repository_info`
Get information about the configured repository.

**Example:**
```bash
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_repository_info"}'
```

## ⚙️ Configuration

### Environment Variables

```bash
# Required
GITHUB_TOKEN=ghp_xxxx                    # GitHub Personal Access Token
GITHUB_REPO_OWNER=myou260312-eng         # Repository owner
GITHUB_REPO_NAME=repo-name               # Repository name

# Optional
MCP_ENABLED=true                         # Enable/disable MCP (default: true)
LLM_MODEL=gpt-3.5-turbo                  # LLM model to use
LOG_LEVEL=INFO                           # DEBUG, INFO, WARNING, ERROR
DEBUG_MODE=false                         # Verbose logging
VANE_ROOT_ID=VANE_ROOT_ID_8A9B3C4D5E6F7G8H  # Workspace ID
```

### Core Settings (config.py)

| Setting | Default | Purpose |
|---------|---------|---------|
| `MCP_ENABLED` | `true` | Enable/disable MCP |
| `TEMPERATURE` | `0.0` | LLM determinism (0=strict) |
| `CONFIDENCE_HIGH_THRESHOLD` | `0.85` | High confidence barrier |
| `API_TIMEOUT` | `3.5s` | External API timeout |
| `MAX_TOKENS` | `800` | Max LLM response tokens |

## 📦 Project Structure

```
skills-integrate-mcp-with-copilot/
├── config.py                      # Core configuration with MCP settings
├── mcp_server.py                  # MCP HTTP server implementation
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variable template
├── .vscode/
│   └── mcp.json                   # VS Code MCP configuration
├── MCP_DEPLOYMENT_GUIDE.md        # Complete deployment guide
└── README.md                      # This file
```

## 🔌 Using with GitHub Copilot

### In VS Code or Codespace

1. **Update `.vscode/mcp.json`** with your MCP server URL
2. **Click Start button** and authenticate
3. **Open Copilot Chat** and use:
   ```
   @github List all open issues
   @github Create issue: Bug fix needed
   @github Show repository information
   ```

## 🚀 Deploy to Production

### Railway.app (Recommended)

1. Visit [Railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Name service: `mdabul-project`
4. Add environment variables
5. Deploy! Your URL: `https://mdabul-project.railway.app/mcp/`

### Docker

```bash
docker build -t vane-mcp-server .
docker run -p 3000:3000 \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -e MCP_ENABLED=true \
  vane-mcp-server
```

### Heroku

```bash
heroku create mdabul-mcp-server
git push heroku main
heroku config:set GITHUB_TOKEN=ghp_xxxx
```

## 📖 Complete Documentation

See **[MCP_DEPLOYMENT_GUIDE.md](./MCP_DEPLOYMENT_GUIDE.md)** for:
- Detailed setup instructions
- Multiple deployment options
- Troubleshooting guide
- Testing procedures
- Cross-project usage examples

## 🧪 Testing

### Test Locally

```bash
# Server status
curl http://localhost:3000/mcp/

# List issues
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{"tool": "list_issues", "parameters": {"state": "open"}}'
```

### Test Production

```bash
curl https://mdabul-project.railway.app/mcp/
```

### Test with Copilot

In VS Code Copilot Chat:
```
@github What are the open issues?
```

## 🔄 Reuse Across Projects

You can use this MCP server in **any GitHub project**:

1. Copy `.vscode/mcp.json` to your project
2. Update `.env` with your repo credentials
3. Start using: `@github` commands in Copilot Chat

**One server. Unlimited projects. 🎯**

## 📋 Checklist

- [x] MCP server implementation
- [x] GitHub tool integration
- [x] Vane agent framework integration
- [x] Local testing
- [x] Production deployment guide
- [x] VS Code configuration
- [x] Documentation
- [x] Railway URL configured

## 🛠️ Architecture

### Core Components

**config.py** - Centralized configuration
- Workspace isolation via VANE_ROOT_ID
- MCP server settings
- LLM orchestration parameters
- Confidence thresholds
- Logging configuration

**mcp_server.py** - HTTP MCP Server
- `MCPRequestHandler` - HTTP request processing
- `MCPServer` - Server lifecycle management
- Tool execution engine
- GitHub integration interface

**Vane Agent Framework**
- Semantic caching with Chroma DB
- Confidence-based filtering
- Structured workspace management

## 🔐 Security

- GitHub token stored in `.env` (never committed)
- HTTPS enforced in production
- Request validation on all endpoints
- Error handling prevents information leakage

## 📊 Logging

Logs stored in: `workspaces/{VANE_ROOT_ID}/logs/vane_agent.log`

Configure verbosity:
```bash
LOG_LEVEL=DEBUG DEBUG_MODE=true python mcp_server.py
```

## 🤝 Contributing

This is a production MCP server. To extend:

1. Add new tools in `MCPRequestHandler.CAPABILITIES`
2. Implement handler methods: `handle_<tool_name>()`
3. Update documentation
4. Test locally before deploying

## 📝 License

MIT License - See LICENSE file for details

## 🔗 Resources

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [GitHub Copilot Extensions](https://docs.github.com/en/copilot)
- [GitHub API Reference](https://docs.github.com/en/rest)
- [Railway Documentation](https://docs.railway.app/)

## 📞 Support

For issues or questions:
1. Check [MCP_DEPLOYMENT_GUIDE.md](./MCP_DEPLOYMENT_GUIDE.md) troubleshooting section
2. Review logs: `tail -f workspaces/*/logs/vane_agent.log`
3. Test connectivity: `curl https://mdabul-project.railway.app/mcp/`

---

**Your MCP Server:** `https://mdabul-project.railway.app/mcp/`

Built by MD ABUL HOSSAIN (myou260312-eng) | 2025
