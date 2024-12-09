import sys
from nba_player_stats.nba_player_stats_per_poss import main as player_stats_per_poss_main
from nba_player_stats.nba_player_stats_per_game import main as player_stats_per_game_main
from nba_opponent_stats.opponent_stats_per_poss import main as opponent_stats_per_poss_main
from nba_odds.nba_odds_script import main as nba_odds_script_main
from nba_odds.nba_team_mapping import main as nba_team_mapping_main
from nba_odds.nba_game_import import main as nba_game_import_main
from nba_odds.nba_opponent_team_mapping import main as nba_opponent_team_mapping_main
from nba_team_stats.nba_team_pace_per_poss import main as team_pace_per_poss_main
from nba_team_stats.nba_team_stats_per_game import main as team_stats_per_game_main
from nba_team_stats.nba_team_stats_per_poss import main as team_stats_per_poss_main

def main():
    
    sys.dont_write_bytecode = True
    print("Starting the NBA player stats automation script...")
    player_stats_per_poss_main()
    player_stats_per_game_main()
    team_pace_per_poss_main()
    team_stats_per_game_main()
    team_stats_per_poss_main()
    opponent_stats_per_poss_main()
    nba_odds_script_main()
    nba_game_import_main()
    nba_team_mapping_main()
    nba_opponent_team_mapping_main()
    
    print("Script completed successfully.")
    
if __name__ == "__main__":
    main()
