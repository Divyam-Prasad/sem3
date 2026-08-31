# Recursive Quick Sort Approach
# This is not an in-place sorting algorithm. It takes space complexity :- O(n)  
# The Time Complexity for this approach is O(nlogn) and worst case O(n^2) is when the splitting is always 1 and n-1


nums = [5,2,6,4,3,3,1,3,7]
def quickSort(nums):
    if len(nums) == 1 or len(nums) == 0:
        return nums
    pivot = nums[0]
    i = 0 
    j = len(nums) - 1
    left = []
    right = []
    for i in range(1,len(nums)):
        if pivot >= nums[i]:
            left.append(nums[i])

        elif pivot < nums[i]:
            right.append(nums[i])

    return quickSort(left) + [pivot] + quickSort(right)

print(quickSort(nums))