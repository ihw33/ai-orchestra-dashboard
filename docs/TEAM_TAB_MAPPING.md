# 🗂️ AI Orchestra Team Tab Mapping
> Last Updated: 2025-08-20
> Current Project: AI Orchestra Dashboard
> PM Location: Tab 1-1

## 📍 Tab Projects & Configuration

### Tab 1: ✳ PM Control Center (현재 여기)
**Project**: AI Orchestra Dashboard Management
| Session | Name | Tool | Role |
|---------|------|------|------|
| 1-1 | ✳ 탭 세션 | PM Claude | **Project Manager (현재 PM)** |
| 1-2 | Default | node | Available |
| 1-3 | Default | codex | Available |

### Tab 2: 🌟 Gemini - AI Engine  
**Project**: Data Processing & Analytics
| Session | Name | Tool | Role |
|---------|------|------|------|
| 2-1 | 🌟 Gemini - AI Engine | Gemini | Data Processing |
| 2-2 | codex | Codex | Backend |
| 2-3 | 🔧 Claude - Integration | Claude | Integration |

### Tab 3: 📱 Claude-Mobile
**Project**: Mobile & Frontend Development
| Session | Name | Tool | Role |
|---------|------|------|------|
| 3-1 | -zsh | Terminal | Available |
| 3-2 | node | Gemini (Node) | Data Processing |
| 3-3 | codex | Codex | Backend |
| 3-4 | 📱 Claude-Mobile | Claude | Mobile/Frontend |

### Tab 4: 🎼 AI Orchestra Board
**Project**: AI Orchestra Dashboard - Backend Development
| Session | Name | Tool | Role |
|---------|------|------|------|
| 4-1 | claude | Claude | **Backend (Issue #26 작업 중)** |
| 4-2 | -zsh | Terminal | Available |
| 4-3 | gemini | Gemini | Data Processing |
| 4-4 | codex | Codex | Backend Development |

## 🔍 Tab Identification Log

### Tab 2
- **Test sent**: 2025-08-20
- **Response**: Gemini responded (but might be wrong CLI)
- **Issue**: Received PR #35 review feedback meant for Codex

### Tab 3  
- **Test sent**: 2025-08-20
- **Response**: VSCode Claude responded
- **Issue**: Received "[Codex] PR #35 리뷰 피드백입니다"

### Tab 4
- **Confirmed**: Claude Code with iwl-code-reviewer agent
- **Function**: Code review only (read-only permissions)

## ❓ Missing Team Members

Looking for:
- **Codex CLI** (Backend development)
- **Gemini CLI** (Data processing)
- **Cursor ChatGPT** (Design system)

## 🎯 Action Items

1. [ ] Confirm Tab 2 identity
2. [ ] Confirm Tab 3 identity
3. [ ] Locate Codex CLI
4. [ ] Update this document when confirmed
5. [ ] Create AppleScript functions for each team member

## 📝 AppleScript Template

```applescript
-- Send to specific team member
on sendToTeamMember(tabNumber, memberName, message)
    tell application "iTerm"
        tell current window
            tell tab tabNumber
                select
                delay 0.5
                tell current session
                    write text "[To " & memberName & "] " & message
                    delay 0.5
                    write text ""
                end tell
            end tell
        end tell
    end tell
end sendToTeamMember
```

## 🚨 Important Notes

- Always verify tab number before sending critical instructions
- Use GitHub Issues as backup communication channel
- Update this document immediately when changes occur
- PM Claude (Tab 1) is the single source of truth

---

**Document Status**: 🟡 Incomplete - Awaiting team member responses