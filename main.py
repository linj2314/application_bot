from package import *

def main():
    scrape_links()
    f = open("links.txt", "r")
    links = f.readlines()
    for link in links:
        try:
            if re.search("myworkdayjobs.com", link):
                workday(link)
            elif re.search("jobs.lever.co", link):
                lever(link)
            elif re.search("boards.greenhouse.io", link):
                greenhouse(link)
        except ExpiredApplicationError as e:
            print(e.message)
            continue

if __name__ == "__main__":
    main()