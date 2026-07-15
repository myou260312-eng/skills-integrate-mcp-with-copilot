import os
from pathlib import Path
from typing import Optional

class Config:
    """
    Central configuration for Vane Agent with MCP integration.
    Manages workspace isolation, LLM orchestration, and MCP server configuration.
    """
    
    # ==================== CORE AGENT IDENTITY & WORKSPACE ====================
    VANE_ROOT_ID = os.getenv("VANE_ROOT_ID", "VANE_ROOT_ID_8A9B3C4D5E6F7G8H")
    BASE_DIR = Path(__file__).resolve().parent
    
    # Workspace isolation using the Vane Root ID
    WORKSPACE_DIR = BASE_DIR / "workspaces" / VANE_ROOT_ID
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    
    # ==================== VECTOR DATABASE CONFIGURATION ====================
    CHROMA_PERSIST_DIR = str(WORKSPACE_DIR / "chroma_db")
    EMBEDDING_MODEL = "text-embedding-3-small"
    CHROMA_COLLECTION_NAME = "vane_semantic_store"
    
    # ==================== LLM ORCHESTRATION ====================
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    TEMPERATURE = 0.0  # Strict deterministic fact-checking
    MAX_TOKENS = 800
    LLM_TIMEOUT = 30.0  # Seconds
    
    # ==================== API NETWORK THRESHOLDS ====================
    API_TIMEOUT = 3.5  # Seconds before discarding lagging external web fetches
    MAX_SEARCH_RESULTS = 4
    RETRY_ATTEMPTS = 3
    RETRY_BACKOFF = 1.5
    
    # ==================== CONFIDENCE SCORE BOUNDARIES ====================
    CONFIDENCE_HIGH_THRESHOLD = 0.85
    CONFIDENCE_MEDIUM_THRESHOLD = 0.60
    CONFIDENCE_LOW_THRESHOLD = 0.40
    
    # ==================== MCP SERVER CONFIGURATION ====================
    MCP_ENABLED = os.getenv("MCP_ENABLED", "true").lower() == "true"
    MCP_SERVERS = {
        "github": {
            "type": "http",
            "url": os.getenv("MCP_GITHUB_URL", "https://api.githubcopilot.com/mcp/"),
            "enabled": True,
            "timeout": 5.0
        }
    }
    
    # ==================== GITHUB INTEGRATION ====================
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITHUB_API_BASE = "https://api.github.com"
    GITHUB_REPO_OWNER = os.getenv("GITHUB_REPO_OWNER", "")
    GITHUB_REPO_NAME = os.getenv("GITHUB_REPO_NAME", "")
    
    # ==================== LOGGING CONFIGURATION ====================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR = WORKSPACE_DIR / "logs"
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = LOG_DIR / "vane_agent.log"
    
    # ==================== FEATURE FLAGS ====================
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
    ENABLE_SEMANTIC_CACHE = os.getenv("ENABLE_SEMANTIC_CACHE", "true").lower() == "true"
    ENABLE_STRUCTURED_OUTPUT = True
    
    @classmethod
    def get_mcp_server_config(cls, server_name: str) -> Optional[dict]:
        """Retrieve MCP server configuration by name."""
        return cls.MCP_SERVERS.get(server_name) if cls.MCP_ENABLED else None
    
    @classmethod
    def validate_environment(cls) -> bool:
        """Validate critical environment variables are set."""
        required_vars = ["GITHUB_TOKEN"] if cls.MCP_ENABLED else []
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            print(f"⚠️  Warning: Missing environment variables: {', '.join(missing)}")
            return False
        return True
