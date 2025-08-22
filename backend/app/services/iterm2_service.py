"""
iTerm2 Integration Service for AI Orchestra Dashboard
Provides programmatic control of iTerm2 terminal sessions for AI agent orchestration
"""

import asyncio
import iterm2
from typing import Dict, Optional, List, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class iTerm2Service:
    """
    Service class for managing iTerm2 terminal sessions
    Enables creation, control, and monitoring of AI agent terminal sessions
    """
    
    def __init__(self):
        self.connection: Optional[iterm2.Connection] = None
        self.app: Optional[iterm2.App] = None
        self.sessions: Dict[str, iterm2.Session] = {}
        self.agent_tabs: Dict[str, iterm2.Tab] = {}
        self.is_connected = False
        
    async def connect(self) -> bool:
        """
        Establish connection to iTerm2
        
        Returns:
            bool: True if connection successful
        """
        try:
            self.connection = await iterm2.Connection.async_create()
            self.app = await iterm2.async_get_app(self.connection)
            self.is_connected = True
            logger.info("Successfully connected to iTerm2")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to iTerm2: {e}")
            self.is_connected = False
            return False
    
    async def create_agent_session(
        self, 
        agent_name: str, 
        profile: str = "Default",
        command: Optional[str] = None
    ) -> Optional[iterm2.Session]:
        """
        Create a new terminal session for an AI agent
        
        Args:
            agent_name: Name of the AI agent (e.g., "claude", "gpt")
            profile: iTerm2 profile to use
            command: Initial command to run in session
            
        Returns:
            Session object if successful, None otherwise
        """
        if not self.is_connected:
            logger.error("Not connected to iTerm2")
            return None
            
        try:
            # Get current window or create new one
            window = self.app.current_terminal_window
            if not window:
                window = await self.app.create_window(profile=profile)
            
            # Create new tab for agent
            tab = await window.async_create_tab(profile=profile)
            session = tab.current_session
            
            # Store references
            self.sessions[agent_name] = session
            self.agent_tabs[agent_name] = tab
            
            # Set session title and badge
            await session.async_set_name(f"AI Agent: {agent_name}")
            await tab.async_set_title(f"{agent_name.upper()} Session")
            
            # Set badge with agent name
            await session.async_set_profile_property("Badge Text", agent_name.upper())
            
            # Run initial command if provided
            if command:
                await session.async_send_text(command + "\n")
            else:
                # Default initialization
                await session.async_send_text(f"# {agent_name} AI Agent Session\n")
                await session.async_send_text(f"# Initialized at {datetime.now()}\n")
            
            logger.info(f"Created session for agent: {agent_name}")
            return session
            
        except Exception as e:
            logger.error(f"Failed to create session for {agent_name}: {e}")
            return None
    
    async def send_command(
        self, 
        agent_name: str, 
        command: str,
        wait_for_prompt: bool = False
    ) -> bool:
        """
        Send a command to a specific agent's session
        
        Args:
            agent_name: Name of the target agent
            command: Command to send
            wait_for_prompt: Whether to wait for command prompt
            
        Returns:
            bool: True if command sent successfully
        """
        if agent_name not in self.sessions:
            logger.error(f"No session found for agent: {agent_name}")
            return False
            
        try:
            session = self.sessions[agent_name]
            await session.async_send_text(command + "\n")
            
            if wait_for_prompt:
                # Wait for command to complete (simplified)
                await asyncio.sleep(0.5)
            
            logger.debug(f"Sent command to {agent_name}: {command[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send command to {agent_name}: {e}")
            return False
    
    async def get_session_output(
        self, 
        agent_name: str, 
        lines: int = 50
    ) -> Optional[str]:
        """
        Get recent output from an agent's session
        
        Args:
            agent_name: Name of the agent
            lines: Number of lines to retrieve
            
        Returns:
            String containing recent output
        """
        if agent_name not in self.sessions:
            logger.error(f"No session found for agent: {agent_name}")
            return None
            
        try:
            session = self.sessions[agent_name]
            
            # Get screen contents
            contents = await session.async_get_screen_contents()
            
            # Extract text from last N lines
            output_lines = []
            for i in range(max(0, contents.number_of_lines - lines), contents.number_of_lines):
                line = contents.line(i)
                output_lines.append(line.string)
            
            return "\n".join(output_lines)
            
        except Exception as e:
            logger.error(f"Failed to get output from {agent_name}: {e}")
            return None
    
    async def monitor_session(
        self, 
        agent_name: str,
        callback: Any
    ):
        """
        Monitor a session for changes and invoke callback
        
        Args:
            agent_name: Name of the agent to monitor
            callback: Async function to call with new content
        """
        if agent_name not in self.sessions:
            logger.error(f"No session found for agent: {agent_name}")
            return
            
        session = self.sessions[agent_name]
        
        try:
            async with session.get_screen_streamer() as streamer:
                while True:
                    content = await streamer.async_get()
                    await callback(agent_name, content)
                    
        except Exception as e:
            logger.error(f"Error monitoring session {agent_name}: {e}")
    
    async def broadcast_command(self, command: str) -> Dict[str, bool]:
        """
        Send command to all active agent sessions
        
        Args:
            command: Command to broadcast
            
        Returns:
            Dict mapping agent names to success status
        """
        results = {}
        for agent_name in self.sessions:
            results[agent_name] = await self.send_command(agent_name, command)
        return results
    
    async def get_all_sessions_status(self) -> Dict[str, Dict]:
        """
        Get status information for all active sessions
        
        Returns:
            Dict containing status for each agent
        """
        status = {}
        for agent_name, session in self.sessions.items():
            try:
                status[agent_name] = {
                    "active": True,
                    "session_id": session.session_id,
                    "name": await session.async_get_variable("session.name"),
                }
            except:
                status[agent_name] = {"active": False}
        
        return status
    
    async def close_session(self, agent_name: str) -> bool:
        """
        Close a specific agent's session
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            bool: True if session closed successfully
        """
        if agent_name not in self.sessions:
            logger.error(f"No session found for agent: {agent_name}")
            return False
            
        try:
            session = self.sessions[agent_name]
            await session.async_close()
            
            # Clean up references
            del self.sessions[agent_name]
            if agent_name in self.agent_tabs:
                del self.agent_tabs[agent_name]
            
            logger.info(f"Closed session for agent: {agent_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to close session for {agent_name}: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from iTerm2"""
        if self.connection:
            # Close all sessions
            for agent_name in list(self.sessions.keys()):
                await self.close_session(agent_name)
            
            # Note: iterm2.Connection doesn't have a close method
            self.connection = None
            self.app = None
            self.is_connected = False
            logger.info("Disconnected from iTerm2")


class AgentOrchestrator:
    """
    High-level orchestrator for managing multiple AI agents via iTerm2
    """
    
    def __init__(self, iterm_service: iTerm2Service):
        self.iterm = iterm_service
        self.agents_config = {
            "claude": {
                "command": "claude-cli",
                "profile": "Default",
            },
            "gpt": {
                "command": "chatgpt-cli",
                "profile": "Default",
            },
            "gemini": {
                "command": "gemini-cli",
                "profile": "Default",
            },
            "codex": {
                "command": "codex-cli",
                "profile": "Default",
            }
        }
        
    async def initialize_all_agents(self) -> Dict[str, bool]:
        """
        Initialize all configured AI agents
        
        Returns:
            Dict mapping agent names to initialization success
        """
        results = {}
        
        for agent_name, config in self.agents_config.items():
            session = await self.iterm.create_agent_session(
                agent_name=agent_name,
                profile=config["profile"],
                command=config.get("command")
            )
            results[agent_name] = session is not None
            
        return results
    
    async def distribute_task(
        self, 
        task: str, 
        agent_type: Optional[str] = None
    ) -> bool:
        """
        Distribute a task to appropriate agent(s)
        
        Args:
            task: Task description or command
            agent_type: Specific agent type, or None for auto-selection
            
        Returns:
            bool: True if task distributed successfully
        """
        if agent_type:
            # Send to specific agent
            return await self.iterm.send_command(agent_type, task)
        else:
            # Auto-select based on task content (simplified logic)
            if "code" in task.lower() or "implement" in task.lower():
                return await self.iterm.send_command("codex", task)
            elif "design" in task.lower() or "ui" in task.lower():
                return await self.iterm.send_command("gemini", task)
            else:
                # Default to Claude for general tasks
                return await self.iterm.send_command("claude", task)
    
    async def collect_responses(
        self, 
        timeout: int = 30
    ) -> Dict[str, str]:
        """
        Collect responses from all active agents
        
        Args:
            timeout: Maximum time to wait for responses
            
        Returns:
            Dict mapping agent names to their responses
        """
        responses = {}
        
        # Wait a bit for agents to process
        await asyncio.sleep(2)
        
        for agent_name in self.iterm.sessions:
            output = await self.iterm.get_session_output(agent_name, lines=30)
            if output:
                responses[agent_name] = output
        
        return responses


# Example usage function
async def main():
    """Example usage of iTerm2 integration"""
    service = iTerm2Service()
    
    # Connect to iTerm2
    if await service.connect():
        orchestrator = AgentOrchestrator(service)
        
        # Initialize agents
        results = await orchestrator.initialize_all_agents()
        print(f"Agent initialization: {results}")
        
        # Send a task
        await orchestrator.distribute_task("Create a Python hello world script")
        
        # Get responses
        await asyncio.sleep(5)
        responses = await orchestrator.collect_responses()
        for agent, response in responses.items():
            print(f"\n{agent} response:\n{response[-500:]}")  # Last 500 chars
        
        # Cleanup
        await service.disconnect()


if __name__ == "__main__":
    # Run example
    iterm2.run_until_complete(main)