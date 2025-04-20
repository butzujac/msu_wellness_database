import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import spacy
from urllib.parse import urljoin, urlparse
import time
from openai import OpenAI

def generate_url_list(school_info, driver, max_links=20):
    """
    This function returns the subdomain links visible from a food bank or wellness programs homepage.
    Parameters:
        school_info: DataFrame with 'school_name' and 'url' columns
        max_links: max size of the list being returned for each school
    Returns:
        result_df: DataFrame with 'school_name' and 'url' columns
    """
    #Initialize all links to be collected
    all_links = []  

    for index, row in school_info.iterrows():
        #get school name and url to base/starting page
        school_name = row["school_name"] 
        url = row["url"]  
        driver.get(url)
        time.sleep(1)
        # parsing url to ensure consistency and proper formatting
        parsed_url = urlparse(url)
        #takes elements such as scheme and netloc to create valid base domain
        base_domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        # set data structure used to avoid duplicates
        links = set()
        #looping though each sublink
        for a in driver.find_elements(By.TAG_NAME, "a"):
            href = a.get_attribute("href")
            if href: # if link exists
                # joining to ensure only focused websites are being generated
                full_link = urljoin(base_domain, href)
                #adding to list of links if it has base domain 
                if full_link.startswith(base_domain) and full_link not in links:
                    links.add(full_link)
                    if len(links) >= max_links: #stopping point after max_links
                        break
        # all links for a school will have school name but different urls
        for link in links:
            all_links.append({"school_name": school_name, "url": link})
    # conver to dataframe 
    result_df = pd.DataFrame(all_links)

    return result_df


def clean_text(text):
    """Removes excessive spaces, newlines, and special characters from text."""
    return re.sub(r'\s+', ' ', text).strip()

#updated extraction function
def extract_relevant_text(url, keywords, driver):
    """
    This function Extracts relevant content and retrieves keyword occurrences with sentence context. it is the most important as it collects all data using beautifulsoup. 
    Parameters:
        url: the main page/subdomain of the unvieristy basic needs site
        keywords (list): list of keywords to search for in sites
        driver: chrome webdriver being used in scraping
    Returns: 
        extracted_info (Dataframe): single row of table, where columns are keywords and text inside is any matches, formatted. 
    """
    driver.get(url)
    #time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    text = clean_text(soup.get_text()) # can also use UniScraper here!
    extracted_info = {"URL": url, "Text": text}
    nlp = spacy.load("en_core_web_sm")
    # Process text with spaCy
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]  # Tokenize into sentences
    total_occurrences = []
    #loop through the keyword list
    for keyword in keywords:
        keyword_lower = keyword.lower()
        occurrences = []
        
        # Find occurences
        for i, sentence in enumerate(sentences):
            if keyword_lower in sentence.lower():  # If the keyword is found in the sentence
                before = sentences[i - 1] if i > 0 else " "  # Previous sentence
                after = sentences[i + 1] if i < len(sentences) - 1 else "N/A"  # Next sentence
                highlighted_sentence = sentence.replace(keyword, keyword.upper())
                occurrence_text = f"Occurrence X: {before} {highlighted_sentence} {after} \n"
                occurrences.append(occurrence_text)
                total_occurrences.append(occurrence_text)
            if len(total_occurrences) >= 5: # stopper if you find more than a reasonable amount of occurrences (prevents infinite/large loops)
                break
        # Placing the occurences into the same column separated by ||
        extracted_info[keyword] = "\n".join(occurrences) + "\n" + url if occurrences else "No"
        if len(total_occurrences) >= 5: # similar stopper logic, but for outer loop
            break

    return extracted_info


def extract_contact_info(text):
    """Extracts email and phone numbers from the scraped text."""
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return {"Emails": ", ".join(set(emails)), "Phone Numbers": ", ".join(set(phones))}


def merge_occurrences(series):
    """
    This function Merges occurrences from multiple sublinks, combining into a single row to capture all occurences of a given keyword across all sites for that school. 
    Parameters: 
        series (pandas series). Series of all occurences across a school, for a particular keyword
    Returns: 
        reordered (list) a list of reordered ocrruences, data to fill in a particular cell in the final table
    
    """
    unique_values = series.dropna().unique()
    filtered_values = [val for val in unique_values if val != "No"]

    if not filtered_values:
        return "No"

    # Step 1: Standardize occurrence format (replace numbers with 'X')
    occurrences = "\n".join(filtered_values)
    occurrence_list = [line for line in occurrences.split("\n") if line.strip()]

    # Step 3: Renumber properly
    reordered = []
    for i, occ in enumerate(occurrence_list):
        reordered.append(occ.replace("Occurrence X:", f"Occurrence {i + 1}:") + "\n")

    return "\n".join(reordered)


#Count total mentions per school
def count_mentions(series):
    """Count total keyword mentions across multiple rows for a school."""
    return series.str.count("Occurrence").sum()

def scrape_university_resources(school_info, keywords, driver, max_links=20, max_mentions_per_url=5):
    """
    Main function to scrape wellness resource mentions, contact info, and return a summarized dataframe.
    
    Parameters:
        school_info (DataFrame): DataFrame with 'school_name' and 'url' columns.
        max_links (int): Max number of sublinks to scrape per school.
        max_mentions_per_url (int): Max number of keyword occurrences per URL.
        
    Returns:
        DataFrame: Aggregated data with all keyword occurrences, contact info, and total mentions per school.
    """
    
    # Step 1: Generate relevant sub-URLs for each school
    result = generate_url_list(school_info, driver, max_links=20)

    
    data = []

    # Step 2: Scrape data from each sublink
    for url, school_name in zip(result["url"], result["school_name"]):
        try:
            extracted_data = extract_relevant_text(url, keywords=keywords, driver=driver) # for each link, extract keywords/nearby text
            contact_info = extract_contact_info(extracted_data["Text"]) 
            final_data = {**extracted_data, **contact_info, "school_name": school_name} # adding emails, phone numbers, to final data
            data.append(final_data)
        except Exception as e:
            print(f"Error scraping {url}: {e}")

    driver.quit()

    # Step 3: Convert to DataFrame and remove raw text
    df = pd.DataFrame(data)
    df.drop(columns=["Text"], inplace=True)

    # Step 4: Aggregate by school name, in order to ensure each school is a single row in the database
    agg_dict = {keyword: merge_occurrences for keyword in keywords}
    agg_dict["Emails"] = merge_occurrences
    agg_dict["Phone Numbers"] = merge_occurrences

    df_grouped = df.groupby("school_name").agg(agg_dict).reset_index()

    # Step 5: Total mentions
    df_grouped["Total Mentions"] = df[keywords].map(lambda x: x.count("Occurrence") if isinstance(x, str) else 0).groupby(df["school_name"]).sum().sum(axis=1).values

    return df_grouped


def clean_text_full(raw_text: str, keyword: str) -> str:
    """
    given a prompt, you can apply this function to any string text and return a cleaned version. see clean_database to see implementation
    Returns: 
        cleaned_text: answer from gpt-4o with cleaned text, according to this prompt and raw text
     """
    client = OpenAI(api_key="api-key-here") # paste your openAI api key into quotues of "api-key-here"
    prompt = f"""
    You are a data cleaner for a database on univerisity wellness initiatives. Each entry is associated with a **keyword**: "{keyword}".

    Your task is to clean the text below. Focus on:
    - Keeping only information **relevant to** "{keyword}", and keeping text which contains the exact match of the keyword
    - remove any occurrences that convey the same mesage or are repetitive
    - **Removing duplicates**, verbose language, or vague phrases
    - Returning an **organized summary** for each useful occurrence
    - make sure not to add any additonal insights or infomration from the raw text, only add text to ensure proper grammar
    - keeping the same format it was orgionally in. make sure to have it in paragraph form, and the links below the occurrence if applicable. 
    - renumber occurrences, make sure each one starts with "Occurrence (number)"
    - if none of the text is relevant to "{keyword}", simply return "no"
    Text to clean:
    \"\"\"
    {raw_text}
    \"\"\"
    return: **only** the cleaned text with no extra charecters
    """ # you can use prompt engineering to get this even more effective! - currenly using RAG to improve preformance
    try:
        response = client.responses.create(
        model="gpt-4o",
        input=prompt )
        cleaned_text = response.output_text # this is the answer from gpt-40, aka the cleaned text
        return cleaned_text
    except Exception as e:
        print(f"Error during OpenAI call: {e}")
        return None

def clean_database(data):
    """
    This function applies clean_text to each cell in the dataframe with keyword matches. 

    parameters: 
        data (pandas dataframe): the data to be cleaned
    returns:
        data (pandas dataframe): cleaned database
    """
    cols = data.columns.tolist()
    remove_items = ["school_name", "Emails", "Phone Numbers", "Total Mentions"] # only looping through columns that are keywords
    cols_to_clean = [item for item in cols if item not in remove_items]
    for col in cols_to_clean:
        data.loc[:,col] = data[col].apply(lambda val: clean_text_full(val, col)) # for each keyword column in the dataframe, apply the clean text to each cell
    # recount occurrences in total mentions column, as gpt-4o may have gotten rid of occurences
    data["Total Mentions"] = data.astype(str).apply(lambda row: row.str.count("Occurrence").sum(), axis=1) 
    return data


def add_new_keyword(existing_database, school_info, keyword, driver):
    """ 
    this funciton adds a new keyowrd(column to the database)

    parameters:
        - existing_database (pandas dataframe): dataframe before
        - school_info ()
    returns: 
        - result_df(pandas dataframe): dataframe with new keyword for all schools
    """
    new_keyword = scrape_university_resources(school_info=school_info, keywords=keyword, driver=driver) # scrappes for new keyword
    result_df = existing_database.merge(new_keyword[['school_name', keyword[0]]], on='school_name', how='left') # merges only the new keyword into the dataframe
    # logic to insert new keyword before emails to keep strucured 
    cols = result_df.columns.tolist() 
    cols.remove(keyword[0])
    value_index = cols.index('Emails') 
    cols.insert(value_index, keyword[0])
    result_df = result_df[cols]
    return result_df


def add_new_school(existing_database, school_info, driver):
    """
    this funciton adds a new school to the database. 

    parameters:
        existing_database(pandas dataframe): database before
        school_info (dataframe): school information (name and )
    """
    ## gathering keywords for new school
    cols = existing_database.columns.tolist()
    remove_items = ["school_name", "Emails", "Phone Numbers", "Total Mentions"]
    keywords = [item for item in cols if item not in remove_items]
    new_school = scrape_university_resources(school_info, keywords=keywords, driver=driver) # scrapes for only one school rather than all
    new_data = pd.concat([existing_database, new_school], ignore_index=True) # adds to the bottom
    return new_data