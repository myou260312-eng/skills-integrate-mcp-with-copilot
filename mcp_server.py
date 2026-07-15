"""
MCP Server Integration for Vane Agent.
Provides HTTP-based Model Context Protocol server for GitHub Copilot.
"""

import json
import logging
from typing import Any, Dict, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from config import Config

logger = logging.getLogger(__name__)


class MCPRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for MCP protocol."""
    
    # MCP Server capabilities and resources
    CAPABILITIES = {
        "tools": [
            {
                "name": "list_issues",
                "description": "List GitHub issues from the configured repository",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "state": {"type": "string", "enum": ["open", "closed", "all"]},
                        "labels": {"type": "array", "items": {"type": "string"}},
                        "limit": {"type": "integer", "default": 10}
                    }
                }
            },
            {
                "name": "create_issue",
                "description": "Create a new GitHub issue",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "body": {"type": "string"},
                        "labels": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "get_repository_info",
                "description": "Get information about the configured repository",
                "inputSchema": {"type": "object", "properties": {}}
            }
        ],
        "resources": [
            {
                "uri": "github://repository",
                "name": "GitHub Repository",
                "description": "Access to GitHub repository data and operations"
            }
        ]
    }
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "status": "MCP Server Running",
                "version": "1.0.0",
                "capabilities": self.CAPABILITIES
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == "/mcp/":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "tools": self.CAPABILITIES["tools"],
                "resources": self.CAPABILITIES["resources"]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for tool execution."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        
        try:
            request_data = json.loads(body.decode())
            tool_name = request_data.get("tool")
            parameters = request_data.get("parameters", {})
            
            logger.info(f"Executing tool: {tool_name} with parameters: {parameters}")
            
            # Execute tool based on name
            if tool_name == "list_issues":
                result = self.handle_list_issues(parameters)
            elif tool_name == "create_issue":
                result = self.handle_create_issue(parameters)
            elif tool_name == "get_repository_info":
                result = self.handle_get_repository_info(parameters)
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            self.send_response(500)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def handle_list_issues(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_issues tool call."""
        # This would integrate with GitHub API
        return {
            "success": True,
            "issues": [],
            "message": "Issue listing requires GITHUB_TOKEN configuration"
        }
    
    def handle_create_issue(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle create_issue tool call."""
        title = parameters.get("title", "")
        if not title:
            return {"error": "Title is required"}
        
        return {
            "success": True,
            "issue": {
                "title": title,
                "body": parameters.get("body", ""),
                "labels": parameters.get("labels", [])
            },
            "message": "Issue creation requires GITHUB_TOKEN configuration"
        }
    
    def handle_get_repository_info(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Handle get_repository_info tool call."""
        return {
            "success": True,
            "repository": {
                "owner": Config.GITHUB_REPO_OWNER,
                "name": Config.GITHUB_REPO_NAME,
                "mcp_enabled": Config.MCP_ENABLED
            }
        }
    
    def log_message(self, format, *args):
        """Override to use configured logger."""
        logger.info(format % args)


class MCPServer:
    """MCP Server wrapper for managing the HTTP server."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        self.host = host
        self.port = port
        self.server = None
        self.thread = None
    
    def start(self):
        """Start the MCP server in a background thread."""
        self.server = HTTPServer((self.host, self.port), MCPRequestHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        logger.info(f"✅ MCP Server started at http://{self.host}:{self.port}")
    
    def stop(self):
        """Stop the MCP server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("❌ MCP Server stopped")


def setup_logging():
    """Configure logging for MCP server."""
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler()
        ]
    )


if __name__ == "__main__":
    setup_logging()
    Config.validate_environment()
    
    mcp_server = MCPServer(host="0.0.0.0", port=3000)
    mcp_server.start()
    
    try:
        print("🚀 MCP Server is running. Press Ctrl+C to stop.")
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        mcp_server.stop()
        print("\n✨ MCP Server shutdown gracefully")
