import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

def validate_urls(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Setup webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    # Add status column
    df['status'] = ''
    
    try:
        for index, row in df.iterrows():
            url = row['url']
            target_node = row['target_node']
            
            try:
                driver.get(url)
                # Wait up to 10 seconds for element
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, target_node))
                )
                df.at[index, 'status'] = 'PASS'
            except TimeoutException:
                df.at[index, 'status'] = 'FAIL'
            except Exception as e:
                df.at[index, 'status'] = f'ERROR: {str(e)}'
    
    finally:
        driver.quit()
    
    # Create output filename
    file_name = os.path.splitext(csv_path)[0]
    output_file = f"{file_name}_validation.csv"
    
    # Save results
    df.to_csv(output_file, index=False)
    print(f"Validation complete. Results saved to: {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python url_validator.py <csv_file_path>")
        sys.exit(1)
    
    validate_urls(sys.argv[1])
