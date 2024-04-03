def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
        print(f"Iteration {i + 1}: {arr}")

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >=0 and key < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
        arr[j+1] = key
        print(f"Iteration {i}: {arr}")

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        print(f"Iteration {i + 1}: {arr}")

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    sorted_arr = quick_sort(left) + middle + quick_sort(right)
    print(f"Sorted array: {sorted_arr}")
    return sorted_arr

def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and arr[l] > arr[largest]:
        largest = l

    if r < n and arr[r] > arr[largest]:
        largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)

    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
        print(f"Iteration {n - i}: {arr}")

def counting_sort(arr):
    max_element = max(arr)
    min_element = min(arr)
    range_of_elements = max_element - min_element + 1
    count_arr = [0 for _ in range(range_of_elements)]
    output_arr = [0 for _ in range(len(arr))]

    for i in range(len(arr)):
        count_arr[arr[i] - min_element] += 1

    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        output_arr[count_arr[arr[i] - min_element] - 1] = arr[i]
        count_arr[arr[i] - min_element] -= 1

    for i in range(len(arr)):
        arr[i] = output_arr[i]
    print(f"Sorted array: {arr}")

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
        print(f"Sorted array: {arr}")

def shell_sort(arr):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
        print(f"Iteration: {arr}")

def print_menu():
    print("Please select a sorting algorithm:")
    print("1. Bubble Sort")
    print("2. Insertion Sort")
    print("3. Selection Sort")
    print("4. Quick Sort")
    print("5. Heap Sort")
    print("6. Counting Sort")
    print("7. Merge Sort")
    print("8. Shell Sort")

def get_choice():
    choice = int(input("Enter your choice: "))
    return choice

def main():
    while True:
        arr = list(map(int, input("Please enter your array in format num1 num2 num3 ... - ").split()))
        print("Original array:", arr)
        print_menu()
        choice = get_choice()
        if choice == 1:
            bubble_sort(arr)
        elif choice == 2:
            insertion_sort(arr)
        elif choice == 3:
            selection_sort(arr)
        elif choice == 4:
            arr = quick_sort(arr)
        elif choice == 5:
            heap_sort(arr)
        elif choice == 6:
            counting_sort(arr)
        elif choice == 7:
            merge_sort(arr)
        elif choice == 8:
            shell_sort(arr)
        else:
            print("Invalid choice!")
        
        sort_again = input("Do you want to sort again? (Y/N): ")
        if sort_again.lower() == 'n':
            break

if __name__ == "__main__":
    main()
