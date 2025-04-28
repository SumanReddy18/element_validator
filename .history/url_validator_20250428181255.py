import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def validate_urls(csv_path, rerun_only_failed=False):
    setup_logging()
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # If rerunning, filter only failed rows
    if rerun_only_failed:
        df = df[df['status'] == 'FAIL']
        if df.empty:
            logging.info("No failed cases to re-run.")
            return

    # Setup webdriver with additional options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)
    
    # Add status and error_message columns if not present
    if 'status' not in df.columns:
        df['status'] = ''
    if 'error_message' not in df.columns:
        df['error_message'] = ''
    
    try:
        for index, row in df.iterrows():
            url = row['url']
            target_node = row['target_node']
            
            logging.info(f"Checking URL: {url}")
            logging.info(f"Looking for element: {target_node}")
            
            try:
                driver.get(url)
                # Wait up to 20 seconds for element
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, target_node))
                )
                
                # Additional verification: check if element is interactable
                if element.is_displayed() and element.is_enabled():
                    df.at[index, 'status'] = 'PASS'
                    logging.info(f"Element found and interactable at {url}")
                else:
                    df.at[index, 'status'] = 'FAIL'
                    df.at[index, 'error_message'] = 'Element exists but not interactable'
                    logging.warning(f"Element exists but not interactable at {url}")
                    
            except TimeoutException:
                df.at[index, 'status'] = 'FAIL'
                df.at[index, 'error_message'] = 'Element not found (timeout)'
                logging.error(f"Timeout waiting for element at {url}")
            except WebDriverException as e:
                df.at[index, 'status'] = 'ERROR'
                df.at[index, 'error_message'] = str(e)
                logging.error(f"WebDriver error for {url}: {str(e)}")
            except Exception as e:
                df.at[index, 'status'] = 'ERROR'
                df.at[index, 'error_message'] = str(e)
                logging.error(f"Unexpected error for {url}: {str(e)}")
    
    finally:
        driver.quit()
    
    # Create output filename
    file_name = os.path.splitext(csv_path)[0]
    output_file = f"{file_name}_validation.csv"
    
    # Save results
    df.to_csv(output_file, index=False)
    logging.info(f"Validation complete. Results saved to: {output_file}")

def rerun_failed_cases(csv_path):
    logging.info("Re-running validation for failed cases...")
    validate_urls(csv_path, rerun_only_failed=True)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python url_validator.py <csv_file_path> [--rerun-failed]")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    rerun_failed = '--rerun-failed' in sys.argv
    
    if rerun_failed:
        rerun_failed_cases(csv_file)
    else:
        validate_urls(csv_file)