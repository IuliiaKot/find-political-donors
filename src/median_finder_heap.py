import heapq


class MedianFinder():

    def __init__(self):
        self.lessheap = []
        self.moreheap = []

    def addNumber(self, value):
        # input: amount
        # add input amount to lessheap or moreheap base on comparising
        median = self.findMedian()

        if (value > median):
            heapq.heappush(self.lessheap, value)
        else:
            heapq.heappush(self.moreheap, -value)
        self.balanceHeap()


    def balanceHeap(self):
        # balance two heaps after addinf amout

        minSize = len(self.lessheap)
        maxSize = len(self.moreheap)
        current_value = 0

        if (minSize > maxSize + 1):
            current_value = heapq.heappop(self.lessheap)
            heapq.heappush(self.moreheap, -current_value)
        if (maxSize > minSize + 1):
            current_value = -heapq.heappop(self.moreheap)
            heapq.heappush(self.lessheap, current_value)



    def findMedian(self):
        # find the current median

        minSize = len(self.lessheap)
        maxSize = len(self.moreheap)

        if (minSize == 0 and maxSize == 0):
            return 0
        if minSize == maxSize:
            return int(round((self.lessheap[0] + (-self.moreheap[0]))/2.0))

        if (minSize > maxSize):
            return int(round(self.lessheap[0]))
        else:
            return int(round(-self.moreheap[0]))
