from bs4 import BeautifulSoup
from glob import iglob

# Returns documents with newid and content from each article in reuters collection
def getDocuments():
    reuter_files = []
    documents = {}

    # Go through each reuter file and add to the reuter files list
    for pathname in iglob('reuters21578/reut2-*.sgm'):
        reuter_files.append(pathname)

    # Go through each file in list
    # Use BeautifulSoup to extract the newid and content for each article in file
    # Add newid and content to documents dictionary
    for file in reuter_files:
        with open(file,'r+') as f:
            contents = f.read()
            soup = BeautifulSoup(contents, "html.parser")
            articles = soup.find_all('reuters')

            for article in articles:
                title = ""
                body = ""
                newid = int(article['newid'])
                if not article.title is None:
                    title = article.title.string
                if not article.body is None:
                    body = article.body.string
                words = title + " " + body
                documents[newid] = words
    print("Documents from Reuteurs Collection have been generated.")
    return documents






