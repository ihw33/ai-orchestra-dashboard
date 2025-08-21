"""
Authentication Router
Issue #26: API 클라이언트 인증 구현
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.services.github_service import github_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@router.get("/test")
async def test_authentication() -> Dict[str, Any]:
    """
    GitHub 인증 테스트 엔드포인트
    
    Returns:
        인증 결과 정보:
        - success: 인증 성공 여부
        - message: 결과 메시지
        - user: 인증된 사용자 정보 (성공시)
        - error: 에러 코드 (실패시)
        - rate_limit: API rate limit 정보
    """
    logger.info("Testing GitHub authentication...")
    
    # GitHub 인증 수행
    auth_result = github_service.authenticate()
    
    # Rate limit 정보 추가
    if auth_result["success"]:
        rate_limit = github_service.get_rate_limit()
        auth_result["rate_limit"] = rate_limit
    
    # 인증 실패시 HTTP 401 반환
    if not auth_result["success"]:
        raise HTTPException(
            status_code=401,
            detail={
                "message": auth_result["message"],
                "error": auth_result["error"]
            }
        )
    
    return auth_result


@router.get("/status")
async def authentication_status() -> Dict[str, Any]:
    """
    현재 인증 상태 확인
    
    Returns:
        인증 상태 정보
    """
    is_authenticated = github_service.is_authenticated()
    
    response = {
        "authenticated": is_authenticated,
        "user": github_service.user_info if is_authenticated else None
    }
    
    # 인증되어 있으면 rate limit 정보도 포함
    if is_authenticated:
        response["rate_limit"] = github_service.get_rate_limit()
    
    return response


@router.post("/refresh")
async def refresh_authentication() -> Dict[str, Any]:
    """
    인증 정보 갱신
    
    Returns:
        갱신된 인증 정보
    """
    logger.info("Refreshing GitHub authentication...")
    
    # 기존 인증 정보 초기화
    github_service.authenticated = False
    github_service.client = None
    github_service.user_info = None
    
    # 재인증 수행
    auth_result = github_service.authenticate()
    
    # Rate limit 정보 추가
    if auth_result["success"]:
        rate_limit = github_service.get_rate_limit()
        auth_result["rate_limit"] = rate_limit
    
    # 인증 실패시 HTTP 401 반환
    if not auth_result["success"]:
        raise HTTPException(
            status_code=401,
            detail={
                "message": auth_result["message"],
                "error": auth_result["error"]
            }
        )
    
    return auth_result