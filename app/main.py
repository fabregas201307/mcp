from mcp.server.fastmcp import FastMCP
from app.connectors.registry import get_registry
from app.skills.alpha_research import backtest_alpha as backtest_alpha_skill
from app.skills.alpha_research import review_alpha_code_prompt as review_alpha_code_skill
from app.skills.data_discovery import list_datasets as list_datasets_skill
from app.skills.data_discovery import get_dataset_schema as get_dataset_schema_skill
from app.skills.data_discovery import generate_sql_query_prompt as generate_sql_query_skill

# Initialize FastMCP server
mcp = FastMCP("mcp-server")

@mcp.tool()
def list_git_repos():
    """List available git repositories."""
    registry = get_registry()
    return registry.execute("git", {"action": "list"})

@mcp.tool()
def search_code(keyword: str):
    """Search for a keyword in python files within the repositories and return the file content."""
    registry = get_registry()
    return registry.execute("git", {"action": "search", "keyword": keyword})

@mcp.tool()
def query_database(query: str = "SELECT 1"):
    """Execute a database query."""
    registry = get_registry()
    return registry.execute("database", {"query": query})

@mcp.tool()
def backtest_alpha(alpha_name: str, start_date: str = "2023-01-01"):
    """
    Run a backtest for a specific alpha strategy on internal data.
    Returns performance metrics (Sharpe, Drawdown) without exposing raw data.
    """
    return backtest_alpha_skill(alpha_name, start_date)

@mcp.tool()
def list_datasets():
    """
    List all available datasets in the internal data warehouse (Snowflake, Redshift, Haver, etc.).
    Use this to discover what data is available for analysis.
    """
    return list_datasets_skill()

@mcp.tool()
def get_dataset_schema(dataset_name: str):
    """
    Get the schema definition (tables and columns) for a specific dataset.
    """
    return get_dataset_schema_skill(dataset_name)

@mcp.prompt()
def review_alpha_code(code_snippet: str):
    """
    A Skill that sets up the LLM to review alpha code according to internal quantitative standards.
    """
    return review_alpha_code_skill(code_snippet)

@mcp.prompt()
def generate_sql_query(dataset_name: str, question: str):
    """
    A Skill that provides the schema context for a dataset and asks the LLM to generate a SQL query.
    """
    return generate_sql_query_skill(dataset_name, question)

# Expose the underlying Starlette/FastAPI app for uvicorn
app = mcp.sse_app

if __name__ == "__main__":
    # This allows running the server in stdio mode (for local clients like Copilot)
    mcp.run()
