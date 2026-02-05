"""
Unit tests for BaseAgent class

Tests the foundational functionality of the BaseAgent class including:
- Initialization
- Logging setup
- Error handling
- Execution flow
"""

import pytest
import logging
from unittest.mock import Mock, AsyncMock, patch
from backend.agents.base_agent import BaseAgent


# Test implementation of BaseAgent for testing purposes
class TestAgent(BaseAgent):
    """Concrete implementation of BaseAgent for testing."""
    
    async def _execute_internal(self, input_data):
        """Test implementation that simply returns the input."""
        return {'result': input_data.get('test_value', 'default')}


class FailingAgent(BaseAgent):
    """Agent that always fails - for testing error handling."""
    
    async def _execute_internal(self, input_data):
        """Raises an exception to test error handling."""
        raise ValueError("Test error from FailingAgent")


class TestBaseAgent:
    """Test suite for BaseAgent class."""
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly with name and LLM client."""
        mock_llm = Mock()
        agent = TestAgent("TestAgent", mock_llm)
        
        assert agent.name == "TestAgent"
        assert agent.llm_client == mock_llm
        assert agent.logger is not None
        assert isinstance(agent.logger, logging.Logger)
    
    def test_agent_initialization_without_llm(self):
        """Test that agent can be initialized without LLM client."""
        agent = TestAgent("TestAgent")
        
        assert agent.name == "TestAgent"
        assert agent.llm_client is None
        assert agent.logger is not None
    
    def test_logger_name_format(self):
        """Test that logger has correct naming convention."""
        agent = TestAgent("MyAgent")
        
        assert "TeaStallBench.Agent.MyAgent" in agent.logger.name
    
    @pytest.mark.asyncio
    async def test_successful_execution(self):
        """Test that successful agent execution returns correct structure."""
        agent = TestAgent("TestAgent")
        input_data = {'test_value': 'hello'}
        
        result = await agent.execute(input_data)
        
        # Check result structure
        assert result['status'] == 'success'
        assert result['agent'] == 'TestAgent'
        assert 'timestamp' in result
        assert 'execution_time' in result
        assert result['result'] == 'hello'
    
    @pytest.mark.asyncio
    async def test_execution_with_default_value(self):
        """Test agent execution with missing input data uses defaults."""
        agent = TestAgent("TestAgent")
        result = await agent.execute({})
        
        assert result['status'] == 'success'
        assert result['result'] == 'default'
    
    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test that agent properly handles and logs errors."""
        agent = FailingAgent("FailAgent")
        
        with pytest.raises(ValueError, match="Test error from FailingAgent"):
            await agent.execute({'test': 'data'})
    
    @pytest.mark.asyncio
    async def test_execution_time_tracking(self):
        """Test that execution time is tracked and reasonable."""
        agent = TestAgent("TestAgent")
        result = await agent.execute({'test_value': 'timing'})
        
        assert 'execution_time' in result
        assert isinstance(result['execution_time'], float)
        assert result['execution_time'] >= 0
        assert result['execution_time'] < 1  # Should be very fast for test
    
    @pytest.mark.asyncio
    async def test_timestamp_format(self):
        """Test that timestamp is in ISO format."""
        agent = TestAgent("TestAgent")
        result = await agent.execute({})
        
        assert 'timestamp' in result
        # Check it's a valid ISO format string
        assert 'T' in result['timestamp']
        assert len(result['timestamp']) > 10
    
    def test_abstract_method_enforcement(self):
        """Test that BaseAgent cannot be instantiated directly."""
        with pytest.raises(TypeError):
            # This should fail because _execute_internal is abstract
            BaseAgent("DirectAgent", None)
    
    def test_agent_repr(self):
        """Test string representation of agent."""
        agent = TestAgent("MyTestAgent")
        repr_str = repr(agent)
        
        assert "TestAgent" in repr_str
        assert "MyTestAgent" in repr_str
    
    @pytest.mark.asyncio
    async def test_logging_output(self, caplog):
        """Test that agent logs execution correctly."""
        caplog.set_level(logging.INFO)
        agent = TestAgent("LogTest")
        
        await agent.execute({'test_value': 'log_test'})
        
        # Check that appropriate log messages were created
        assert any("LogTest agent starting execution" in record.message 
                  for record in caplog.records)
        assert any("LogTest agent completed successfully" in record.message 
                  for record in caplog.records)
    
    @pytest.mark.asyncio
    async def test_error_logging(self, caplog):
        """Test that errors are logged with appropriate level."""
        caplog.set_level(logging.ERROR)
        agent = FailingAgent("ErrorTest")
        
        try:
            await agent.execute({})
        except ValueError:
            pass
        
        # Check error was logged
        assert any("ErrorTest agent failed" in record.message 
                  for record in caplog.records)
        assert any(record.levelname == "ERROR" for record in caplog.records)


# Additional integration-style tests
class TestBaseAgentIntegration:
    """Integration tests for BaseAgent."""
    
    @pytest.mark.asyncio
    async def test_multiple_sequential_executions(self):
        """Test that agent can execute multiple times successfully."""
        agent = TestAgent("MultiExec")
        
        result1 = await agent.execute({'test_value': 'first'})
        result2 = await agent.execute({'test_value': 'second'})
        result3 = await agent.execute({'test_value': 'third'})
        
        assert result1['result'] == 'first'
        assert result2['result'] == 'second'
        assert result3['result'] == 'third'
        
        # Each should have its own timestamp
        assert result1['timestamp'] != result2['timestamp']
