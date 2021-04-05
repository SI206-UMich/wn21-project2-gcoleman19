from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest
#worked with: Zita Jameson, Blair Fields, Savy Dardashti

def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website)
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.
    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    f = open(filename, 'r')
    fileData = f.read()
    f.close()

    soup = BeautifulSoup(fileData, 'lxml')
    bookTitles = soup.find_all('a', class_='bookTitle')
    bookInfo = []
    for tag in bookTitles:
        bookInfo.append(tag.text.strip())

    authorsList = []
    authorTags = soup.find_all('div', class_='authorName__container')
    for item in authorTags:
        authorsList.append(item.text.strip())

    information = []
    for i in range(len(bookTitles)):
        tup = (bookInfo[i], authorsList[i])
        information.append(tup)
    return information


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:
    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]
    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to
    your list, and , and be sure to append the full path to the URL so that the url is in the format
    “https://www.goodreads.com/book/show/kdkd".
    """

    url_list = []
    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    anchor = soup.find_all('a', class_='bookTitle')
    for i in anchor:
        link = i['href']
        if link.startswith("/book/show/"):
            x = "https://www.goodreads.com" + str(link)
            url_list.append(x)
    return url_list[:10]


def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number
    of pages. This function should return a tuple in the following format:
    ('Some book title', 'the book's author', number of pages)
    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """
    
    r = requests.get(book_url)
    soup = BeautifulSoup(r.text, 'lxml')

    anchor = soup.find('h1', class_='gr-h1 gr-h1--serif')
    title = anchor.text.strip()

    anchor2 = soup.find('a', class_='authorName')
    author = anchor2.text.strip()

    anchor3 = soup.find('span', itemprop='numberOfPages')
    page_count = anchor3.text.strip(' pages')

    tup = (title, author, int(page_count))
    return tup

def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a
    filepath and return a list of (category, book title, URL) tuples.
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020")
    to your list of tuples.
    """
    catList = []
    bbList = []
    urlList = []
    tups = []

    source_dir = os.path.dirname(__file__)
    full_path = os.path.join(source_dir, filepath)
    infile = open(full_path,'r')

    re = infile.read()
    infile.close()

    soup = BeautifulSoup(re, 'html.parser')
    cat = soup.find_all("h4", class_ = 'category__copy')
    for category in cat:
        catList.append(category.text.strip())

    bb = soup.find_all('img', class_ = 'category__winnerImage')
    for book in bb:
        title = book['alt']
        bbList.append(title)

    urls = soup.find_all("div", class_ = "category clearFix")
    for url in urls:
        urlList.append(url.find('a')['href'])

    for i in range(len(urlList)):
        tup = (catList[i], bbList[i], urlList[i])
        tups.append(tup)
    return tups


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a
    csv file, and saves it to the passed filename.
    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.
    When you are done your CSV file should look like this:
    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......
    This function should not return anything.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Book title','Author Name'])
        for line in data:
            f.writerow(line)

def extra_credit(filepath):
     """
#     EXTRA CREDIT
#     Please see the instructions document for more information on how to complete this function.
#     You do not have to write test cases for this function.
#     """
     file1 = open(filepath, 'r')
     data = file1.read()
     file1.close()

     regex = r'\b[A-Z]\w.\w+(?:\s[A-Z]\w+)+'
     soup = BeautifulSoup(data, 'lxml')
     descriptions = soup.find('div', class_= 'readable stacked').find('span', id = 'freeText4791443123668479528').text

     entity = re.findall(regex, descriptions)
     return entity


class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        search_urls = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(search_urls), 20)
        # check that the variable you saved after calling the function is a list
        self.assertIsInstance(search_urls, list)
        # check that each item in the list is a tuple
        for x in search_urls:
            self.assertIsInstance(x, tuple)
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(search_urls[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(search_urls[-1][0], 'Harry Potter: The Prequel (Harry Potter, #0.5)')

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        search_urls = get_search_links()
        self.assertIsInstance(search_urls, list)
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(search_urls), 10)
        # check that each URL in the TestCases.search_urls is a string
        for x in search_urls:
            self.assertIsInstance(x, str)
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for x in search_urls:
            self.assertTrue("/book/show/" in x)

    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        # for each URL in TestCases.search_urls (should be a list of tuples)
        search_urls = get_search_links()
        summaries = []
        for x in search_urls:
            summaries.append(get_book_summary(x))
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for x in summaries:
            self.assertIsInstance(x,tuple)
            # check that each tuple has 3 elements
            self.assertEqual(len(x), 3)
            # check that the first two elements in the tuple are string
        self.assertIsInstance(summaries[0][0], str)
        self.assertIsInstance(summaries[0][1], str)
            # check that the third element in the tuple, i.e. pages is an int
        self.assertIsInstance(summaries[0][2], int)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)

    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable
        summarize = summarize_best_books("best_books_2020.htm")
        # check that we have the right number of best books (20)
        self.assertEqual(len(summarize), 20)
            # assert each item in the list of best books is a tuple
        for x in summarize:
            # check that each tuple has a length of 3
            self.assertEqual(type(x), tuple)
            self.assertEqual(len(x), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(summarize[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(summarize[-1], ('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        titles = get_titles_from_search_results('search_results.htm')
        # call write csv on the variable you saved and 'test.csv'
        write_csv(titles,'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        csv_lines = []
        with open('test.csv') as file:
            csv_f = csv.reader(file)
            for x in csv_f:
                csv_lines.append(x)

        # check that there are 21 lines in the csv
        self.assertEqual(len(csv_lines), 21)
        # check that the header row is correct
        self.assertEqual(csv_lines[0], ["Book title", "Author Name"])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(csv_lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'
        self.assertEqual(csv_lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'Julian Harrison (Introduction)'])

    def test_extra_credit(self):
         ex = extra_credit('extra_credit.htm')
         self.assertEqual(len(ex), 9)


if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)