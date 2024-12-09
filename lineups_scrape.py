from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Set up WebDriver
driver = webdriver.Chrome()

# Navigate to the webpage
url = "https://www.lineups.com/nba/nba-player-minutes-per-game"
driver.get(url)

# Wait for the page to load
driver.implicitly_wait(10)

# Locate the table wrapper
table_wrapper = driver.find_element(By.CLASS_NAME, "horizontal-table-wrapper.two-col")

# Locate the table inside the wrapper
table = table_wrapper.find_element(By.TAG_NAME, "table")

# Extract all rows (including potential header row)
rows = table.find_elements(By.TAG_NAME, "tr")

# Manually define headers to include "Name" if missing
headers = ["Name"]  # Default first column as "Name"
for cell in rows[0].find_elements(By.TAG_NAME, "th")[1:]:  # Skip the first header cell
    headers.append(cell.text.strip() or "Unnamed Column")

# Extract data rows
data = []
for row in rows[1:]:  # Skip header row
    cells = row.find_elements(By.TAG_NAME, "td")
    row_data = [cell.text for cell in cells]
    data.append(row_data)

# Ensure DataFrame columns align with data
df = pd.DataFrame(data, columns=headers)

# Save the table to a CSV
output_file = "output_table_with_name.csv"
df.to_csv(output_file, index=False)

print(f"Table with 'Name' column saved to {output_file}")
driver.quit()
