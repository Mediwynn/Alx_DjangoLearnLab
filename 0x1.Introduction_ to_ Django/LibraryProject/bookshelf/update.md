book = Book.objects.get(id=1) 
book.title= "Nineteen Eighty-Four"
book.save()

# retrieve book attributes,
# rename title from "1984" to "Nineteen Eighty-Four"
# then save changes