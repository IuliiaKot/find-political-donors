class Contributions():
    def __init__(self, median, amt, heap):
        self.median = median
        self.count = 1
        self.total_amt = amt
        self.heap_obj = heap
