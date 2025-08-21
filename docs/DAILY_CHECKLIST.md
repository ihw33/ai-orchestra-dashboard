# ✅ Daily Operations Checklist

## 🌅 Morning Standup Process

### PM Claude Morning Routine (First 15 minutes)

#### 1. System Health Check (5 minutes)
```bash
# Navigate to project
cd /Users/m4_macbook/Projects/ai-orchestra-dashboard

# Check running services
ps aux | grep -E "(uvicorn|npm|node)"

# Verify frontend is running
curl -s http://localhost:3000 > /dev/null && echo "✅ Frontend OK" || echo "❌ Frontend DOWN"

# Verify backend is running  
curl -s http://localhost:8001/health > /dev/null && echo "✅ Backend OK" || echo "❌ Backend DOWN"

# Check GitHub CLI authentication
gh auth status
```

#### 2. Team Status Assessment (5 minutes)
```bash
# Check active issues
gh issue list -R ihw33/ai-orchestra-dashboard --state open --assignee @me
gh issue list -R ihw33/ai-orchestra-dashboard --state open --label "in-progress"

# Review yesterday's progress
gh issue list -R ihw33/ai-orchestra-dashboard --search "updated:>=$(date -d '1 day ago' +%Y-%m-%d)"

# Check for blockers
gh issue list -R ihw33/ai-orchestra-dashboard --label "blocked" --state open
```

#### 3. Sprint Progress Review (5 minutes)
```bash
# Round 2 progress check
gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state all

# Calculate completion rate
TOTAL_ROUND2=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state all --json number | jq length)
COMPLETED_ROUND2=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state closed --json number | jq length)
echo "Round 2 Progress: $COMPLETED_ROUND2/$TOTAL_ROUND2 ($(($COMPLETED_ROUND2 * 100 / $TOTAL_ROUND2))%)"
```

### Team Member Morning Check-in (Each member, 10 minutes)

#### Gemini Morning Routine
```bash
# 1. Verify AI mode status
echo "Current mode check..."
!  # Switch to AI mode if needed

# 2. Check assigned tasks
gh issue list -R ihw33/ai-orchestra-dashboard --assignee @me --state open

# 3. Report availability
gh issue comment [active-issue-number] --body "Gemini 🌅 Morning check-in complete, ready for tasks"
```

#### Codex Morning Routine
```bash
# 1. Check assigned backend tasks
gh issue list -R ihw33/ai-orchestra-dashboard --label "backend" --assignee @me --state open

# 2. Verify development environment
cd /Users/m4_macbook/Projects/ai-orchestra-dashboard/backend
source venv/bin/activate
python -c "import app; print('✅ Backend environment OK')"

# 3. Report status
gh issue comment [active-issue-number] --body "Codex 🌅 Environment verified, ready for backend development"
```

#### VSCode Claude Morning Routine
```bash
# 1. Check frontend tasks
gh issue list -R ihw33/ai-orchestra-dashboard --label "frontend" --assignee @me --state open

# 2. Verify Node.js environment
cd /Users/m4_macbook/Projects/ai-orchestra-dashboard/frontend
npm run type-check
echo "✅ Frontend environment OK"

# 3. Report availability
gh issue comment [active-issue-number] --body "VSCode Claude 🌅 Frontend environment ready, standing by"
```

#### Cursor ChatGPT Morning Routine
```applescript
# Open Cursor and report status
tell application "Cursor"
    activate
    delay 1
end tell

tell application "System Events"
    keystroke "k" using {command down}  # Cmd+K for AI chat
    delay 2
    type "🌅 Morning check-in: Ready for design and UX tasks. Checking assigned issues..."
    keystroke return
end tell
```

---

## 📋 Task Review and Assignment

### Priority Assessment Matrix

| Priority | Criteria | Response Time | Escalation |
|----------|----------|---------------|------------|
| **P0 (Critical)** | Blocking other work, production issues | 15 minutes | Immediate |
| **P1 (High)** | Sprint goals, major features | 1 hour | Same day |
| **P2 (Medium)** | Enhancements, optimizations | 4 hours | Next day |
| **P3 (Low)** | Nice-to-have, documentation | 24 hours | End of sprint |

### Task Assignment Process

#### 1. Review New Issues (10 minutes)
```bash
# Check for unassigned issues
gh issue list -R ihw33/ai-orchestra-dashboard --no-assignee --state open

# Review issue details and assign based on specialization
for issue in $(gh issue list -R ihw33/ai-orchestra-dashboard --no-assignee --state open --json number | jq -r '.[].number'); do
    echo "Reviewing issue #$issue"
    gh issue view $issue
    # Manual assignment based on content
done
```

#### 2. Workload Balancing Check
```bash
# Check current workload per member
echo "=== Current Team Workload ==="
echo "Gemini:"
gh issue list -R ihw33/ai-orchestra-dashboard --assignee "user-gemini" --state open --json title | jq length

echo "Codex:"  
gh issue list -R ihw33/ai-orchestra-dashboard --assignee "user-codex" --state open --json title | jq length

echo "VSCode Claude:"
gh issue list -R ihw33/ai-orchestra-dashboard --assignee "user-vscode-claude" --state open --json title | jq length

echo "Cursor ChatGPT:"
gh issue list -R ihw33/ai-orchestra-dashboard --assignee "user-cursor" --state open --json title | jq length
```

#### 3. Assignment Distribution
```bash
# Assign issues based on expertise and workload
assign_task() {
    local issue_number=$1
    local member=$2
    local notify_script=$3
    
    gh issue edit $issue_number --add-assignee $member
    gh issue comment $issue_number --body "🎯 Task assigned to $member. Please acknowledge within 5 minutes."
    
    # Send notification via AppleScript
    osascript $notify_script "New task assigned: Issue #$issue_number"
}

# Example assignments
# assign_task 123 "user-gemini" "notify_gemini.applescript"
# assign_task 124 "user-codex" "notify_codex.applescript"
```

---

## 📊 Progress Monitoring Checkpoints

### 30-Minute Progress Check

#### Automated Monitoring Script
```bash
#!/bin/bash
# check_progress.sh - Run every 30 minutes

echo "🔍 Progress Check - $(date)"

# Check for overdue progress reports
THIRTY_MIN_AGO=$(date -d '30 minutes ago' '+%Y-%m-%dT%H:%M:%S')

# Get issues with in-progress status
IN_PROGRESS_ISSUES=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "in-progress" --state open --json number,assignees,updatedAt)

echo "$IN_PROGRESS_ISSUES" | jq -r '.[] | select(.updatedAt < "'$THIRTY_MIN_AGO'") | "⚠️  Issue #\(.number) - No update from \(.assignees[0].login) for >30 minutes"'

# Check for stuck sessions
echo "📡 Checking session responsiveness..."
osascript -e 'tell application "iTerm2" to get name of every session of tab 4'

# Generate progress summary
TOTAL_ACTIVE=$(echo "$IN_PROGRESS_ISSUES" | jq length)
echo "📊 Active tasks: $TOTAL_ACTIVE"
```

### Hourly Health Check

#### System Resources
```bash
# check_system_health.sh
echo "🏥 System Health Check - $(date)"

# Memory usage
echo "Memory Usage:"
ps aux | awk '{print $4" "$11}' | sort -n | tail -5

# Disk usage
echo "Disk Usage:"
df -h /Users/m4_macbook/Projects/ai-orchestra-dashboard

# Process monitoring
echo "AI Orchestra Processes:"
ps aux | grep -E "(uvicorn|npm|node)" | grep -v grep

# GitHub API rate limit
echo "GitHub Rate Limit:"
gh api rate_limit --jq '.rate | "Used: \(.used)/\(.limit) (Reset: \(.reset | strftime("%H:%M:%S")))"'
```

### End-of-Sprint Review

#### Completion Analysis
```bash
# sprint_review.sh
echo "🏁 Sprint Review - Round 2"

# Calculate completion metrics
ROUND2_TOTAL=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state all --json number | jq length)
ROUND2_COMPLETED=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state closed --json number | jq length)
COMPLETION_RATE=$(($ROUND2_COMPLETED * 100 / $ROUND2_TOTAL))

echo "📊 Completion Rate: $COMPLETION_RATE% ($ROUND2_COMPLETED/$ROUND2_TOTAL)"

# Identify remaining tasks
echo "📋 Remaining Tasks:"
gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state open --json number,title | jq -r '.[] | "- Issue #\(.number): \(.title)"'

# Team performance summary
echo "👥 Team Performance:"
for member in "gemini" "codex" "vscode-claude" "cursor-chatgpt"; do
    MEMBER_COMPLETED=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "round-2" --state closed --search "assignee:user-$member" --json number | jq length)
    echo "- $member: $MEMBER_COMPLETED tasks completed"
done
```

---

## 🚨 Blocker Resolution Workflow

### Immediate Response (0-15 minutes)

#### Blocker Detection
```bash
# detect_blockers.sh - Run every 5 minutes
echo "🚨 Checking for blockers..."

# Check for blocked issues
BLOCKED_ISSUES=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "blocked" --state open --json number,title,assignees,updatedAt)

if [[ $(echo "$BLOCKED_ISSUES" | jq length) -gt 0 ]]; then
    echo "🚨 BLOCKERS DETECTED:"
    echo "$BLOCKED_ISSUES" | jq -r '.[] | "Issue #\(.number): \(.title) (Assigned to: \(.assignees[0].login))"'
    
    # Auto-escalate critical blockers
    echo "$BLOCKED_ISSUES" | jq -r '.[] | select(.labels[]?.name == "p0") | .number' | while read issue_num; do
        gh issue comment $issue_num --body "🚨 CRITICAL BLOCKER ESCALATED - PM Claude investigating immediately"
    done
fi
```

#### Resolution Strategies
```bash
# resolve_blocker.sh
resolve_blocker() {
    local issue_number=$1
    local blocker_type=$2
    
    case $blocker_type in
        "dependency")
            echo "🔧 Resolving dependency blocker for issue #$issue_number"
            # Check for missing dependencies
            # Attempt automatic installation
            ;;
        "environment")
            echo "🔧 Resolving environment blocker for issue #$issue_number"
            # Reset development environment
            # Restart necessary services
            ;;
        "knowledge")
            echo "🔧 Resolving knowledge blocker for issue #$issue_number"
            # Provide documentation links
            # Assign mentor/helper
            ;;
        "resource")
            echo "🔧 Resolving resource blocker for issue #$issue_number"
            # Redistribute workload
            # Prioritize resource allocation
            ;;
    esac
}
```

### Escalation Process

#### Level 1: Automated Resolution (0-15 minutes)
- Restart stuck processes
- Clear temporary files
- Reset environment variables
- Retry failed operations

#### Level 2: Team Collaboration (15-60 minutes)
- Assign helper team member
- Share knowledge resources
- Pair programming session
- Alternative approach suggestions

#### Level 3: PM Intervention (1+ hour)
- Task reassignment
- Scope reduction
- External resource allocation
- Stakeholder notification

---

## 🌙 End-of-Day Reporting

### Team Member End-of-Day Report

#### Template for All Members
```bash
# end_of_day_report.sh [member-name]
MEMBER_NAME=$1
TODAY=$(date +%Y-%m-%d)

echo "📊 End of Day Report - $MEMBER_NAME - $TODAY"

# Get today's activities
TODAY_COMMENTS=$(gh issue list -R ihw33/ai-orchestra-dashboard --search "commenter:user-$MEMBER_NAME updated:>=$TODAY" --json number,title)

echo "💬 Issues worked on today:"
echo "$TODAY_COMMENTS" | jq -r '.[] | "- Issue #\(.number): \(.title)"'

# Calculate productivity metrics
TOTAL_COMMENTS=$(echo "$TODAY_COMMENTS" | jq length)
echo "📈 Activity: $TOTAL_COMMENTS issue interactions"

# Current status
ACTIVE_ISSUES=$(gh issue list -R ihw33/ai-orchestra-dashboard --assignee "user-$MEMBER_NAME" --state open --json number,title)
echo "🎯 Active assignments:"
echo "$ACTIVE_ISSUES" | jq -r '.[] | "- Issue #\(.number): \(.title)"'
```

#### PM Claude Consolidated Report
```bash
# daily_summary.sh
echo "📊 Daily Summary Report - $(date +%Y-%m-%d)"

# Sprint progress
ROUND2_PROGRESS=$(./scripts/calculate_sprint_progress.sh)
echo "🏁 Round 2 Progress: $ROUND2_PROGRESS"

# Team productivity
echo "👥 Team Productivity:"
for member in "gemini" "codex" "vscode-claude" "cursor-chatgpt"; do
    MEMBER_ACTIVITY=$(gh api "search/issues?q=repo:ihw33/ai-orchestra-dashboard+commenter:user-$member+updated:>=$(date +%Y-%m-%d)" --jq '.total_count')
    echo "- $member: $MEMBER_ACTIVITY activities"
done

# Blockers summary
ACTIVE_BLOCKERS=$(gh issue list -R ihw33/ai-orchestra-dashboard --label "blocked" --state open --json number | jq length)
echo "🚨 Active Blockers: $ACTIVE_BLOCKERS"

# Tomorrow's priorities
echo "📋 Tomorrow's Priorities:"
gh issue list -R ihw33/ai-orchestra-dashboard --label "p0,p1" --state open --json number,title | jq -r '.[] | "- Issue #\(.number): \(.title)"'
```

---

## 🔄 Weekly Operations

### Monday Sprint Planning
- [ ] Review previous sprint completion
- [ ] Set new sprint goals
- [ ] Assign initial tasks
- [ ] Update project timeline

### Wednesday Mid-Sprint Review
- [ ] Progress assessment
- [ ] Blocker identification
- [ ] Resource reallocation
- [ ] Scope adjustments

### Friday Sprint Retrospective
- [ ] Completion analysis
- [ ] Team performance review
- [ ] Process improvements
- [ ] Next sprint preparation

---

## 🛠️ Quick Reference Commands

### Essential Daily Commands
```bash
# Morning startup
./scripts/morning_startup.sh

# Progress check
./scripts/check_progress.sh

# Assign new task
./scripts/assign_task.sh [issue-number] [member]

# Handle blocker
./scripts/handle_blocker.sh [issue-number] [type]

# End of day summary
./scripts/daily_summary.sh
```

### Emergency Procedures
```bash
# System restart
./scripts/emergency_restart.sh

# Reset all sessions
./scripts/reset_sessions.sh

# Backup current state
./scripts/backup_state.sh

# Restore from backup
./scripts/restore_backup.sh [backup-id]
```

---

**📅 Last Updated**: August 21, 2025  
**✅ Checklist Version**: 2.0  
**🔄 Review Schedule**: Weekly retrospectives  
**📝 Maintained by**: Documentation AI (Task Master)  
**🎯 Optimized for**: Round 2 Operations