def calculate_sum(arr):
    return sum(arr)

def main():
    size = int(input("Enter the size of the array: "))
    arr = []

    print(f"Enter {size} integers:")
    for _ in range(size):
        arr.append(int(input()))

    sum_ = calculate_sum(arr)
    
    print(f"The sum of the array is: {sum_}")

    if sum_ % 2 == 0:
        print("The sum is even.")
    else:
        print("The sum is odd.")

if __name__ == "__main__":
    main()
