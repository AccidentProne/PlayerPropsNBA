import gspread
from google.oauth2.service_account import Credentials
from nba_api.stats.endpoints import leaguedashplayerstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat
import unicodedata

# Google Sheets credentials and setup
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_PLAYER_STATS = 'player_stats_per_pos'

# Authenticate with Google Sheets API
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_player_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_PLAYER_STATS)

# Clear all content from the specified worksheet
def clear_sheet(sheet):
    sheet.clear()

# Standardize player names by removing special characters and handling exceptions
def remove_special_characters(name):
    if name == "Moritz Wagner":
        return "Moe Wagner"
    if name == "Nic Claxton":
        return "Nicolas Claxton"
    return ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    ).replace('.', '')

# Fetch and process player stats from the NBA API
def fetch_player_stats():
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
    )
    stats_df = player_stats.get_data_frames()[0]
    stats_df = stats_df[stats_df['FGA'] > 0.0]  # Filter players with zero field goal attempts
    stats_df['FGA'] = stats_df['FGA'] / 100  # Scale FGA per 100 possessions
    columns = ['PLAYER_NAME', 'FGA', 'FG_PCT', 'FG3A', 'FG3_PCT', 'FTA', 
               'FT_PCT', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'PTS']
    stats_df = stats_df[columns]
    stats_df.loc[:, 'FG_PCT'] *= 100
    stats_df.loc[:, 'FG3_PCT'] *= 100
    stats_df.loc[:, 'FT_PCT'] *= 100
    for col in ['FTA', 'OREB', 'DREB', 'AST', 'STL', 'BLK', 'PTS', 'FG3A']:
        stats_df.loc[:, col] /= 100
    stats_df.update(stats_df.select_dtypes(include='number').round(3))  # Round numerical values to 3 decimal places
    return stats_df

# Upload player stats to Google Sheets
def upload_player_stats_to_sheet():
    player_stats_df = fetch_player_stats()
    rows = [["Player", "FGA", "FG_PCT", "FG3A", "FG3_PCT", "FTA", "FT_PCT", 
             "OREB", "DREB", "AST", "STL", "BLK", "PTS"]]
    for _, row in player_stats_df.iterrows():
        rows.append([remove_special_characters(row['PLAYER_NAME'])] + row[1:].tolist())
    if len(rows) == 1:  # No data to upload
        print("No player stats found.")
        return
    clear_sheet(sheet_player_stats)
    sheet_player_stats.update(values=rows, range_name='A1')
    format_cell_range(sheet_player_stats, 'A1:N1', CellFormat(textFormat=TextFormat(bold=True)))
    format_cell_range(sheet_player_stats, f'B2:N{len(rows)}', CellFormat(horizontalAlignment='RIGHT'))
    print("Player stats have been successfully uploaded to 'player_stats_per_pos' sheet.")

# Main entry point to run the script
def main():
    upload_player_stats_to_sheet()

if __name__ == "__main__":
    main()
