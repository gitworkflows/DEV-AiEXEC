"""A simple chat flow example for Aiexec.

This script demonstrates how to set up a basic conversational flow using Aiexec's ChatInput and ChatOutput components.

Features:
- Configures logging to 'aiexec.log' at INFO level
- Connects ChatInput to ChatOutput
- Builds a Graph object for the flow

Usage:
    python simple_chat.py

You can use this script as a template for building more complex conversational flows in Aiexec.
"""

from pathlib import Path

from lfx.components.input_output import ChatInput, ChatOutput
from lfx.graph import Graph
from lfx.log.logger import LogConfig

log_config = LogConfig(
    log_level="INFO",
    log_file=Path("aiexec.log"),
)
chat_input = ChatInput()
chat_output = ChatOutput().set(input_value=chat_input.message_response)

graph = Graph(chat_input, chat_output, log_config=log_config)
