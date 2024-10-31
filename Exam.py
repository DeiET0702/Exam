import os
import re
import subprocess
import requests
import html
import argparse

path = './exploit-db'
#create path if it haven't existed.
if not os.path.exists(path):
    os.makedirs(path)

#--exploit
def exploit_func(id_input):
    #Check input using regex
    pattern_match = re.match(r'(?:https://www.exploit-db.com/exploits/)?(\d+)', id_input)
    #Get id from input
    if pattern_match:
        id = pattern_match.group(1)
    else:
        print("Invalid ID!")
        return
    #create file_path name
    exploit_file_path = os.path.join(path, f"{id}.txt")
    #checking file_path exists
    if os.path.exists(exploit_file_path):
        subprocess.run(["open", exploit_file_path])
    else:
        try:
            #scrapt data from exploit-db.com
            url = 'https://exploit-db.com/exploits/{}'.format(id)
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            res = requests.get(url, headers = headers)
            exploit = res.text[res.text.find('<code') : res.text.find('</code>')]
            exploit = html.unescape(exploit[exploit.find('">') +2 :])
            with open(exploit_file_path, 'w', encoding='utf-8') as file:
                file.write(exploit)
            subprocess.run(["open", exploit_file_path])
        except Exception as e:
            print("An error occurred: ", e)

#--page
def page_func(page):
    page_number = int(page)
    #return all sorted .txt file
    exploits = sorted(os.listdir(path), key = lambda x: int(x.split('.')[0]))
    #each page has 5 files. Return list exploit_file of a page
    start = page_number*5
    end = start+5
    files_page = exploits[start:end]
    #print files of page
    if files_page:
        for i in files_page:
            print(i.split('.')[0])
    else:
        print("No exploits found on this page!")

def search_func(key):
    key_pattern = r'\b(?:' + '|'.join(key.split()) + r')\b'
    #list-file has key search
    key_files = [] 
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        with open(file_path, 'r', encoding='utf-8') as file:
            content_file = file.read()
            if re.search(key_pattern, content_file, re.IGNORECASE):
                key_files.append(file_path)
    
    if key_files:
        for i in key_files:
            print(i)
    else:
        print("No exploits found!")

def main():
    #initialzie parser
    parser = argparse.ArgumentParser(description='Python Exam')
    #add optional arguments
    parser.add_argument('--exploit', help='exploit ID', type=str)
    parser.add_argument('--page', help='get page', type=int)
    parser.add_argument('--search', help='Search keyword', type=str)
    #parse argument
    args = parser.parse_args()
    #func
    if args.exploit:
        exploit_func(args.exploit)
    elif args.page is not None:
        page_func(args.page)
    elif args.search:
        search_func(args.search)
    else:
        parser.print_help()

if __name__ == "__main__":
        try:
            main()
        except Exception as e:
            print("An error occurred: ", e)










            


