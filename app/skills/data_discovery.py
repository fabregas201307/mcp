from app.connectors.registry import get_registry

def list_datasets():
    """
    List all available datasets in the internal data warehouse.
    """
    registry = get_registry()
    result = registry.execute("warehouse", {"action": "list_datasets"})
    return result

def get_dataset_schema(dataset_name: str):
    """
    Get the schema (tables and columns) for a specific dataset.
    """
    registry = get_registry()
    result = registry.execute("warehouse", {"action": "get_schema", "dataset": dataset_name})
    return result

def generate_sql_query_prompt(dataset_name: str, natural_language_query: str):
    """
    Generates a prompt for the LLM to write a SQL query based on the dataset schema.
    """
    registry = get_registry()
    result = registry.execute("warehouse", {"action": "get_schema", "dataset": dataset_name})
    
    if result.get("is_error"):
        return f"Error: {result.get('error')}"
    
    schema_info = result.get("schema", {})
    tables = schema_info.get("tables", {})
    
    schema_str = ""
    for table, columns in tables.items():
        schema_str += f"- Table: {table}\n  Columns: {', '.join(columns)}\n"
    
    prompt = f"""[Role: system]
You are an expert SQL Data Analyst. 
Your task is to generate a SQL query for the '{dataset_name}' dataset ({schema_info.get('type')}).

Schema Information:
{schema_str}

[Role: user]
Question: {natural_language_query}

[Role: assistant]
Here is the SQL query to answer your question:
```sql
"""
    return prompt
