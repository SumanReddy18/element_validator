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

def validate_element(driver, target_node):
    try:
        # Try different strategies to find the element
        strategies = [
            (By.CSS_SELECTOR, target_node),
            (By.XPATH, target_node),
            (By.ID, target_node),
            (By.CLASS_NAME, target_node)
        ]
        
        element = None
        used_strategy = None
        
        for strategy, selector in strategies:
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((strategy, selector))
                )
                used_strategy = strategy
                break
            except:
                continue
        
        if not element:
            return False, "Element not found with any strategy"
            
        # Special handling for meta tags and head elements
        if element.tag_name.lower() in ['meta', 'link', 'style', 'script']:
            return True, f"Found {element.tag_name} element using {used_strategy}"
            
        # For visible elements, perform additional checks
        is_visible = element.is_displayed()
        is_enabled = element.is_enabled()
        in_viewport = driver.execute_script("""
            var elem = arguments[0];
            var rect = elem.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        """, element)
        
        if is_visible and is_enabled and in_viewport:
            return True, "Element is fully visible, enabled, and in viewport"
        elif is_visible and is_enabled:
            return True, "Element is visible and enabled but outside viewport"
        elif is_visible:
            return True, "Element is visible but may not be interactive"
        else:
            return False, "Element exists but is not visible"
            
    except Exception as e:
        return False, f"Validation error: {str(e)}"

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
                success, message = validate_element(driver, target_node)
                
                if success:
                    df.at[index, 'status'] = 'PASS'
                    df.at[index, 'error_message'] = message
                    logging.info(f"Success: {message}")
                else:
                    df.at[index, 'status'] = 'FAIL'
                    df.at[index, 'error_message'] = message
                    logging.warning(f"Failed: {message}")
                    
            except TimeoutException:
                df.at[index, 'status'] = 'FAIL'
                df.at[index, 'error_message'] = 'Page load timeout'
                logging.error(f"Timeout loading page at {url}")
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