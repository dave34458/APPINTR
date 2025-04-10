# Book
Fields: id, title, author, published_date, isbn
Routes:
  GET/POST           /books
  GET/PUT/PATCH/DELETE /books/{book_id}

# AvailableBook
Fields: id, book (FK), location, is_available
Routes:
  GET/POST           /books/{book_pk}/availablebooks
  GET/PUT/PATCH/DELETE /books/{book_pk}/availablebooks/{id}

# Borrow
Fields: id, available_book (FK), user (FK), borrow_date, return_date
Routes:
  GET/POST           /books/{book_pk}/availablebooks/{available_book_pk}/borrows
  GET/PUT/PATCH/DELETE /books/{book_pk}/availablebooks/{available_book_pk}/borrows/{id}

# Review
Fields: id, book (FK), user (FK), rating, comment
Routes:
  GET/POST           /books/{book_pk}/reviews
  GET/PUT/PATCH/DELETE /books/{book_pk}/reviews/{id}
