#include <iostream>
#include <vector>
#include <ctime>

using namespace std;

void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<int> leftArr(n1);
    vector<int> rightArr(n2);

    for (int i = 0; i < n1; ++i)
        leftArr[i] = arr[left + i];
    for (int j = 0; j < n2; ++j)
        rightArr[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;

    while (i < n1 && j < n2) {
        if (leftArr[i] <= rightArr[j])
            arr[k++] = leftArr[i++];
        else
            arr[k++] = rightArr[j++];
    }

    while (i < n1)
        arr[k++] = leftArr[i++];
    while (j < n2)
        arr[k++] = rightArr[j++];
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left >= right)
        return;

    int mid = left + (right - left) / 2;
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);
    merge(arr, left, mid, right);
}

int main() {
    int n;
    if (!(cin >> n)) {
        cerr << "No input provided." << endl;
        return 0;
    }

    vector<int> arr(n);
    for (int i = 0; i < n; ++i)
        cin >> arr[i];

    clock_t start = clock();
    mergeSort(arr, 0, n - 1);
    double timeTaken = double(clock() - start) / CLOCKS_PER_SEC;

    cout << "Time taken: " << timeTaken << " seconds" << endl;
    cout << "First 10 elements of sorted array:";
    for (int i = 0; i < min(n, 10); ++i)
        cout << " " << arr[i];
    cout << endl;

    return 0;
}
