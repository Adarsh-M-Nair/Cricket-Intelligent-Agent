# tools/player_tools.py

from backend.utils.player_resolver import resolve_player_name
from backend.utils.stats import get_total_runs


def player_runs_tool(player_name: str):

    db_name = resolve_player_name(player_name)

    return get_total_runs(db_name)


def player_strike_rate_tool(player_name: str):

    db_name = resolve_player_name(player_name)

    from backend.utils.stats import get_strike_rate

    return get_strike_rate(db_name)