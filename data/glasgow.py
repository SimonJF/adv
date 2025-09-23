#!/usr/bin/env python3
# Scrapes UofG pages
from bs4 import BeautifulSoup
import json
import requests
import os
from itertools import takewhile

CATALOGUE_URL = "https://www.gla.ac.uk/coursecatalogue/courselist/?code=REG30200000"

# Strip annoying unicode characters that creep in
def strip_unicode(inp):
    return inp.encode('ascii', 'ignore').decode()

def scrape_catalogue(url):
    response = requests.get(url)
    html = response.text

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find all course list items
    course_list_items = soup.find('main').find_all('li')

    # Extract course details
    courses = []
    for item in course_list_items:
        course_name = item.find('a').text.strip()
        course_code = item.find('span').text.strip()
        course_url = item.find('a')['href']
        courses.append({
            'name': course_name,
            'course_code': course_code,
            'url': 'https://www.gla.ac.uk' + course_url
        })

    # Convert to JSON
    # courses_json = json.dumps(courses, indent=2)
    return courses

def scrape_course_page(url):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser').find('main')

    course_details = {
        "name": "",
        "course_code": "",
        "semester": "",
        "aims": "",
        "ilos": "",
        "credits": 0,
        "aliases": []
    }

    # Extract course name
    course_name_tag = soup.find('h2')
    name = ""
    if course_name_tag:
        name = course_name_tag.get_text(strip=True)
        print(f"Scraping: {name}")
        name_contents = strip_unicode(name)
        name_split = name_contents.split(' ')
        name = " ".join(name_split[:-1])
        code = name_split[-1]
        course_details["name"] = name
        course_details["course_code"] = code

    # Extract course code
    #course_code_tag = soup.find('a', href=True)
   # if course_code_tag:
    #    course_details["course_code"] = strip_unicode(course_code_tag['href'].split('=')[-1])

    # Extract credits
    credits_strong_tag = soup.find('strong', string='Credits:')
    if credits_strong_tag and credits_strong_tag.parent.name == 'li':
        credits_tag = credits_strong_tag.parent
        course_details["credits"] = int(strip_unicode(credits_tag.get_text(strip=True).split(':')[1]))


    # Extract semester
    semester_strong_tag = soup.find('strong', string='Typically Offered:')
    if semester_strong_tag and semester_strong_tag.parent.name == 'li':
        semester_tag = semester_strong_tag.parent
        course_details["semester"] = strip_unicode(semester_tag.get_text(strip=True).split(':')[1])

    # Extract aims
    aims_tag = soup.find('h3', string='Course Aims').find_next('div')
    if aims_tag:
        course_details["aims"] = strip_unicode(aims_tag.get_text(strip=True))

    # Extract intended learning outcomes
    ilos_tag = soup.find('h3', string='Intended Learning Outcomes of Course').find_next('div')
    if ilos_tag:
        course_details["ilos"] = strip_unicode(ilos_tag.get_text(strip=True))

    course_details["aliases"] = gen_aliases(name)

    # Convert to JSON
    # json_output = json.dumps(course_details, indent=2)
    return course_details
    #print(json_output)

def discard_descriptors(name):
    name = name.split(':')[0]
    return name.split(' - ')[0]

# Approximation of common aliases
def gen_aliases(course_name):
    course_name = course_name.lower()
    # First-year courses and a few others are hard-coded
    if "1ct" in course_name:
        return ["cs1ct", "1ct"]
    elif "1s" in course_name:
        return ["cs1s", "1s"]
    elif "1px" in course_name:
        return ["cs1px", "1px"]
    elif "1p" in course_name:
        return ["cs1p", "1p"]
    elif "algorithmics i" in course_name:
        return ["alg1"]
    elif "algorithmics ii" in course_name:
        return ["alg2"]

    # Otherwise discard descriptors
    course_name = discard_descriptors(course_name)
    # Tokenise
    split_name = course_name.split(' ')
    # Filter 'and', 'for', 'in', and '(H)' / '(M)'
    filtered_name = [word for word in split_name if \
                     word not in ['and', 'for', 'in'] and len(word) > 0 \
                     and word != "&" and word != "(h)" and word != "h" \
                     and word != "(m)" and word != "m" and word != "msc"]
    # Return singleton list containing first word of each
    return ["".join([word[0] for word in filtered_name])]



def scrape():
    output = [ scrape_course_page(course['url']) for course in \
               scrape_catalogue(CATALOGUE_URL) ]
    #output = scrape_course_page(scrape_catalogue(CATALOGUE_URL)[0]['url'])
    #print(output)
    with open(os.path.join('glasgow.json'), 'w') as f:
        f.write(json.dumps(output, indent=True))

## TEMP
def main():
    #print(scrape_catalogue(CATALOGUE_URL))
    scrape()

if __name__ == "__main__":
    main()
