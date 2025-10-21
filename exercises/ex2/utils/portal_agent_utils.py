import base64
import os
from typing import Dict, Optional

from dotenv import load_dotenv
from gen_ai_hub.proxy.langchain import init_llm
from IPython.display import Markdown, display
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent


def build_user_message(content: str) -> dict:
    """
    Helper to build a user message dict for agent calls.
    Args:
        content: The user message string
    Returns:
        Dict in the format {"role": "user", "content": ...}
    """
    return {"role": "user", "content": content}


"""
Portal Agent Utilities

This module provides utilities for creating and configuring an Employee Portal Agent
that connects to SAP LeanIX via Model Context Protocol (MCP).
"""


def load_environment_variables() -> Dict[str, str]:
    """
    Load and validate required environment variables.

    Returns:
        Dict containing the required environment variables

    Raises:
        ValueError: If required environment variables are missing
    """
    load_dotenv()

    required_vars = [
        "AICORE_CLIENT_ID",
        "AICORE_CLIENT_SECRET",
        "AICORE_RESOURCE_GROUP",
        "AICORE_BASE_URL",
        "AICORE_AUTH_URL",
        "LEANIX_API_TOKEN",
    ]

    env_vars = {}
    missing_vars = []

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing_vars.append(var)
        else:
            env_vars[var] = value

    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

    return env_vars


def get_default_system_prompt() -> str:
    """
    Get the default system prompt for the Employee Portal Agent.

    Returns:
        The system prompt string
    """
    return """You are an AI assistant for the company's Enterprise Architecture portal, designed to help employees find information about applications, services, and IT components.

Your role:
- Help employees discover applications and tools they need for their work
- Provide information about application ownership, lifecycle status, and go-live dates
- Assist with finding alternatives when applications are obsolete or unavailable
- Always include direct links to fact sheets when providing information
- Focus on practical, actionable information that helps employees make decisions

Always use the available LeanIX tools to search for and retrieve current information. When providing application details, include:
- Lifecycle phase and status
- Go-live dates or planned dates
- Owner/responsible team contact
- Direct link to the fact sheet for more details

Be concise and practical in your responses.
"""


async def create_mcp_client(
    leanix_api_token: str,
    leanix_url: str = "https://demo-eu-2.leanix.net/services/mcp-server/v1/mcp",
) -> MultiServerMCPClient:
    """
    Create and configure an MCP client for LeanIX integration.

    Args:
        leanix_api_token: The LeanIX API token
        leanix_url: The LeanIX MCP server URL (optional)

    Returns:
        Configured MultiServerMCPClient instance
    """
    # Prepare the LeanIX MCP access token
    lx_api_token_base64 = base64.b64encode(
        f"apitoken:{leanix_api_token}".encode()
    ).decode()

    # Initialize MCP client with LeanIX configuration
    mcp_client = MultiServerMCPClient(
        {
            "LeanIX MCP Remote": {
                "transport": "streamable_http",
                "url": leanix_url,
                "headers": {"Authorization": f"Basic {lx_api_token_base64}"},
            }
        }
    )

    return mcp_client


async def create_portal_agent(
    model_name: str = "gpt-4.1",
    max_tokens: int = 32767,
    system_prompt: Optional[str] = None,
    leanix_url: str = "https://demo-eu-2.leanix.net/services/mcp-server/v1/mcp",
):
    """
    Create a complete Employee Portal Agent with LeanIX integration.

    Args:
        model_name: The AI model to use (default: "gpt-4.1")
        max_tokens: Maximum tokens for the model (default: 32767)
        system_prompt: Custom system prompt (optional, uses default if not provided)
        leanix_url: LeanIX MCP server URL (optional)

    Returns:
        Configured ReAct agent ready for use

    Raises:
        ValueError: If environment variables are missing
        Exception: If agent creation fails
    """
    try:
        # Load and validate environment variables
        env_vars = load_environment_variables()

        # Initialize the LLM
        llm = init_llm(model_name, max_tokens=max_tokens)
        print(f"✅ Created LLM: {llm.get_name()}")

        # Create MCP client
        mcp_client = await create_mcp_client(
            leanix_api_token=env_vars["LEANIX_API_TOKEN"], leanix_url=leanix_url
        )
        print(
            f"✅ Initialized MCP client with connections: {', '.join(mcp_client.connections.keys())}"
        )

        # Get available tools
        tools = await mcp_client.get_tools()
        print(f"✅ Loaded {len(tools)} tools from MCP server")

        # Use provided system prompt or default
        prompt = system_prompt or get_default_system_prompt()

        # Create the ReAct agent
        agent = create_react_agent(model=llm, tools=tools, prompt=prompt)
        print("✅ Employee Portal Agent created successfully!")

        return agent

    except Exception as e:
        print(f"❌ Failed to create portal agent: {str(e)}")
        raise


async def call_agent(agent, query):
    response = await agent.ainvoke({"messages": [{"role": "user", "content": query}]})
    return response


def print_agent_response(response):
    msgs = response.get("messages", [])
    for msg in reversed(msgs):
        content = getattr(msg, "content", "")
        if content:
            display(Markdown(content))
            break
    else:
        print("No printable content in agent response.")
