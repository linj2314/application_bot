from package import *
import cProfile
import pstats

def main():
    scrape_links()
    f = open("links.txt", "r")
    links = f.readlines()
    f1 = open("application_count.txt", "rw")
    f2 = open("not_applied_to.txt", "w")
    num_applied = int(f.read())
    
    for link in links:
        try:
            if re.search("myworkdayjobs.com", link):
                ret = workday(link)
            elif re.search("jobs.lever.co", link):
                ret = lever(link)
            elif re.search("boards.greenhouse.io", link):
                ret = greenhouse(link)
            else:
                f2.write(link)
                continue

            if ret == 0:
                #successful application
                num_applied += 1
            elif ret == 1:
                #not successful; add to list of unapplied applications
                f2.write(link)
            elif ret == 2:
                #application already submitted; do nothing
                pass

        except ExpiredApplicationError as e:
            print(e.message)
            continue

    f1.write(num_applied)
    f1.close()
    f2.close()

if __name__ == "__main__":
    f = open("application_count.txt", "rw")
    n = int(f.read())
    f.write(n + 1)
    f.close()
