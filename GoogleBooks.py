import requests
import pandas as pd
import csv


pd.set_option('display.float_format', lambda x: '%.5f' % x) #Preventing scientific notation of ISBNs
numBooks = 30000 #How many ISBNS should be read. Due to duplicates and google books not having certain books, about 2.5% of this number is actually collected.

#Read ISBNS, convert to list
data = pd.read_csv('textbook_data.csv', nrows=numBooks, usecols=["ISBN"])
isbnList = data.values.tolist()
print("Initial Length: " + str(len(isbnList)))

#Filter out duplicates and NaNs
res = []
[res.append(x) for x in isbnList if x not in res]
isbnList = []
[isbnList.append(int(x[0])) for x in res if not pd.isna(x[0])]
res = []

print("Filtered Length: " + str(len(isbnList)))
print("=====Filtering Complete=====")


header = ["title", "description", "authors", "publisher", "publishDate", "pageCount", "categories", "language", "smallThumbnail", "thumbnail", "isbn13", "isbn10"]
bookCSVData = []

for isbn in isbnList:
    try:
        r = requests.get("https://www.googleapis.com/books/v1/volumes?q=isbn:{0}".format(isbn))
        if(r.json()['totalItems']):
            book = r.json()['items'][0]

            title = book['volumeInfo']['title']
            authors = book['volumeInfo']['authors']
            description = book['volumeInfo']['description']
            pageCount = book['volumeInfo']['pageCount']
            categories = book['volumeInfo']['categories']
            publishDate = book['volumeInfo']['publishedDate']
            publisher = book['volumeInfo']['publisher']
            language = book['volumeInfo']['language']
            smallThumbnail = book['volumeInfo']['imageLinks']['smallThumbnail']
            thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
            isbn13 = book['volumeInfo']['industryIdentifiers'][0]["identifier"]
            isbn10 = book['volumeInfo']['industryIdentifiers'][1]["identifier"]

            bookCSVData.append([title, description, authors, publisher, publishDate, pageCount, categories, language, smallThumbnail, thumbnail, isbn13, isbn10])
    except: 
        pass
print ("Books Collected: " + str(len(bookCSVData)))
print("=====Data Collection Complete=====")

open('books.csv', 'w').close() #precaution to clear previous data
with open('books.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    for row in bookCSVData:
        writer.writerow(row)

print("=====Write Complete=====")