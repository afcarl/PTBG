__author__ = 'luocheng'

class Object:
    def __init__(self):
        pass
    def binary_search(self,seq,key):
        def search(low,high):
            if low == high:
                if seq[low] == key:
                    return low
                else:
                    return -1
            else:
                mid = low+(high - low)/2
                if seq[mid] == key:
                    return mid
                if seq[mid] < key:
                    return search(mid,high)
                if seq[mid] > key:
                    return search(low,mid)
        return search(0,len(seq)-1)

obj = Object()
print obj.binary_search([1,2,3,4,5,6,7,8],6)