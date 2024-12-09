from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up WebDriver
driver = webdriver.Chrome()

# Navigate to the webpage
url = "https://www.lineups.com/nba/nba-player-minutes-per-game"
driver.get(url)

# Explicit wait for the table to load
wait = WebDriverWait(driver, 15)
table_wrapper = wait.until(
    EC.presence_of_element_located((By.CLASS_NAME, "horizontal-table-wrapper.two-col"))
)

# Locate the table inside the wrapper
table = table_wrapper.find_element(By.TAG_NAME, "table")

# Extract all rows (including potential header row)
rows = table.find_elements(By.TAG_NAME, "tr")

# Extract headers
headers = []
for cell in rows[0].find_elements(By.TAG_NAME, "th"):
    headers.append(cell.text.strip() or "Unnamed Column")

# Extract data rows
data = []
for row in rows[1:]:  # Skip header row
    try:
        # Locate the player name (assuming it's in a specific <th> or nested element)
        name_cell = row.find_element(By.CLASS_NAME, "player-name-col")
        player_name = name_cell.text.strip()
    except:
        player_name = "Unknown Name"  # Default if name can't be found

    # Extract other row data
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [player_name] + [cell.text for cell in cells]
    data.append(row_data)

# Add "Name" to the headers if it's not already there
if "Name" not in headers:
    headers = ["Name"] + headers  # Prepend "Name" to the headers

# Create a DataFrame and save to CSV
df = pd.DataFrame(data, columns=headers)
output_file = "output_table_with_player_names.csv"
df.to_csv(output_file, index=False)

print(f"Table with player names saved to {output_file}")
driver.quit()
