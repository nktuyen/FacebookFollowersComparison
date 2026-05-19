import os
import sys
import json
import re
import optparse
from bs4 import BeautifulSoup

if __name__=="__main__":
    parser: optparse.OptionParser = optparse.OptionParser('%prog [options] following_file follower_file')
    parser.add_option('-v', '--verbose', action='store_false', help='Verbose')
    parser.add_option('-o', '--out', default='out.html', help='Output HTML file. Default is out.html')
    parser.add_option('-n', '--number', default=None, help='Start number. Default is 1')
    
    opts, args = parser.parse_args()
    if len(args) <= 0:
        print(f"Error:There is no any link/url specified")
        sys.exit(1)
    if len(args) < 2:
        print(f"Error:Two link2/urls must be specified")
        sys.exit(1)
    
    url1: str = args[0]
    url2: str = args[1]

    if not os.path.exists(url1):
        print(f"{url1} is not exist or valid")
        sys.exit(1)
    if not os.path.exists(url2):
        print(f"{url2} is not exist or valid")
        sys.exit(1)
    
    html1: str = ""
    json1 = None
    try:
        with open(url1, 'r', encoding='utf-8') as file1:
            if url1.lower().endswith(".html"):
                html1 = file1.read()
            elif url1.lower().endswith(".json"):
                json1 = json.load(file1)
    except Exception as ex1:
        print(f"Exception:{ex1}")
        sys.exit(1)
    
    html2: str = ""
    json2 = None
    try:
        with open(url2, 'r', encoding='utf-8') as file2:
            if url2.lower().endswith(".html"):
                html2 = file2.read()
            elif url2.lower().endswith(".json"):
                json2 = json.load(file2)
    except Exception as ex2:
        print(f"Exception:{ex2}")
        sys.exit(1)

    followers_map1: dict = {}
    followers_map2: dict = {}
    
    pattern = r"\\u[0-9a-fA-F]{4}"
    #Who you're followed
    name: str = ""
    if url1.lower().endswith(".html"):
        soup1 = BeautifulSoup(html1, 'lxml')
        title1 = soup1.title.string
        print(f"Processing {title1}...")
        followers_tags = soup1.find_all('h2', class_='_2ph_ _a6-h _a6-i')
        for index, person in enumerate(followers_tags, 1):
            name = person.get_text().strip()
            if name not in followers_map1:
                followers_map1[name] = 1
            else:
                followers_map1[name] += 1
    elif url1.lower().endswith(".json"):
        key1: str = "following_v3"
        if key1 in json1:
            title1 = key1[:9]
            print(f"Processing {title1}...")
            peoples: list = json1[key1]
            people: dict = None
            for people in peoples:
                if "name" in people:
                    name = people["name"].strip()
                    try:
                        name = name.encode("latin1").decode("utf-8")
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        pass
                    if name not in followers_map1:
                        followers_map1[name] = 1
                    else:
                        followers_map1[name] += 1
    

    # People who followed you
    if url2.lower().endswith(".html"):
        soup2 = BeautifulSoup(html2, 'lxml')
        title2 = soup2.title.string
        print(f"Processing {title2}...")
        followers_tags = soup2.find_all('h2', class_='_2ph_ _a6-h')
        for index, person in enumerate(followers_tags, 1):
            name = person.get_text().strip()
            if name not in followers_map2:
                followers_map2[name] = 1
            else:
                followers_map2[name] += 1
    elif url2.lower().endswith(".json"):
        key2: str = "followers_v3"
        if key2 in json2:
            title2 = key2[:9]
            print(f"Processing {title2}...")
            peoples: list = json2[key2]
            people: dict = None
            for people in peoples:
                if "name" in people:
                    name = people["name"].strip()
                    try:
                        name = name.encode("latin1").decode("utf-8")
                    except (UnicodeEncodeError, UnicodeDecodeError):
                        pass
                    if name not in followers_map2:
                        followers_map2[name] = 1
                    else:
                        followers_map2[name] += 1

    #Generate report file
    out_file: str = opts.out
    index: int = 0
    verbose: bool = True if opts.verbose is not None else False
    start_index: int = 1
    if opts.number is not None:
        try:
            start_index = int(opts.number)
        except:
            start_index = 1

    with open(out_file, 'w', encoding='utf-8') as report_file:
        report_file.write("<html><heade><title>Report</title></head><body><table style='border:solid 1px gray;'><caption><h1>Report</h1></caption><tr><th>#</th><th>Who you're followed</th><th>Did he/she follow you?</th></tr>")
        if verbose:
            for _, name in enumerate(followers_map1, 1):
                if name in followers_map2:
                    index += 1
                    if index >= start_index:
                        report_file.write(f"<tr><td style='border-top:solid 1px gray;'>{index}</td><td style='border-top:solid 1px gray;;border-left:solid 1px gray;'>{name}</td><td style='border-top:solid 1px gray;border-left:solid 1px gray;'>")
                        count = followers_map2[name]
                        while count > 0:
                            report_file.write(f"<span style='display:block'>{name}</span>")
                            count -= 1
                        report_file.write("</td></tr>")
        for _, name in enumerate(followers_map1, 1):
            if name not in followers_map2:
                index += 1
                if index >= start_index:
                    report_file.write(f"<tr><td style='border-top:solid 1px gray;color:red;'>{index}</td><td style='border-top:solid 1px gray;;border-left:solid 1px gray;color:red;'>{name}</td><td style='border-top:solid 1px gray;border-left:solid 1px gray;color:red;'>")
                    report_file.write("</td></tr>")
        report_file.write("</table></body></html>")
    
