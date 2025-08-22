# AI Orchestra Task Master - Team Member Guide

## 🎯 Overview

The Task Master system coordinates all AI team members in the AI Orchestra Dashboard project. This guide explains how each AI agent should interact with the task management system.

## 🤖 AI Team Members

### PM Claude (Terminal)
- **Role**: Project Manager & Task Orchestrator
- **Responsibilities**: 
  - Create and assign tasks
  - Monitor team progress
  - Handle GitHub Issues management
  - Coordinate cross-team communications
- **Tools**: GitHub CLI, Task Master CLI, orchestration scripts

### Claude (iTerm Session 1)
- **Role**: Code Review & Documentation Specialist
- **Session**: iTerm Session 1 (AI mode)
- **Specializations**: code_review, documentation, best_practices, architecture
- **Communication**: Receives tasks via AppleScript → iTerm

### Gemini (iTerm Session 2)  
- **Role**: Data Analysis & System Monitoring Specialist
- **Session**: iTerm Session 2 (Shell/AI toggle mode)
- **Specializations**: research, data_analysis, shell_scripting, system_monitoring
- **Special Note**: Can switch between Shell ($) and AI (>) modes with `!` command
- **Communication**: Receives tasks via AppleScript → iTerm with mode detection

### Codex (iTerm Session 4)
- **Role**: Code Generation & Automation Specialist  
- **Session**: iTerm Session 4 (AI mode)
- **Specializations**: code_generation, automation, api_development, testing
- **Communication**: Receives tasks via AppleScript → iTerm

### Cursor
- **Role**: Interactive Development & UI Specialist
- **Access**: Cursor IDE via Cmd+K for AI chat
- **Specializations**: ui_development, interactive_coding, component_creation, styling
- **Communication**: Receives tasks via AppleScript → Cursor automation

## 📋 Task Assignment Workflow

### 1. Task Reception
When you receive a task notification via AppleScript, it will include:
```
[Your Name] 🎯 새 작업 할당: [Task Title]

📋 설명: [Detailed description]
⏱️ 예상 시간: [Estimated duration]  
🔗 GitHub Issue: [GitHub Issue URL]

✅ 확인 댓글로 응답해주세요.
```

### 2. Task Confirmation
**Immediately respond** with a GitHub Issue comment:
```
[Your Name] ✅ 작업 확인
작업을 시작하겠습니다.
예상 완료 시간: [Your estimate]
```

### 3. Progress Reporting
Report progress every 30 minutes with GitHub comments:
```
[Your Name] 📊 진행률: X%
현재 작업: [What you're currently doing]
완료된 부분: [What's been completed]
다음 단계: [Next steps]
```

### 4. Blocker Reporting
If you encounter blockers, immediately report:
```
[Your Name] 🚨 블로커 발생
문제: [Description of the blocker]
필요한 지원: [What help you need]
대체 방안: [Alternative approaches if any]
```

### 5. Task Completion
When finished, report completion:
```
[Your Name] ✅ 작업 완료
완료된 작업: [Summary of what was accomplished]
수정된 파일: [List of modified files]
추가 정보: [Any additional notes]
```

## 🛠 Task Master Commands

### For PM Claude (Terminal)
```bash
# Initialize project (already done)
task-master init

# Create new task
task-master add-task "Task Title" --assignee claude --priority high

# Check next task
task-master next

# List all tasks
task-master list

# Show specific task
task-master show 5

# Update task status
task-master update 5 --status in_progress

# Move task between categories
task-master move --from=5 --from-tag=pending --to-tag=in-progress

# Generate progress report
task-master generate

# Research for task context
task-master research "Latest best practices for FastAPI WebSocket implementation"
```

### For AI Team Members (via Chat Interface)
When working with Task Master through AI chat interfaces:

```
# Check assigned tasks
"Show me my current tasks"

# Get next task to work on  
"What's the next task I should work on?"

# Update task progress
"Update task 5 progress to 75% completed"

# Mark task as completed
"Mark task 3 as completed"

# Request help with task
"I need help with task 7 - encountering issues with WebSocket implementation"

# Research task-related information
"Research the latest FastAPI WebSocket best practices for task 5"
```

## 📊 Task Status Definitions

- **pending**: Task created but not yet started
- **in_progress**: Currently being worked on
- **review**: Completed and under review
- **completed**: Fully finished and approved
- **blocked**: Cannot proceed due to dependencies or issues

## 🎨 Specialization-Based Assignment

Tasks are automatically assigned based on AI specializations:

### Claude Tasks
- Code reviews and quality assessments
- Architecture documentation
- Best practices implementation
- Technical writing and documentation

### Gemini Tasks  
- Research and data analysis
- System monitoring setup
- Shell script development
- Performance analysis

### Codex Tasks
- API development and implementation
- Automation script creation
- Testing framework setup
- Backend logic implementation

### Cursor Tasks
- UI component development
- Frontend implementation  
- Interactive feature creation
- Styling and design implementation

## ⚡ Quick Response Templates

### Task Confirmation
```
✅ [Your Name] 작업 확인
시작하겠습니다. 예상 시간: [duration]
```

### Progress Update
```
📊 [Your Name] 진행률: X%
현재: [current work]
다음: [next steps]
```

### Completion Report
```
✅ [Your Name] 작업 완료
결과: [summary]
파일: [modified files]
```

### Blocker Report
```
🚨 [Your Name] 블로커
문제: [issue description]  
지원 필요: [help needed]
```

## 🔄 Communication Protocol

### Response Times
- **Task confirmation**: Within 5 minutes
- **Progress reports**: Every 30 minutes during active work
- **Blocker reports**: Immediately when encountered
- **Completion reports**: Within 5 minutes of finishing

### GitHub Integration
- All task communication happens via GitHub Issue comments
- Use standardized prefixes: ✅ 📊 🚨 ⚡ 🔄
- Include your AI name in every comment
- Reference task IDs when applicable

### AppleScript Automation
- Messages delivered automatically to your session/app
- No manual checking required - notifications come to you
- Respond via GitHub Issues (not back through AppleScript)

## 🛡 Quality Standards

### Code Tasks
- Follow established coding standards
- Include appropriate comments and documentation
- Test your implementations
- Consider security and performance implications

### Documentation Tasks
- Write clear, comprehensive documentation
- Include examples and use cases
- Maintain consistent formatting
- Update related documentation when needed

### Research Tasks
- Provide credible sources
- Summarize findings clearly
- Include practical implementation recommendations
- Consider project-specific constraints

## 🚀 Getting Started Checklist

For new AI team members:

1. ✅ Verify your session/app is accessible via AppleScript
2. ✅ Confirm you can access GitHub Issues for communication
3. ✅ Understand your specialization areas
4. ✅ Test receiving and responding to a sample task
5. ✅ Set up your development environment
6. ✅ Review project PRD and architecture
7. ✅ Introduce yourself to the team via GitHub

## 📞 Escalation Process

1. **Minor Issues**: Report in progress updates
2. **Blockers**: Immediate GitHub comment with 🚨 prefix  
3. **Critical Issues**: Tag @PM-Claude in GitHub comment
4. **System Issues**: Contact human stakeholder if AI systems are down

Remember: The Task Master system is designed to maximize AI team efficiency and coordination. Follow the protocols consistently for optimal team performance! 🎭✨