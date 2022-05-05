class Node:
    def __init__(self, data):
        self.__prev = None
        self.__next = None
        self.__data = data

    def __repr__(self):
        return f'<{self.__data}>'

    def __str__(self):
        return f'{self.__data}'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.data == other.data
        else:
            return self.data == other

    @property
    def prev(self):
        return self.__prev

    @prev.setter
    def prev(self, prev):
        self.__prev = prev

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, next):
        self.__next = next

    @property
    def data(self):
        return self.__data


class DLL:
    class __DLLIterator:
        def __init__(self, hd: Node | None):
            self.curr = hd

        def __iter__(self):
            return self

        def __next__(self):
            if not self.curr:
                raise StopIteration
            else:
                item = self.curr.data
                self.curr = self.curr.next
                return item

    def __init__(self):
        self.__hd: Node | None = None
        self.__tl: Node | None = None
        self.__size: int = 0

    def __len__(self):
        return self.__size

    def __iter__(self):
        return DLL.__DLLIterator(self.__hd)

    def __contains__(self, other):
        for node in self:
            if node == other:
                return True
        return False

    def append(self, data):
        new_node = Node(data)
        if self.__tl:
            self.__tl.next = new_node
            new_node.prev = self.__tl
        else:
            self.__hd = new_node
        self.__tl = new_node
        self.__size += 1

    def remove(self, data):
        curr = self.__hd
        while curr and curr.next and curr != data:
            curr = curr.next
        if curr == data:
            if curr == self.__hd and curr == self.__tl:
                self.__hd = self.__tl = None
            elif curr == self.__hd and curr != self.__tl:
                self.__hd = curr.next
                curr.next.prev = None
            elif curr != self.__hd and curr == self.__tl:
                self.__tl = curr.prev
                curr.prev.next = None
            else:
                curr.prev.next = curr.next
                curr.next.prev = curr.prev
        else:
            raise ValueError(f'{data} not found')

    def search(self, data):
        curr = self.__hd
        while curr and curr.next and curr != data:
            curr = curr.next
        if curr == data:
            return curr
        raise ValueError(f'{data} not found')
