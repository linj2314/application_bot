from package import *

def main():
    scrape_links()
    f = open("links.txt", "r")
    links = f.readlines()
    f1 = open("application_count.txt", "r+")
    f2 = open("not_applied_to.txt", "a")
    num_applied = int(f1.read())
    
    for link in links:
        try:
            if re.search("myworkdayjobs.com", link):
                ret = workday(link)
            elif re.search("jobs.lever.co", link):
                ret = lever(link)
            elif re.search("boards.greenhouse.io", link):
                ret = greenhouse(link)
            else:
                f2.write(link + "\n")
                continue

            if ret == 0:
                #successful application
                print("Applied!")
                num_applied += 1
            elif ret == 1:
                #not successful; add to list of unapplied applications
                print("Unsuccesful")
                f2.write(link + "\n")
            elif ret == 2:
                #do nothing
                print("Already Applied/Expired Application")
                pass

        except Exception as e:
            print(e.message)
            continue

    f1.seek(0)
    f1.write(str(num_applied))
    f1.truncate()
    f1.close()
    f2.close()

if __name__ == "__main__":
    main()
