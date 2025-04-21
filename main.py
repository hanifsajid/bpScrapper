import argparse
import pandas as pd
import utils
import os
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)



def get_args():
    parser = argparse.ArgumentParser()
  
    parser.add_argument('--year', type=int, required=True, help= "Year of election for which the data is scrapped")
    parser.add_argument('--output_dir', default="scrapped_data", help= "Output directory containing scrapped data")
    parser.add_argument('--output_file', default="senate{year}.csv", help= "A dataframe containing scrapped data")
    parser.add_argument('--states_str', type=str, required=True, help= "String of states copied for ballotpedia for which the results are retrieved")
 
    args = parser.parse_args()
    args.output_file = args.output_file.format(year=args.year)
    
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Output directory '{args.output_dir}' created.")

    return args

 
if __name__ == '__main__':
    args = get_args()

    config = vars(args)

    output_file_path = os.path.join(config["output_dir"], config["output_file"])

    states_str = config["states_str"] 

    states = utils.format_state_names(states_str)

    df = pd.DataFrame(columns = ["year", "state", "candidate", "party", "writein_details", "vote_percentage", "votes", "winner","incumbent", "bio_url", "additional_info"])


    for state_i in states:
        state_name = state_i.replace(" ", "_")
        if "special" in state_name:
            state_only = state_name.rsplit('_', 1)[0]
            url = f"https://ballotpedia.org/United_States_Senate_special_election_in_{state_only},_{config['year']}"
        else:
            url = f"https://ballotpedia.org/United_States_Senate_election_in_{state_name},_{config['year']}"

        try:
            if config["year"] == 2016:
                all_cases = utils.fetchresults2016(url, config['year'], state_i, driver)
            else:
                all_cases = utils.fetchresults_2018onwards(url, config['year'], state_i, driver)

            for case in all_cases:
                df.loc[len(df)] = case
            print(f"Case done for:  {state_i}")
        except Exception as e: 
            print(f"Error with {state_i}: {e}")
            
        time.sleep(random.uniform(4, 10))  
    driver.quit()
    df.to_csv(output_file_path, index=False)
    print(f"All documents for the year: {config['year']} are retrieved.")