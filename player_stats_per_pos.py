import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from gspread_formatting import *
import warnings
import unicodedata

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Google Sheets credentials and setup
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_PLAYER_STATS = 'Player Stats Per1Poss'

# Setup the Google Sheets client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_player_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_PLAYER_STATS)

# Function to clear the content of the sheet
def clear_sheet(sheet):
    sheet.clear()

# Function to remove special characters from player names
def remove_special_characters(name):
    # Specific player name corrections
    if name == "Moritz Wagner":
        return "Moe Wagner"
    if name == "Nic Claxton":
        return "Nicolas Claxton"
    
    # Normalize the name by removing accents and special characters
    name_no_special_chars = ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    )
    
    # Remove periods from the name
    name_cleaned = name_no_special_chars.replace('.', '')
    return name_cleaned

# Function to fetch player stats for the 2024-25 NBA season
def fetch_player_stats():
    # Fetching player stats from the NBA API (Per 100 possessions)
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
    )
    
    # Convert the data into a pandas DataFrame
    stats_df = player_stats.get_data_frames()[0]
    
    # Filter out players who have not played enough minutes
    stats_df_filtered = stats_df[stats_df['FGA'] > 0.0]
    
    # Adjust FGA by moving the decimal two places to the left
    stats_df_filtered['FGA'] = stats_df_filtered['FGA'] / 100
    
    # Define the columns we want to use
    player_stats_columns = [
        'PLAYER_NAME', 'FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA', 
        'FT_PCT', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'PTS'
    ]
    
    # Create a new DataFrame with the selected columns
    player_stats_df = stats_df_filtered[player_stats_columns]
    
    # Apply adjustments to specific statistics
    player_stats_df.loc[:, 'FG_PCT'] = player_stats_df['FG_PCT'] * 100  # Convert FG% to percentage
    player_stats_df.loc[:, 'FTA'] = player_stats_df['FTA'] / 100  # Adjust FTA by dividing by 100
    player_stats_df.loc[:, 'OREB'] = player_stats_df['OREB'] / 100  # Adjust OREB by dividing by 100
    player_stats_df.loc[:, 'PTS'] = player_stats_df['PTS'] / 100  # Adjust PTS by dividing by 100
    player_stats_df.loc[:, 'AST'] = player_stats_df['AST'] / 100  # Adjust AST by dividing by 100
    player_stats_df.loc[:, 'STL'] = player_stats_df['STL'] / 100  # Adjust STL by dividing by 100
    player_stats_df.loc[:, 'BLK'] = player_stats_df['BLK'] / 100  # Adjust BLK by dividing by 100
    player_stats_df.loc[:, 'FG3A'] = player_stats_df['FG3A'] / 100  # Adjust 3PA by dividing by 100
    player_stats_df.loc[:, 'DREB'] = player_stats_df['DREB'] / 100  # Adjust DREB by dividing by 100
    player_stats_df.loc[:, 'FG3_PCT'] = player_stats_df['FG3_PCT'] * 100  # Convert 3P% to percentage
    player_stats_df.loc[:, 'FT_PCT'] = player_stats_df['FT_PCT'] * 100  # Convert FT% to percentage
    
    # Round all numerical columns to 3 decimal places
    numerical_columns = ['FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA', 'FT_PCT', 
                         'OREB', 'DREB', 'AST', 'STL', 'BLK', 'PTS']
    player_stats_df[numerical_columns] = player_stats_df[numerical_columns].applymap(lambda x: round(x, 3))
    
    return player_stats_df

# Function to upload player stats to the Google Sheets
def upload_player_stats_to_sheet():
    # Fetch player stats from the NBA API
    player_stats_df = fetch_player_stats()
    
    # Prepare the header row for Google Sheets
    stats_rows = [["Player", "FGA", "FG_PCT", "FG3A", "FG3_PCT", "FTA", "FT_PCT", "OREB", "DREB", "AST", "STL", "BLK", "PTS"]]
    
    # Loop through the player stats and prepare each row for upload
    for _, row in player_stats_df.iterrows():
        cleaned_name = remove_special_characters(row['PLAYER_NAME'])
        stats_row = [cleaned_name]  # Player name stays in column A
        stats_row.extend([  # Stats now start from column B
            row['FGA'], row['FG_PCT'], row['FG3A'], row['FG3_PCT'],
            row['FTA'], row['FT_PCT'], row['OREB'], row['DREB'],
            row['AST'], row['STL'], row['BLK'], row['PTS']
        ])
        stats_rows.append(stats_row)
    
    # Check if there is any data to upload
    if not stats_rows:
        print("No player stats found.")
        return
    
    # Clear the existing content in the sheet before uploading new data
    clear_sheet(sheet_player_stats)
    
    # Upload the data to the 'Player Stats Import' sheet starting from cell A1
    sheet_player_stats.update(values=stats_rows, range_name='A1')
    
    # Format the header row to be bold
    header_format = CellFormat(textFormat=TextFormat(bold=True))
    format_cell_range(sheet_player_stats, 'A1:N1', header_format)
    
    # Format the numerical columns (from B to N) to be right-aligned
    format_cell_range(sheet_player_stats, 'B2:N' + str(len(stats_rows) + 1), CellFormat(horizontalAlignment='RIGHT'))
    
    print("Player stats have been successfully uploaded to 'Player Stats Import' sheet.")


# Main function to run the script
def main():
    upload_player_stats_to_sheet()

# Run the script if it is executed directly
if __name__ == "__main__":
    main()
