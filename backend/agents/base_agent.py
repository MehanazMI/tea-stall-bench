"""
Base Agent Class for Tea Stall Bench

This module provides the foundational BaseAgent class that all AI agents
in the Tea Stall Bench system inherit from. It provides common functionality
including logging, error handling, and a standard interface for agent execution.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class BaseAgent(ABC):
    """
    Base class for all AI agents in the Tea Stall Bench system.
    
    This abstract class provides core functionality that all agents need:
    - Logging capabilities
    - Error handling
    - Standard execution interface
    - Performance tracking
    
    All agent classes should inherit from this base class and implement
    the _execute_internal method with their specific logic.
    
    Attributes:
        name (str): The name of the agent
        llm_client: The LLM client instance for generating content
        logger (logging.Logger): Logger instance for this agent
    
    Example:
        >>> class WriterAgent(BaseAgent):
        ...     async def _execute_internal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        ...         # Implement writer logic here
        ...         pass
    """
    
    def __init__(self, name: str, llm_client: Optional[Any] = None):
        """
        Initialize the base agent.
        
        Args:
            name (str): The name of this agent (e.g., "Writer", "Research")
            llm_client (Optional[Any]): LLM client instance for content generation.
                                       Can be None for agents that don't need LLM.
        
        Example:
            >>> agent = WriterAgent("Writer", llm_client)
        """
        self.name = name
        self.llm_client = llm_client
        self.logger = logging.getLogger(f"TeaStallBench.Agent.{name}")
        
        # Configure logger if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's task with error handling and logging.
        
        This method wraps the agent's specific logic (_execute_internal) with
        standardized logging, error handling, and performance tracking.
        
        Args:
            input_data (Dict[str, Any]): Input data for the agent to process.
                                        Structure depends on the specific agent.
        
        Returns:
            Dict[str, Any]: Result of the agent's execution. Always includes:
                - 'status': 'success' or 'error'
                - 'agent': name of the agent
                - 'timestamp': when execution completed
                - Plus agent-specific output fields
        
        Raises:
            Exception: Re-raises any exception after logging, allowing
                      orchestrator to handle failures appropriately.
        
        Example:
            >>> result = await agent.execute({"topic": "Python tips"})
            >>> print(result['status'])
            'success'
        """
        start_time = datetime.now()
        
        try:
            self.logger.info(f"{self.name} agent starting execution")
            self.logger.debug(f"Input data: {input_data}")
            
            # Call the agent-specific implementation
            result = await self._execute_internal(input_data)
            
            # Add metadata to result
            result['status'] = 'success'
            result['agent'] = self.name
            result['timestamp'] = datetime.now().isoformat()
            result['execution_time'] = (datetime.now() - start_time).total_seconds()
            
            self.logger.info(f"{self.name} agent completed successfully in {result['execution_time']:.2f}s")
            self.logger.debug(f"Output: {result}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"{self.name} agent failed: {str(e)}", exc_info=True)
            
            # Return error result instead of just raising
            error_result = {
                'status': 'error',
                'agent': self.name,
                'error': str(e),
                'error_type': type(e).__name__,
                'timestamp': datetime.now().isoformat(),
                'execution_time': (datetime.now() - start_time).total_seconds()
            }
            
            # Re-raise the exception for orchestrator to handle
            raise
    
    @abstractmethod
    async def _execute_internal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Internal execution logic - must be implemented by subclasses.
        
        This method contains the agent-specific logic. Subclasses must
        implement this method with their unique functionality.
        
        Args:
            input_data (Dict[str, Any]): Input data for processing
        
        Returns:
            Dict[str, Any]: Agent-specific output. Should NOT include
                          status, agent, or timestamp fields as these
                          are added by the execute() wrapper.
        
        Raises:
            NotImplementedError: If subclass doesn't implement this method
        
        Example:
            >>> async def _execute_internal(self, input_data):
            ...     topic = input_data['topic']
            ...     content = await self.llm_client.generate(topic)
            ...     return {'content': content}
        """
        raise NotImplementedError("Subclasses must implement _execute_internal()")
    
    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"{self.__class__.__name__}(name='{self.name}')"
