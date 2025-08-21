#!/bin/bash

# AI Orchestra Process Manager
# 전체 업무 프로세스 관리 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# 함수: 상태 출력
print_status() {
    echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# 함수: 새 업무 생성
create_new_task() {
    local title="$1"
    local description="$2"
    
    print_status "새 업무 생성 중: $title"
    
    # PM에게 업무 전달
    osascript pm_task_distributor.applescript "$title" "$description"
    
    # GitHub Issue 생성 (예시)
    # gh issue create --title "$title" --body "$description" --label "task"
    
    print_success "업무 생성 완료"
}

# 함수: 업무 배분
distribute_tasks() {
    print_status "업무를 팀원들에게 배분 중..."
    
    # Gemini: 기획/문서
    osascript assign_task_to_cli.applescript 5 "Gemini" "프로젝트 기획 문서 작성 및 사용자 가이드 준비"
    sleep 2
    
    # Codex: 백엔드
    osascript assign_task_to_cli.applescript 6 "Codex" "API 엔드포인트 구현 및 데이터베이스 스키마 설계"
    sleep 2
    
    # Claude2: 프론트엔드 (세션 7이 있다면)
    # osascript assign_task_to_cli.applescript 7 "Claude2" "UI 컴포넌트 개발 및 스타일링"
    
    print_success "업무 배분 완료"
}

# 함수: 진행 상황 모니터링
monitor_progress() {
    print_status "진행 상황 모니터링 중..."
    
    while true; do
        # 완료 보고 수집
        result=$(osascript collect_completion_report.applescript)
        echo -e "${CYAN}$result${NC}"
        
        # 30초마다 체크
        sleep 30
        
        # 완료 신호 확인 (예: 특정 파일 존재 여부)
        if [[ -f "/tmp/ai_orchestra_complete.flag" ]]; then
            print_success "모든 작업 완료!"
            rm -f /tmp/ai_orchestra_complete.flag
            break
        fi
    done
}

# 함수: 결과 검증 및 승인
verify_and_approve() {
    print_status "작업 결과 검증 중..."
    
    # 여기에 실제 검증 로직 추가
    # 예: 테스트 실행, 코드 리뷰 등
    
    read -p "작업을 승인하시겠습니까? (y/n): " approval
    
    if [[ "$approval" == "y" ]]; then
        print_success "작업 승인됨"
        # GitHub Issue 닫기
        # gh issue close <issue_number>
    else
        print_warning "추가 작업 필요"
        # 추가 지시사항 입력 받기
        read -p "추가 지시사항: " additional_instructions
        # 해당 CLI에 추가 작업 전달
    fi
}

# 메인 메뉴
show_menu() {
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo -e "${PURPLE}    AI Orchestra Process Manager${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
    echo "1. 새 업무 생성"
    echo "2. 업무 배분"
    echo "3. 진행 상황 모니터링"
    echo "4. 완료 보고 수집"
    echo "5. 결과 검증 및 승인"
    echo "6. 전체 프로세스 실행"
    echo "0. 종료"
    echo -e "${PURPLE}═══════════════════════════════════════${NC}"
}

# 메인 루프
main() {
    while true; do
        show_menu
        read -p "선택: " choice
        
        case $choice in
            1)
                read -p "업무 제목: " title
                read -p "업무 설명: " description
                create_new_task "$title" "$description"
                ;;
            2)
                distribute_tasks
                ;;
            3)
                monitor_progress
                ;;
            4)
                osascript collect_completion_report.applescript
                ;;
            5)
                verify_and_approve
                ;;
            6)
                # 전체 프로세스 실행
                read -p "업무 제목: " title
                read -p "업무 설명: " description
                create_new_task "$title" "$description"
                sleep 3
                distribute_tasks
                sleep 5
                monitor_progress
                verify_and_approve
                ;;
            0)
                print_status "종료합니다."
                exit 0
                ;;
            *)
                print_error "잘못된 선택입니다."
                ;;
        esac
        
        echo ""
        read -p "계속하려면 Enter를 누르세요..."
    done
}

# 스크립트 실행
main