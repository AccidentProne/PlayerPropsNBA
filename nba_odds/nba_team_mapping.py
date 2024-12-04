import gspread
from google.oauth2.service_account import Credentials
import unicodedata
from nba_api.stats.endpoints import leaguedashplayerstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat
import pandas as pd

# Set up Google Sheets API credentials
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME = 'nba_odds'  # Update this to the actual worksheet name if different

# Authenticate with Google Sheets API
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)

# Access the Google Sheet
sheet = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME)

# Fetch player stats with team information
def fetch_player_stats():
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        per_mode_detailed='PerGame',
        season='2024-25',
        season_type_all_star='Regular Season'
    )
    stats_df = player_stats.get_data_frames()[0]
    player_team_df = stats_df[['PLAYER_NAME', 'TEAM_ABBREVIATION']]
    return player_team_df

# Standardizes player names by removing special characters and handling exceptions
def remove_special_characters(name):
    # Handle special exceptions
    if name == "Moritz Wagner":
        return "Moe Wagner"
    if name == "Nic Claxton":
        return "Nicolas Claxton"
    if name == "Alex Sarr":
        return "Alexandre Sarr"
    if name in ["Derrick Jones Jr.", "Derrick Jones Jr", "Derrick Jones"]:
        return "Derrick Jones Jr"
    if name == "AJ Green":
        return "A. J. Green"
    if name == "Andre Jackson Jr":
        return "Andre Jackson Jr."

    return ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    ).replace('.', '')

# Load the nba_odds.csv into a DataFrame (from the Google Sheet or file)
nba_odds_df = pd.DataFrame(sheet.get_all_records())

# Fetch the player-team data
player_team_df = fetch_player_stats()

# Team abbreviation to full team name mapping
team_mapping = {
    'ATL': 'Atlanta Hawks',
    'BOS': 'Boston Celtics',
    'BKN': 'Brooklyn Nets',
    'CHA': 'Charlotte Hornets',
    'CHI': 'Chicago Bulls',
    'CLE': 'Cleveland Cavaliers',
    'DAL': 'Dallas Mavericks',
    'DEN': 'Denver Nuggets',
    'DET': 'Detroit Pistons',
    'GSW': 'Golden State Warriors',
    'HOU': 'Houston Rockets',
    'IND': 'Indiana Pacers',
    'LAC': 'Los Angeles Clippers',
    'LAL': 'Los Angeles Lakers',
    'MEM': 'Memphis Grizzlies',
    'MIA': 'Miami Heat',
    'MIL': 'Milwaukee Bucks',
    'MIN': 'Minnesota Timberwolves',
    'NOP': 'New Orleans Pelicans',
    'NYK': 'New York Knicks',
    'OKC': 'Oklahoma City Thunder',
    'ORL': 'Orlando Magic',
    'PHI': 'Philadelphia 76ers',
    'PHX': 'Phoenix Suns',
    'POR': 'Portland Trail Blazers',
    'SAC': 'Sacramento Kings',
    'SAS': 'San Antonio Spurs',
    'TOR': 'Toronto Raptors',
    'UTA': 'Utah Jazz',
    'WAS': 'Washington Wizards'
}

# Clean player names to ensure consistency in matching
def clean_player_name(name):
    return remove_special_characters(name)

nba_odds_df['Player_cleaned'] = nba_odds_df['Player'].apply(clean_player_name)
player_team_df['PLAYER_NAME_cleaned'] = player_team_df['PLAYER_NAME'].apply(clean_player_name)

# Merge the DataFrames to add the team abbreviation information
merged_df = pd.merge(nba_odds_df, player_team_df[['PLAYER_NAME_cleaned', 'TEAM_ABBREVIATION']], 
                     left_on='Player_cleaned', right_on='PLAYER_NAME_cleaned', how='left')

# Replace abbreviations with full team names
merged_df['TEAM_NAME'] = merged_df['TEAM_ABBREVIATION'].map(team_mapping)

# Insert the Team column between Player and BetMGM
cols = list(merged_df.columns)
team_col_index = cols.index('TEAM_NAME')
cols.insert(1, cols.pop(team_col_index))  # Move 'TEAM_NAME' after 'Player'

# Reorder columns and drop extra 'cleaned' columns
final_df = merged_df[cols].drop(columns=['Player_cleaned', 'PLAYER_NAME_cleaned', 'TEAM_ABBREVIATION'])

# Replace NaN values with 'null' (or any placeholder)
final_df = final_df.fillna('null')

# Update the Google Sheet with the new data
sheet.update([final_df.columns.values.tolist()] + final_df.values.tolist())

# Apply formatting (optional)
format_cell_range(sheet, 'A1:F1', CellFormat(textFormat=TextFormat(bold=True)))  # Assuming 6 columns (Player, Team, BetMGM, etc.)
format_cell_range(sheet, f'B2:B{len(final_df) + 1}', CellFormat(horizontalAlignment='RIGHT'))  # Center align Team column

print("Team stats have been successfully uploaded to 'nba_odds' sheet.")
