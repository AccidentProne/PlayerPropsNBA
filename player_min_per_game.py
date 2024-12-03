import gspread
from google.oauth2.service_account import Credentials
from nba_api.stats.endpoints import leaguedashplayerstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat
import unicodedata

# Path to the Google service account credentials file
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'

# Google Sheets configuration
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_PLAYER_STATS = 'player_min_per_game'

# Authenticate and initialize the Google Sheets client
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)
sheet_player_stats = client.open_by_key(SPREADSHEET_ID).worksheet(WORKSHEET_NAME_PLAYER_STATS)

# Standardizes player names by removing special characters and handling exceptions
def remove_special_characters(name):
    if name == "Moritz Wagner":
        return "Moe Wagner"
    if name == "Nic Claxton":
        return "Nicolas Claxton"
    return ''.join(
        c for c in unicodedata.normalize('NFD', name)
        if unicodedata.category(c) != 'Mn'
    ).replace('.', '')

# Fetches player stats for the current season from the NBA API
def fetch_player_stats():
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        per_mode_detailed='PerGame',
        season='2024-25',
        season_type_all_star='Regular Season',
    )
    stats_df = player_stats.get_data_frames()[0]
    return stats_df[stats_df['MIN'] > 0.0][['PLAYER_NAME', 'MIN']]

# Clears all data from the specified worksheet
def clear_sheet(sheet):
    sheet.clear()

# Uploads player stats to Google Sheets
def upload_player_stats_to_sheet():
    clear_sheet(sheet_player_stats)
    player_stats_df = fetch_player_stats()
    stats_rows = [["Player", "MIN"]]

    # Clean player names and add rows to upload
    for _, row in player_stats_df.iterrows():
        stats_rows.append([remove_special_characters(row['PLAYER_NAME']), row['MIN']])

    if len(stats_rows) == 1:  # Only the header row exists, no data found
        print("No player stats found.")
        return

    sheet_player_stats.update(values=stats_rows, range_name='A1')

    # Apply formatting to the sheet
    format_cell_range(sheet_player_stats, 'A1:B1', CellFormat(textFormat=TextFormat(bold=True)))
    format_cell_range(sheet_player_stats, f'B2:B{len(stats_rows)}', CellFormat(horizontalAlignment='RIGHT'))

    print("Player stats have been successfully uploaded to 'player_min_per_game' sheet.")

# Main function to execute the script
def main():
    upload_player_stats_to_sheet()

# Entry point for the script
if __name__ == "__main__":
    main()
