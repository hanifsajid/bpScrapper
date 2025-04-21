# Senate Election Results Scrapper

This Python script scrapes U.S. Senate election results from [Ballotpedia](https://ballotpedia.org) for a given year and a list of states. It uses Selenium to automate browser interaction and supports scraping data for both standard and special elections.

Note: It is always preferable to use Ballotpedia's official API, but this script does not require an API.

-----
## Features

- Scrapes Senate election results from Ballotpedia.
- Supports special election pages.
- Automatically formats and saves results into a CSV.
- Works for 2016 and 2018+ elections (adjusts based on year).
- Includes dynamic wait times between requests to avoid rate limiting.
-----

## Requirements

- Python 3.10+
- Google Chrome browser
- ChromeDriver (auto-installed via webdriver-manager)

## Getting Started 

Follow these steps to get the project up and running locally using venv and pip:

### a. Clone or Download the Repository

Download or clone this repository to your local machine:

```shell
git clone https://github.com/hanifsajid/bpScrapper.git
cd bpScrapper
```

### b. Create and Activate a Virtual Environment

```shell
python -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### c. Install Dependencites 

```shell
pip install -r requirements.txt
```

## Usage

Run the script:

```shell
python main.py \
  --year 2016 \
  --states_str "South Dakota, Utah, Vermont" \
  --output_dir "results" \
  --output_file "senate_2016_results.csv"
```
Example with default --output_dir, --output_file, and dot-separated states.

```shell
python main.py \
  --year 2018 \
  --states_str "Arizona • California • Connecticut" 
 ```
## Arguments 

Argument | Type | Required | Description
--year | int | \checkmark | Election year (e.g., 2020)
--states_str | string | \checkmark | Comma-separated (,) or dot-seprated (•) string of state names (as listed on Ballotpedia)
--output_dir | string | X | Directory to store CSV (default: scrapped_data)
--output_file | string | X | Output CSV file name with {year} placeholder (default: senate{year}.csv)

## Output

A CSV file with the following columns:

- year
- state
- candidate
- party
- writein_details
- vote_percentage
- votes
- winner
- incumbent
- bio_url
- additional_info

## License

This project is licensed under the MIT License.