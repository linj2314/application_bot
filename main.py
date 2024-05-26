from imports import *
from utilities import *
from workday import workday
from lever import lever
from greenhouse import greenhouse

def main():
    scrape_links()
    f = open("links.txt", "r")
    links = f.readlines()
    for link in links:
        if re.search("myworkdayjobs.com", link):
            workday(link)
        elif re.search("jobs.lever.co", link):
            lever(link)
        elif re.search("boards.greenhouse.io", link):
            greenhouse(link)

if __name__ == "__main__":
    main()