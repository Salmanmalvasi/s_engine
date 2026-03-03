#include <iostream>
#include <vector>
#include <string>
#include <ctime>

using namespace std;

string LCS(const string& X, const string& Y) {
    int m = X.length();
    int n = Y.length();
    vector<vector<int>> dp(m + 1, vector<int>(n + 1, 0));

    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (X[i - 1] == Y[j - 1]) {
                dp[i][j] = 1 + dp[i - 1][j - 1];
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    string lcs;
    int i = m, j = n;
    while (i > 0 && j > 0) {
        if (X[i - 1] == Y[j - 1]) {
            lcs = X[i - 1] + lcs;
            i--;
            j--;
        } else if (dp[i - 1][j] > dp[i][j - 1]) {
            i--;
        } else {
            j--;
        }
    }

    return lcs;
}

int main() {
    string X, Y;
    cin >> X >> Y;

    clock_t start = clock();
    string lcs = LCS(X, Y);
    double timeTaken = double(clock() - start) / CLOCKS_PER_SEC;

    cout << "LCS Length: " << lcs.length() << "\n";
    cout << "LCS String: " << lcs << "\n";
    cout << "Time taken: " << timeTaken << " seconds\n";

    return 0;
}
