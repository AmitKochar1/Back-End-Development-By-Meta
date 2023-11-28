# Define class MyFirstClass
class MyFirstClass:
    print('Who wrote this?')
    index = "Author-Book"

    def hand_list(self, philosopher, book):
        self.philosopher = philosopher
        self.book = book
        #print(MyFirstClass.index)
        print(self.philosopher + ' wrote the book: '  + self.book)


# Call function handlist()
whodunnit = MyFirstClass()

whodunnit.hand_list('amit', 'the life')