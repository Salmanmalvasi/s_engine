#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime>

using namespace std;

// Rod Cutting using Dynamic Programming (Bottom-Up)
// Time Complexity: O(n^2)
int rodCutting(int n, const vector<int>& prices) {
    // dp[i] stores the maximum revenue for a rod of length i
    vector<int> dp(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        int max_val = -1;
        // Try all possible cuts
        // prices[j] is the price of a piece of length j+1
        for (int j = 0; j < i; j++) {
            max_val = max(max_val, prices[j] + dp[i - j - 1]);
        }
        dp[i] = max_val;
    }

    return dp[n];
}

int main() {
    int n;
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    if (!(cin >> n)) return 0;

    vector<int> prices(n);
    for (int i = 0; i < n; i++) {
        cin >> prices[i];
    }

    clock_t start = clock();
    int max_revenue = rodCutting(n, prices);
    double timeTaken = double(clock() - start) / CLOCKS_PER_SEC;

    cout << "Maximum Revenue: " << max_revenue << "\n";
    cout << "Time taken: " << timeTaken << " seconds\n";

    return 0;
}
