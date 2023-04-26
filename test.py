class Book:
    def __init__(self, title: str, author: str, pages: int, year: int):
    #def __init__(self, title, author, pages, year):
        self.title = title
        self.author = author
        self.pages = pages
        self.year = year


class DigitBook(Book):
    def __init__(self, title, author, pages, year, size, frm):
        super().__init__(title, author, pages, year)
        self.size = size
        if frm in ('pdf', 'doc', 'fb2', 'txt'):
            self.frm = frm


book = Book('Oz', 'NN', '172', 34)
db = DigitBook(title, author, pages, year, size, frm)