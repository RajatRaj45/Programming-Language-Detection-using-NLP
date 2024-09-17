#include <iostream>
using namespace std;

int calculateSum(int arr[], int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}

int main() {
    int size;
    cout << "Enter the size of the array: ";
    cin >> size;

    int arr[size];

    cout << "Enter " << size << " integers:\n";
    for (int i = 0; i < size; i++) {
        cin >> arr[i];
    }

    int sum = calculateSum(arr, size);
    
    cout << "The sum of the array is: " << sum << endl;

    if (sum % 2 == 0) {
        cout << "The sum is even." << endl;
    } else {
        cout << "The sum is odd." << endl;
    }

    return 0;
}
