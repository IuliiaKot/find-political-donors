
class MedianFinder():

    def __init__(self):
        self.all_amounts = []

    def addNumber(self, value):

        if len(self.all_amounts) == 0:
            self.all_amounts.append(value)
        else:
            postition = self.searchInsert(value)
            self.all_amounts.insert(postition, value)

    def searchInsert(self, value):
        # binart search insert

        n = len(self.all_amounts)
        low = 0
        high = n - 1
        while low <= high:
            mid = (low + high)/2
            if self.all_amounts[mid] == value:
                return mid
            elif self.all_amounts[mid] < value:
                low = mid + 1
            else:
                high = mid - 1
        return low


    def findMedian(self):
        # find median

        count = len(self.all_amounts)
        if len(self.all_amounts) % 2 == 0:
            rmedian = (self.all_amounts[count/2]  + self.all_amounts[count/2 - 1])/2
        else:
            rmedian = self.all_amounts[count/2]
        return int(round(rmedian))
