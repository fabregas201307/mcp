import json
from typing import Dict, Any

def backtest_alpha(alpha_name: str, start_date: str = "2023-01-01") -> str:
    """
    Run a backtest for a specific alpha strategy on internal data.
    Returns performance metrics (Sharpe, Drawdown) without exposing raw data.
    This is a 'Thick Tool' that saves tokens by processing data server-side.
    """
    # In a real implementation, this would load data and run the python code
    # For now, we simulate the "Skill" of backtesting
    
    # Mock result - in reality this comes from your internal engine
    result = {
        "alpha": alpha_name,
        "period": f"{start_date} to present",
        "metrics": {
            "sharpe_ratio": 1.45,
            "max_drawdown": -0.12,
            "annualized_return": 0.24,
            "win_rate": 0.54
        },
        "status": "success"
    }
    return json.dumps(result, indent=2)

def review_alpha_code_prompt(code_snippet: str) -> list:
    """
    A 'Skill' (Prompt) that sets up the LLM to review alpha code 
    according to internal quantitative standards.
    """
    return [
        {
            "role": "user",
            "content": {
                "type": "text",
                "text": f"""Please review the following alpha strategy code for production readiness.
                
                Focus on these internal standards:
                1. Vectorization: Ensure pandas/numpy are used efficiently (no loops).
                2. Safety: Check for look-ahead bias (using future data).
                3. Robustness: Ensure handling of NaN/Infinite values.
                
                Code to review:
                ```python
                {code_snippet}
                ```
                """
            }
        }
    ]
