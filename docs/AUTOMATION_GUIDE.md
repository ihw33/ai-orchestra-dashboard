# 🤖 Process Automation Guide

## 📋 Overview
This guide covers the AI Orchestra Dashboard's automation systems including the Allow Request System, iTerm session management, smart prompt delivery, and GitHub workflow automation.

## 🚦 Allow Request System

### Risk Classification System

| Risk Level | Criteria | Auto-Approval | Manual Review |
|------------|----------|---------------|---------------|
| **LOW** | File reads, status checks, safe commands | ✅ Automatic | ❌ Not needed |
| **MEDIUM** | File edits, non-destructive operations | ⚠️ Conditional | ✅ Required |
| **HIGH** | Deletions, system changes, external APIs | ❌ Blocked | ✅ Always required |

### Implementation

```python
class AllowRequestSystem:
    def __init__(self):
        self.risk_analyzer = RiskAnalyzer()
        self.approval_queue = []
    
    async def process_request(self, request: AutomationRequest) -> RequestDecision:
        risk_level = self.risk_analyzer.assess_risk(request)
        
        if risk_level == RiskLevel.LOW:
            return RequestDecision.ALLOW
        elif risk_level == RiskLevel.MEDIUM:
            return await self.conditional_approval(request)
        else:
            return await self.manual_review_required(request)
    
    def assess_command_risk(self, command: str) -> RiskLevel:
        high_risk_patterns = [
            r'rm\s+-rf',
            r'sudo\s+',
            r'git\s+push\s+--force',
            r'npm\s+publish'
        ]
        
        medium_risk_patterns = [
            r'git\s+commit',
            r'npm\s+install',
            r'pip\s+install',
            r'docker\s+build'
        ]
        
        if any(re.search(pattern, command) for pattern in high_risk_patterns):
            return RiskLevel.HIGH
        elif any(re.search(pattern, command) for pattern in medium_risk_patterns):
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
```

## 🖥️ iTerm Session Management

### Session Identification & Control

```applescript
-- Get all active sessions
on getAllSessions()
    tell application "iTerm2"
        set sessionList to {}
        repeat with currentTab in tabs of current window
            repeat with currentSession in sessions of currentTab
                set sessionInfo to {id:id of currentSession, name:name of currentSession, tabIndex:(index of currentTab)}
                set end of sessionList to sessionInfo
            end repeat
        end repeat
        return sessionList
    end tell
end getAllSessions

-- Smart session targeting
on findSessionByName(targetName)
    set sessions to getAllSessions()
    repeat with sessionInfo in sessions
        if name of sessionInfo contains targetName then
            return sessionInfo
        end if
    end repeat
    return null
end findSessionByName

-- Send command with verification
on sendCommandWithVerification(sessionId, command)
    tell application "iTerm2"
        tell session id sessionId
            write text command
            delay 2
            set output to text
            return output
        end tell
    end tell
end sendCommandWithVerification
```

### Session Health Monitoring

```python
class SessionHealthMonitor:
    def __init__(self):
        self.sessions = {}
        self.health_check_interval = 30  # seconds
    
    async def monitor_sessions(self):
        """Continuously monitor session health"""
        while True:
            for session_id, session_info in self.sessions.items():
                health_status = await self.check_session_health(session_id)
                
                if health_status.status == 'unhealthy':
                    await self.handle_unhealthy_session(session_id, health_status)
                
            await asyncio.sleep(self.health_check_interval)
    
    async def check_session_health(self, session_id: str) -> HealthStatus:
        """Check if session is responsive"""
        try:
            # Send ping command and wait for response
            response = await self.send_ping_command(session_id)
            
            if response.success and response.response_time < 5:
                return HealthStatus(status='healthy', response_time=response.response_time)
            else:
                return HealthStatus(status='slow', response_time=response.response_time)
                
        except TimeoutError:
            return HealthStatus(status='unresponsive', error='Timeout')
        except Exception as e:
            return HealthStatus(status='error', error=str(e))
```

## 📨 Smart Prompt Sender

### Intelligent Message Delivery

```python
class SmartPromptSender:
    def __init__(self):
        self.delivery_strategies = {
            'gemini': GeminiDeliveryStrategy(),
            'codex': CodexDeliveryStrategy(),
            'vscode-claude': VSCodeDeliveryStrategy(),
            'cursor-chatgpt': CursorDeliveryStrategy()
        }
        self.verification_timeout = 30
    
    async def send_with_verification(self, member: str, message: str) -> DeliveryResult:
        """Send message and verify delivery"""
        strategy = self.delivery_strategies[member]
        
        # Pre-delivery validation
        if not await strategy.validate_target():
            return DeliveryResult(success=False, error="Target not available")
        
        # Send message
        delivery_id = await strategy.send_message(message)
        
        # Wait for verification
        verification = await self.wait_for_verification(member, delivery_id)
        
        return DeliveryResult(
            success=verification.acknowledged,
            delivery_time=verification.delivery_time,
            acknowledgment_time=verification.acknowledgment_time
        )
    
    async def wait_for_verification(self, member: str, delivery_id: str) -> VerificationResult:
        """Wait for message acknowledgment"""
        start_time = time.time()
        
        while time.time() - start_time < self.verification_timeout:
            # Check GitHub for acknowledgment comment
            ack = await self.check_github_acknowledgment(member, delivery_id)
            if ack:
                return VerificationResult(
                    acknowledged=True,
                    delivery_time=ack.timestamp - start_time,
                    acknowledgment_time=time.time() - start_time
                )
            
            await asyncio.sleep(2)
        
        return VerificationResult(acknowledged=False, timeout=True)
```

### Delivery Strategy Implementations

```python
class GeminiDeliveryStrategy:
    async def validate_target(self) -> bool:
        """Check if Gemini session is available and in correct mode"""
        session_output = await self.get_session_output()
        
        # Check for AI mode (>) vs Shell mode ($)
        if session_output.prompt_indicator == '$':
            await self.switch_to_ai_mode()
        
        return session_output.responsive
    
    async def send_message(self, message: str) -> str:
        """Send message to Gemini session"""
        applescript = f'''
        tell application "iTerm2"
            tell session 2 of tab 4 of current window
                write text "{message}"
                delay 1
                write text ""
            end tell
        end tell
        '''
        
        delivery_id = str(uuid.uuid4())
        await self.execute_applescript(applescript)
        return delivery_id
    
    async def switch_to_ai_mode(self):
        """Switch Gemini from Shell to AI mode"""
        await self.send_command("!")
        await asyncio.sleep(1)

class VSCodeDeliveryStrategy:
    async def validate_target(self) -> bool:
        """Check if VSCode Claude is available"""
        return await self.check_vscode_process() and await self.check_claude_extension()
    
    async def send_message(self, message: str) -> str:
        """Send message via VSCode Claude extension"""
        applescript = f'''
        tell application "Visual Studio Code"
            activate
            delay 1
        end tell
        
        tell application "System Events"
            keystroke "@" using {{command down, shift down}}
            delay 2
            type "{message}"
            keystroke return
        end tell
        '''
        
        delivery_id = str(uuid.uuid4())
        await self.execute_applescript(applescript)
        return delivery_id
```

## 🔄 Task Master MCP Integration

### MCP Server Configuration

```json
{
  "mcpServers": {
    "ai-orchestra": {
      "command": "node",
      "args": ["/Users/m4_macbook/Projects/ai-orchestra-dashboard/claude-task-master/mcp-server/server.js"],
      "env": {
        "PROJECT_ROOT": "/Users/m4_macbook/Projects/ai-orchestra-dashboard",
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "LOG_LEVEL": "info"
      }
    }
  }
}
```

### Task Management Automation

```javascript
// claude-task-master integration
class TaskMasterIntegration {
    constructor() {
        this.taskMaster = new TaskMaster({
            projectRoot: process.env.PROJECT_ROOT,
            githubToken: process.env.GITHUB_TOKEN
        });
    }
    
    async automateTaskDistribution() {
        // Get pending tasks from Task Master
        const pendingTasks = await this.taskMaster.getPendingTasks();
        
        for (const task of pendingTasks) {
            // Analyze task requirements
            const analysis = await this.analyzeTaskRequirements(task);
            
            // Select optimal team member
            const assignee = await this.selectOptimalMember(analysis);
            
            // Create GitHub issue and assign
            const issue = await this.createGitHubIssue(task, assignee);
            
            // Notify team member
            await this.notifyTeamMember(assignee, issue);
            
            // Update Task Master
            await this.taskMaster.updateTaskStatus(task.id, 'assigned');
        }
    }
    
    async analyzeTaskRequirements(task) {
        return {
            complexity: this.calculateComplexity(task),
            skillsRequired: this.extractSkills(task.description),
            estimatedHours: this.estimateHours(task),
            dependencies: this.findDependencies(task)
        };
    }
}
```

## 🔧 GitHub Automation Workflows

### Automated Issue Management

```yaml
# .github/workflows/issue-automation.yml
name: AI Orchestra Issue Automation

on:
  issues:
    types: [opened, edited, closed]
  issue_comment:
    types: [created]

jobs:
  process-issue:
    runs-on: ubuntu-latest
    steps:
      - name: Analyze Issue
        uses: ./.github/actions/analyze-issue
        with:
          issue-number: ${{ github.event.issue.number }}
          
      - name: Auto-assign Team Member
        if: github.event.action == 'opened'
        run: |
          python scripts/auto-assign.py \
            --issue ${{ github.event.issue.number }} \
            --repository ${{ github.repository }}
            
      - name: Update Progress Metrics
        if: github.event.action == 'comment'
        run: |
          python scripts/update-metrics.py \
            --comment-body "${{ github.event.comment.body }}" \
            --issue ${{ github.event.issue.number }}
```

### Progress Tracking Automation

```python
class ProgressTracker:
    def __init__(self):
        self.github_client = GitHubClient()
        self.metrics_collector = MetricsCollector()
    
    async def process_comment(self, comment_data: dict):
        """Process GitHub comment for progress updates"""
        comment_body = comment_data['body']
        issue_number = comment_data['issue']['number']
        
        # Extract progress information
        progress_match = re.search(r'\[(\w+)\].*?(\d+)%', comment_body)
        if progress_match:
            member = progress_match.group(1)
            progress = int(progress_match.group(2))
            
            # Update database
            await self.update_task_progress(issue_number, member, progress)
            
            # Broadcast real-time update
            await self.broadcast_progress_update(issue_number, member, progress)
            
            # Check for completion
            if progress >= 100:
                await self.handle_task_completion(issue_number, member)
    
    async def auto_detect_completion(self, issue_number: int):
        """Automatically detect task completion from file changes"""
        # Check recent commits related to issue
        commits = await self.github_client.get_issue_commits(issue_number)
        
        if commits:
            latest_commit = commits[0]
            
            # Analyze commit for completion indicators
            completion_indicators = [
                'fix:', 'feat:', 'complete:', 'done:', 'implement:'
            ]
            
            if any(indicator in latest_commit.message.lower() 
                   for indicator in completion_indicators):
                await self.suggest_task_completion(issue_number)
```

## 📊 Automated Monitoring & Alerting

### System Health Monitoring

```python
class AutomatedMonitoring:
    def __init__(self):
        self.alert_thresholds = {
            'response_time': 30,  # seconds
            'error_rate': 0.05,   # 5%
            'memory_usage': 0.85, # 85%
            'disk_usage': 0.90    # 90%
        }
        self.notification_channels = [
            GitHubIssueNotifier(),
            SlackNotifier(),
            EmailNotifier()
        ]
    
    async def monitor_system_health(self):
        """Continuous system health monitoring"""
        while True:
            health_report = await self.collect_health_metrics()
            
            # Check each metric against thresholds
            for metric, value in health_report.items():
                if self.exceeds_threshold(metric, value):
                    await self.trigger_alert(metric, value)
            
            # Generate automated health report
            if self.should_generate_report():
                await self.generate_health_report(health_report)
            
            await asyncio.sleep(60)  # Check every minute
    
    async def trigger_alert(self, metric: str, value: float):
        """Trigger alerts through configured channels"""
        alert = Alert(
            severity=self.calculate_severity(metric, value),
            metric=metric,
            current_value=value,
            threshold=self.alert_thresholds[metric],
            timestamp=datetime.utcnow()
        )
        
        for notifier in self.notification_channels:
            await notifier.send_alert(alert)
```

### Automated Recovery Procedures

```python
class AutoRecovery:
    def __init__(self):
        self.recovery_procedures = {
            'session_unresponsive': self.restart_session,
            'high_memory_usage': self.cleanup_memory,
            'api_rate_limit': self.implement_backoff,
            'database_connection': self.reconnect_database
        }
    
    async def handle_system_issue(self, issue_type: str, context: dict):
        """Automatically attempt to recover from system issues"""
        if issue_type in self.recovery_procedures:
            recovery_func = self.recovery_procedures[issue_type]
            
            try:
                result = await recovery_func(context)
                if result.success:
                    await self.log_successful_recovery(issue_type, result)
                else:
                    await self.escalate_to_human(issue_type, context)
            except Exception as e:
                await self.escalate_to_human(issue_type, context, error=e)
    
    async def restart_session(self, context: dict) -> RecoveryResult:
        """Restart unresponsive iTerm session"""
        session_id = context['session_id']
        member = context['member']
        
        # Kill existing session
        await self.kill_session(session_id)
        
        # Create new session
        new_session = await self.create_new_session(member)
        
        # Update session mapping
        await self.update_session_mapping(member, new_session.id)
        
        return RecoveryResult(success=True, new_session_id=new_session.id)
```

## 🔐 Security Automation

### Automated Security Scanning

```python
class SecurityAutomation:
    def __init__(self):
        self.security_scanners = [
            DependencyScanner(),
            CodeQualityScanner(),
            SecretsScanner(),
            VulnerabilityScanner()
        ]
    
    async def run_security_checks(self, trigger: str = 'scheduled'):
        """Run comprehensive security checks"""
        results = {}
        
        for scanner in self.security_scanners:
            try:
                scan_result = await scanner.scan()
                results[scanner.name] = scan_result
                
                # Handle critical vulnerabilities immediately
                if scan_result.has_critical_issues():
                    await self.handle_critical_security_issue(scan_result)
                    
            except Exception as e:
                await self.log_scanner_error(scanner.name, e)
        
        # Generate security report
        await self.generate_security_report(results, trigger)
        
        return results
    
    async def handle_critical_security_issue(self, scan_result: ScanResult):
        """Immediate response to critical security issues"""
        # Create urgent GitHub issue
        issue = await self.create_security_issue(scan_result)
        
        # Notify all team members
        await self.broadcast_security_alert(scan_result)
        
        # Automatically apply fixes if available
        if scan_result.has_auto_fixes():
            await self.apply_security_fixes(scan_result)
```

## 🚀 Quick Setup Commands

### Environment Setup
```bash
# Initialize automation environment
cd /Users/m4_macbook/Projects/ai-orchestra-dashboard
./scripts/setup_automation.sh

# Configure allow request system
python scripts/configure_allow_system.py --risk-threshold medium

# Start iTerm session monitoring
./scripts/start_session_monitoring.sh

# Setup Task Master MCP integration
./claude-task-master/scripts/setup-mcp.sh
```

### Testing Automation
```bash
# Test prompt delivery
python scripts/test_prompt_delivery.py --member gemini --message "Test message"

# Test automation workflows
python scripts/test_automation.py --workflow task-assignment

# Verify security automation
python scripts/test_security.py --scan-type full
```

---

**📅 Last Updated**: August 21, 2025  
**🤖 Automation Version**: 2.1  
**🔄 Next Update**: After Round 2 completion  
**🛠️ Maintained by**: Documentation AI (Task Master)  
**✅ Tested by**: PM Claude & Team