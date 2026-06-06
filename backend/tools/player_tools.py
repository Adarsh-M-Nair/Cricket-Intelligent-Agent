from utils.stats import (
    get_total_runs,
    get_strike_rate
)

def player_runs_tool(player_name: str):
    return get_total_runs(player_name)

def player_strike_rate_tool(player_name: str):
    return get_strike_rate(player_name)