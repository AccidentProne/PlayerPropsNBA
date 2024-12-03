import gspread
from google.oauth2.service_account import Credentials
from nba_api.stats.endpoints import leaguedashteamstats
from gspread_formatting import format_cell_range, CellFormat, TextFormat

# Google Sheets credentials and configuration
SERVICE_ACCOUNT_FILE = 'C:/Users/tyler/playerpropsnba-64aafb0d30ae.json'
SPREADSHEET_ID = '1tP6jNJnNwv5LWDtOp9AwfL5ZljYQRRqDc_kMKVYNevA'
WORKSHEET_NAME_TEAM_PACE = 'team_pace_per_pos'

# Authenticate with Google Sheets API
SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
client = gspread.authorize(credentials)

# Access an existing worksheet or create a new one if it doesn't exist
def get_or_create_worksheet(spreadsheet_id, worksheet_name):
    try:
        return client.open_by_key(spreadsheet_id).worksheet(worksheet_name)
    except gspread.exceptions.WorksheetNotFound:
        return client.open_by_key(spreadsheet_id).add_worksheet(title=worksheet_name, rows=100, cols=10)

# Fetch team pace stats for the 2024-25 NBA season from the NBA API
def fetch_team_pace():
    team_stats = leaguedashteamstats.LeagueDashTeamStats(
        per_mode_detailed='Per100Possessions',
        season='2024-25',
        season_type_all_star='Regular Season',
        measure_type_detailed_defense='Advanced'
    )
    stats_df = team_stats.get_data_frames()[0]
    if 'PACE' not in stats_df.columns:
        raise KeyError("'PACE' column not found in the returned data.")
    return stats_df[['TEAM_NAME', 'PACE']]

# Clears all data from the specified worksheet
def clear_sheet(sheet):
    sheet.clear()

# Upload team pace stats to Google Sheets
def upload_team_pace_to_sheet():
    team_pace_df = fetch_team_pace()
    rows = [team_pace_df.columns.tolist()] + team_pace_df.values.tolist()
    sheet = get_or_create_worksheet(SPREADSHEET_ID, WORKSHEET_NAME_TEAM_PACE)
    clear_sheet(sheet)
    sheet.update(values=rows, range_name='A1')
    format_cell_range(sheet, 'A1:B1', CellFormat(textFormat=TextFormat(bold=True)))
    format_cell_range(sheet, f'B2:B{len(rows)}', CellFormat(horizontalAlignment='RIGHT'))
    print("Team pace stats have been successfully uploaded to 'team_pace_per_pos' sheet.")

# Main function to run the script
def main():
    upload_team_pace_to_sheet()

# Entry point for the script
if __name__ == "__main__":
    main()
