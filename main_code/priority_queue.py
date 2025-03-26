class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.append(item)
        index = len(self.items) - 1
        while index > 0 and self.items[index][1] < self.items[index - 1][1]:
            self.items[index], self.items[index - 1] = self.items[index - 1], self.items[index]
            index -= 1

    def dequeue(self):
        if len(self.items) > 0:
            return self.items.pop(0)

        else:
            return "Queue empty"

    def size(self):
        return len(self.items)

    def show(self):
        return self.items

    def show_front(self):
        return self.items[0]
