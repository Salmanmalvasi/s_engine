#include <chrono>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "Algorithm: Floyd-Warshall (All-Pairs Shortest Paths)\n";

    int n, m;
    if (!(cin >> n >> m)) {
        cerr << "Invalid input. Expected: n m then m lines of u v w\n";
        return 1;
    }

    const long long INF = numeric_limits<long long>::max() / 4;
    vector<vector<long long>> dist(n, vector<long long>(n, INF));

    for (int i = 0; i < n; i++) dist[i][i] = 0;

    for (int i = 0; i < m; i++) {
        int u, v;
        long long w;
        cin >> u >> v >> w;
        dist[u][v] = min(dist[u][v], w);
    }

    auto start = chrono::high_resolution_clock::now();

    for (int k = 0; k < n; k++) {
        for (int i = 0; i < n; i++) {
            if (dist[i][k] == INF) continue;
            for (int j = 0; j < n; j++) {
                if (dist[k][j] == INF) continue;
                long long nd = dist[i][k] + dist[k][j];
                if (nd < dist[i][j]) dist[i][j] = nd;
            }
        }
    }

    bool negCycle = false;
    for (int i = 0; i < n; i++) {
        if (dist[i][i] < 0) { negCycle = true; break; }
    }

    auto stop = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = stop - start;

    if (negCycle)
        cout << "Negative cycle detected\n";
    else
        cout << "No negative cycle detected\n";

    long long reachablePairs = 0, sumDist = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            if (dist[i][j] != INF) { reachablePairs++; sumDist += dist[i][j]; }

    cout << "ReachablePairs: " << reachablePairs << "\n";
    cout << "SumDist: " << sumDist << "\n";
    cout << "Time taken: " << fixed << setprecision(9) << elapsed.count() << " seconds\n";
    return 0;
}
