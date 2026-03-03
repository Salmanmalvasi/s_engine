#include <iostream>
#include <vector>
#include <climits>
#include <ctime>

using namespace std;

void MCM(
    vector<int>& p,
    vector<vector<int>>& m,
    vector<vector<int>>& s,
    int n
){
    for(int i = 0; i < n; i++){
        m[i][i] = 0;
    }
    for(int L = 2; L < n; L++){
        for(int i = 1; i < n - L + 1; i++){
            int j = i + L - 1;
            m[i][j] = INT_MAX;
            for(int k = i; k < j; k++){
                int cost = m[i][k] + m[k+1][j] + p[i-1] * p[k] * p[j];
                if(cost < m[i][j]){
                    m[i][j] = cost;
                    s[i][j] = k;
                }
            }
        }
    }
}

void printOptimal(vector<vector<int>>& s, int i, int j){
    if(i == j){
        cout << "A" << i;
        return;
    }
    cout << "(";
    printOptimal(s, i, s[i][j]);
    printOptimal(s, s[i][j] + 1, j);
    cout << ")";
}

int main() {
    int n;
    cin >> n;
    vector<int> p(n);
    for (int i = 0; i < n; i++)
        cin >> p[i];

    vector<vector<int>> m(n, vector<int>(n, 0));
    vector<vector<int>> s(n, vector<int>(n, 0));

    clock_t start = clock();
    MCM(p, m, s, n);
    double timeTaken = double(clock() - start) / CLOCKS_PER_SEC;

    cout << "Minimum Cost: " << m[1][n - 1] << "\n";
    cout << "Time taken: " << timeTaken << " seconds\n";
    return 0;
}
