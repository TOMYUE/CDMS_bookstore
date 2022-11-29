book_relation_oldname = "main.book"
book_relation_newname = "Book_bp"

with open("book.sql", "r+") as f:
    s = f.read()
    s = s.replace(book_relation_oldname, "\""+book_relation_newname+"\"")

with open("book.sql", "w+") as f:
    f.write(s)
