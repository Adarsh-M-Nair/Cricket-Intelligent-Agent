import json
import os
from pathlib import Path

class CricketMatchParser:
  def __init__(self, data_path):
    self.data_path = data_path

  def load_match_file(self, file_path):
    """
    Load a single JSON match file
    """
    with open(file_path, 'r',encoding='utf-8') as file:
      return json.load(file)
    
  def parse_match_info(self, match_data):
    """
    Extract match-level information
    """
    info = match_data.get("info",{})
    teams = info.get("teams",["Unknown","Unknown"])
    outcome=info.get("outcome",{})

    match_info = {
      "match_id": info.get("event", {}).get("match_number", "N/A"),
      "date": info.get("dates", ["N/A"])[0],
            "venue": info.get("venue", "Unknown"),
            "city": info.get("city", "Unknown"),
            "team1": teams[0] if len(teams) > 0 else "Unknown",
            "team2": teams[1] if len(teams) > 1 else "Unknown",
            "winner": outcome.get("winner", "No Result"),
            "toss_winner": info.get("toss", {}).get("winner", "Unknown"),
            "toss_decision": info.get("toss", {}).get("decision", "Unknown"),
            "player_of_match": (
                info.get("player_of_match", ["Unknown"])[0]
                if info.get("player_of_match")
                else "Unknown"
            ),
    }

    return match_info
  
  def parse_innings(self, match_data):
    """ 
    Extract innings and ball-by-ball delivery data
    """
    innings_data = []
    
    innings_list= match_data.get("innings", [])

    for innings_index, innings in enumerate(innings_list, start=1):

      team_name = innings.get("team","Unknown")

      overs = innings.get("overs",[])

      for over_data in overs:
        over_number = over_data.get("over",0)
        deliveries = over_data.get("deliveries", [])

        for ball_index, delivery in enumerate(deliveries, start=1):
          batter = delivery.get("batter", "Unknown")
          bowler = delivery.get("bowler", "Unknown")
          non_striker = delivery.get("non_striker", "Unknown")

          runs_info = delivery.get("runs", {})
          batter_runs = runs_info.get("batter", 0)
          extras = runs_info.get("extras", 0)
          total_runs = runs_info.get("total", 0)

          wicket_info = delivery.get("wickets", [])
          wicket_type = None
          player_out = None
          if wicket_info:
            wicket_type = wicket_info[0].get("kind", None)
            player_out = wicket_info[0].get("player_out", None)

          innings_data.append({
            "innings": innings_index,
            "batting_team": team_name,
            "over": over_number,
            "ball": ball_index,
            "batter": batter,
            "bowler": bowler,
            "non_striker": non_striker,
            "batter_runs": batter_runs,
            "extras": extras,
            "total_runs": total_runs,
            "wicket_type": wicket_type,
            "player_out": player_out,
          })

    return innings_data

  def parse_match(self, file_path):
    """
    Parse complete match file
    """
    match_data = self.load_match_file(file_path)
    match_info = self.parse_match_info(match_data)
    innings_data = self.parse_innings(match_data)
    return {"match_info": match_info, "innings_data": innings_data}

  def parse_all_matches(self):

    all_matches = []

    json_files = list(Path(self.data_path).glob("*.json"))

    print(f"\nJSON Files Found: {len(json_files)}")

    for file in json_files:

        try:

            parsed_match = self.parse_match(file)

            all_matches.append(parsed_match)

            print(f"Parsed: {file.name}")

        except Exception as e:

            print(f"Error parsing {file.name}: {e}")

    return all_matches


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    DATASET_PATH = BASE_DIR / "data" / "raw" / "ipl" / "ipl_json"

    print(f"\nDataset Path: {DATASET_PATH}")

    parser = CricketMatchParser(DATASET_PATH)

    matches = parser.parse_all_matches()

    print("\n========== SAMPLE MATCH ==========\n")

    if matches:

        sample_match = matches[0]

        print("MATCH INFO:\n")
        print(sample_match["match_info"])

        print("\nFIRST 5 DELIVERIES:\n")

        for delivery in sample_match["innings_data"][:5]:
            print(delivery)

    print(f"\nTotal Matches Parsed: {len(matches)}")