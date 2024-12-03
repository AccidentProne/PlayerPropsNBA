import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from gspread_formatting import *
import warnings
import unicodedata

# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Google Sheets credentials and configuration
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_PLAYER_STATS = 'Player Stats PerGame'

# Google Sheets client setup
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_player_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_PLAYER_STATS)

def remove_special_characters(name):
    """Removes special characters and hard-codes certain names."""
    # Replace specific player names with their preferred names
    if name == "Moritz Wagner":
        return "Moe Wagner"
    if name == "Nic Claxton":
        return "Nicolas Claxton"
    
    # Remove accents and special characters from names
    name_no_special_chars = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    
    # Remove periods from the name
    name_cleaned = name_no_special_chars.replace('.', '')
    return name_cleaned

def fetch_player_stats():
    """Fetch player stats for the 2024-25 NBA season using the NBA API."""
    # Fetch player statistics from the NBA API
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        per_mode_detailed='PerGame',
        season='2024-25',
        season_type_all_star='Regular Season',
    )

    # Convert the fetched data into a pandas DataFrame
    stats_df = player_stats.get_data_frames()[0]
    
    # Filter out players with zero minutes played
    stats_df_filtered = stats_df[stats_df['MIN'] > 0.0]
    
    # Select only the player name and minutes played columns
    player_MIN_df = stats_df_filtered[['PLAYER_NAME', 'MIN']]
    
    return player_MIN_df

def clear_sheet(sheet):
    """Clears the content of the provided Google Sheets worksheet."""
    sheet.clear()

def upload_player_stats_to_sheet():
    """Uploads cleaned player stats to the 'Player Stats Import' worksheet in Google Sheets."""
    # Clear the sheet before importing new data
    clear_sheet(sheet_player_stats)
    
    # Fetch player stats from the NBA API
    player_stats_df = fetch_player_stats()
    
    # Prepare the data for upload
    stats_rows = [["Player", "MIN"]]  # Header row
    
    # Clean the player names and collect the data
    for _, row in player_stats_df.iterrows():
        cleaned_name = remove_special_characters(row['PLAYER_NAME'])
        stats_rows.append([cleaned_name, row['MIN']])
    
    # If no data found, exit
    if not stats_rows:
        print("No player stats found.")
        return
    
    # Upload the stats to the Google Sheets worksheet
    sheet_player_stats.update(values=stats_rows, range_name='A1')
    
    # Format the header row to be bold
    header_format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet_player_stats, 'A1:B1', header_format)
    
    # Right-align the 'Minutes Played' column
    format_cell_range(sheet_player_stats, 'B2:B' + str(len(stats_rows) + 1), CellFormat(horizontalAlignment='RIGHT'))
    
    print("Player stats have been successfully uploaded to 'Player Stats Import' sheet.")

def main():
    """Main function to fetch and upload player stats."""
    upload_player_stats_to_sheet()

# Entry point for the script
if __name__ == "__main__":
    main()
