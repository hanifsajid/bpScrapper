from selenium.webdriver.common.by import By
import time
import random
import re


def format_state_names(election_states_str):
    states = [state.strip() for state in re.split(r'[•,]', election_states_str)]
    formatted_states = [f"{state}" for state in states if state]  # Exclude empty strings
    return formatted_states



def is_driver_running(driver):
    try:
        return driver.service.process.poll() is None
    except Exception as e:
        return False


def fetchresults2016(url, year, state, driver):
    driver.get(url)
    time.sleep(random.uniform(3, 5))
    
    tables = driver.find_elements(By.CSS_SELECTOR, "table.table")

    target_table = None
    for table in tables:
        caption = table.find_element(By.CSS_SELECTOR, "caption.general")
        print(caption.text)
        if str(year) in caption.text:
            target_table = table
            break

    if not target_table:
        print(f"Could not find a table for {state} in {year}.")
        return [] 
    
    all_cases = []
    rows = target_table.find_elements(By.CSS_SELECTOR, "tbody tr")

    for row in rows:
        columns = row.find_elements(By.TAG_NAME, "td")
        
        if len(columns) == 5:
            party = columns[1].text.strip()  # Party column
            candidate = columns[2].text.strip()  # Candidate column
            winner = False
            
            try:
                won_element = columns[2].find_element(By.XPATH, './/a[@title="Won"]')  # Using relative XPath
                if won_element:
                    winner = True
            except:
                winner = False  
            
            vote_percentage = columns[3].text.strip()  # Vote % column
            votes = columns[4].text.strip()  # Votes column
        
            
            incumbent = False
            if "Incumbent" in candidate:
                incumbent = True
                candidate = candidate.replace("Incumbent", "").strip()
            
            case = [year, state, candidate, party, "", vote_percentage, votes, winner, incumbent, "", ""]

            all_cases.append(case)
        else:
            for column in columns:
                print(column.text)
            print("_"*80)
    return all_cases


def fetchresults_2018onwards(url, year, state, driver): # 2024, 2022, 2020, 2018
    driver.get(url)
    time.sleep(random.uniform(3, 5))

        # Find the results_text element containing "general election" and the year 2024
    result_texts = driver.find_elements(By.CLASS_NAME, 'results_text')


    # Loop through each results_text to check if it contains "general election" and "2024"
    for result_text in result_texts:
        text = result_text.text.lower()
        if "general election" in text and str(year) in text:
            # Get the table that is associated with this results_text
            table_container = result_text.find_element(By.XPATH, './following-sibling::div[@class="results_table_container"]')
            table = table_container.find_element(By.CLASS_NAME, 'results_table')

            all_cases = []
            # Find all the rows in the table (ignoring the header row)
            rows = table.find_elements(By.TAG_NAME, 'tr')[1:]

            for row in rows:
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) == 5:
                    winner_col = columns[0].text.strip()
                    if"✔" in winner_col:
                        winner = True
                    else:
                        winner = False
                    # Extract candidate info from the third column
                    candidate_column = columns[2]

                    # Get the candidate info text (to compare the content)
                    candidate_info = candidate_column.text.strip()

                    try:
                        # Check if the element contains both <b> and <u> tags (either of them, or both)
                        bold = candidate_column.find_element(By.TAG_NAME, "b")
                        underline = candidate_column.find_element(By.TAG_NAME, "u")

                        # If both bold and underline are found
                        if bold and underline:
                            incumbent = True
                    except:
                        incumbent = False
                    
                    info_parts = candidate_info.split('(')
                    cand_name = info_parts[0].split(')')[0] if len(info_parts) > 1 else ''
                    main_party = info_parts[1].split(')')[0] if len(info_parts) > 1 else ''
                    additional_writein = info_parts[2].split(')')[0] if len(info_parts) > 2 else '' 

                    try:
                        link = candidate_column.find_element(By.TAG_NAME, "a")
                        href = link.get_attribute('href')
                    except:
                        href = ""
                    
                    vote_percentage = columns[3].text.strip()  # Vote % column
                    votes = columns[4].text.strip()  # Votes column

                    case = [year, state, cand_name, main_party, additional_writein, vote_percentage, votes, winner, incumbent, href, candidate_info]
                    
                    all_cases.append(case)
                else:
                    print(f"Could not general election data for {state} in {year}.")
                    return [] 
            return all_cases
