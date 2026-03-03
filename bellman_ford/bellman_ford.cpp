#include <chrono>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

using namespace std;

struct Edge {
    int u;
    int v;
    long long w;
};

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    cout << "Algorithm: Bellman-Ford (Single Source Shortest Path)" << "\n";

    int n, m, src;
    if (!(cin >> n >> m >> src)) {
        cerr << "Invalid input. Expected: n m src then m lines of u v w\n";
        return 1;
    }

    vector<Edge> edges;
    edges.reserve(m);

    for (int i = 0; i < m; i++) {
        Edge e;
        cin >> e.u >> e.v >> e.w;
        edges.push_back(e);
    }

    const long long INF = numeric_limits<long long>::max() / 4;
    vector<long long> dist(n, INF);
    dist[src] = 0;

    auto start = chrono::high_resolution_clock::now();

    for (int i = 1; i <= n - 1; i++) {
        bool changed = false;
        for (const auto &e : edges) {
            if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
                dist[e.v] = dist[e.u] + e.w;
                changed = true;
            }
        }
        if (!changed) break;
    }

    bool negCycle = false;
    for (const auto &e : edges) {
        if (dist[e.u] != INF && dist[e.u] + e.w < dist[e.v]) {
            negCycle = true;
            break;
        }
    }

    auto stop = chrono::high_resolution_clock::now();
    chrono::duration<double> elapsed = stop - start;

    if (negCycle) {
        cout << "Negative cycle detected (reachable from source)\n";
    } else {
        cout << "No negative cycle detected\n";
    }

    long long reachable = 0;
    long long sumDist = 0;
    for (int i = 0; i < n; i++) {
        if (dist[i] != INF) {
            reachable++;
            sumDist += dist[i];
        }
    }

    cout << "Reachable: " << reachable << "\n";
    cout << "SumDist: " << sumDist << "\n";
    cout << "Time taken: " << fixed << setprecision(9) << elapsed.count() << " seconds\n";

    return 0;
}
