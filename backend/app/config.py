"""
Configuration module for AI Orchestra Dashboard
Handles environment variables and settings validation
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        self.github_token: Optional[str] = os.getenv('GITHUB_TOKEN')
        self.github_org: str = os.getenv('GITHUB_ORG', 'ihw33')
        self.default_repo: str = os.getenv('DEFAULT_REPO', 'ai-orchestra-dashboard')
        
    def validate(self) -> None:
        """
        Validate required settings
        Raises ValueError if required settings are missing
        """
        if not self.github_token:
            raise ValueError(
                "GITHUB_TOKEN is required. "
                "Please set it in your .env file or environment variables."
            )
        
        if not self.github_org:
            raise ValueError(
                "GITHUB_ORG is required. "
                "Please set it in your .env file or environment variables."
            )
    
    def __repr__(self) -> str:
        """String representation for debugging"""
        return (
            f"Settings("
            f"github_org={self.github_org}, "
            f"default_repo={self.default_repo}, "
            f"token={'***' if self.github_token else 'NOT_SET'})"
        )


# Create singleton instance
settings = Settings()

# Export for easy import
__all__ = ['settings', 'Settings']