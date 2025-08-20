"""
GitHub Service Module
Issue #26: API 클라이언트 인증 구현
"""

from typing import Optional, Dict, Any
from github import Github, GithubException
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class GitHubService:
    """GitHub API 서비스 클래스"""
    
    def __init__(self):
        """초기화 - 토큰은 settings에서 가져옴"""
        self.token = settings.github_token
        self.client: Optional[Github] = None
        self.authenticated = False
        self.user_info: Optional[Dict[str, Any]] = None
    
    def authenticate(self) -> Dict[str, Any]:
        """
        GitHub 인증 수행
        
        Returns:
            Dict containing:
                - success (bool): 인증 성공 여부
                - message (str): 결과 메시지
                - user (dict|None): 인증된 사용자 정보
                - error (str|None): 에러 메시지
        """
        try:
            # 토큰이 없는 경우
            if not self.token:
                logger.warning("GitHub token not configured")
                return {
                    "success": False,
                    "message": "GitHub token not configured",
                    "user": None,
                    "error": "MISSING_TOKEN"
                }
            
            # PyGithub 클라이언트 생성
            self.client = Github(self.token)
            
            # 인증 테스트 - 현재 사용자 정보 가져오기
            user = self.client.get_user()
            
            # 사용자 정보 저장
            self.user_info = {
                "login": user.login,
                "name": user.name,
                "email": user.email,
                "bio": user.bio,
                "public_repos": user.public_repos,
                "followers": user.followers,
                "following": user.following,
                "created_at": user.created_at.isoformat() if user.created_at else None,
            }
            
            self.authenticated = True
            logger.info(f"Successfully authenticated as {user.login}")
            
            return {
                "success": True,
                "message": f"Successfully authenticated as {user.login}",
                "user": self.user_info,
                "error": None
            }
            
        except GithubException as e:
            # GitHub API 에러 처리
            error_message = f"GitHub API error: {e.data.get('message', str(e))}"
            logger.error(error_message)
            
            # 401 Unauthorized - 토큰이 유효하지 않음
            if e.status == 401:
                return {
                    "success": False,
                    "message": "Invalid GitHub token",
                    "user": None,
                    "error": "INVALID_TOKEN"
                }
            
            # 403 Forbidden - Rate limit 또는 권한 부족
            elif e.status == 403:
                return {
                    "success": False,
                    "message": "Access forbidden - check rate limits or token permissions",
                    "user": None,
                    "error": "FORBIDDEN"
                }
            
            # 기타 GitHub API 에러
            return {
                "success": False,
                "message": error_message,
                "user": None,
                "error": f"GITHUB_ERROR_{e.status}"
            }
            
        except Exception as e:
            # 예상치 못한 에러
            error_message = f"Unexpected error during authentication: {str(e)}"
            logger.error(error_message)
            
            return {
                "success": False,
                "message": error_message,
                "user": None,
                "error": "UNEXPECTED_ERROR"
            }
    
    def is_authenticated(self) -> bool:
        """인증 상태 확인"""
        return self.authenticated
    
    def get_client(self) -> Optional[Github]:
        """GitHub 클라이언트 반환"""
        if not self.authenticated:
            self.authenticate()
        return self.client
    
    def get_rate_limit(self) -> Dict[str, Any]:
        """
        API Rate Limit 정보 조회
        
        Returns:
            Rate limit 정보 딕셔너리
        """
        if not self.client:
            return {"error": "Not authenticated"}
        
        try:
            rate_limit = self.client.get_rate_limit()
            core = rate_limit.core
            
            return {
                "limit": core.limit,
                "remaining": core.remaining,
                "reset": core.reset.isoformat(),
                "used": core.limit - core.remaining
            }
        except Exception as e:
            logger.error(f"Error getting rate limit: {e}")
            return {"error": str(e)}


# Singleton 인스턴스
github_service = GitHubService()