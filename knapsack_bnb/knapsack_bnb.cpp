#include <algorithm>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <queue>
#include <vector>

using namespace std;

struct Item {
    int weight;
    int value;
    double ratio;
};

struct Node {
    int level;              
    long long value;        
    long long weight;       
    double bound;           
};

static double compute_bound(const Node &u, int n, long long W, const vector<Item> &items) {
    if (u.weight >= W) return 0.0;

    long long totalWeight = u.weight;
    double profitBound = static_cast<double>(u.value);

    int j = u.level;
    while (j < n && totalWeight + items[j].weight <= W) {
        totalWeight += items[j].weight;
        profitBound += items[j].value;
        j++;
    }

    if (j < n) {
        long long remain = W - totalWeight;
        profitBound += remain * items[j].ratio;
    }

    return profitBound;
}

static long long knapsack_branch_and_bound(int n, long long W, vector<Item> items) {
    sort(items.begin(), items.end(), [](const Item &a, const Item &b) {
        return a.ratio > b.ratio;
    });

    auto cmp = [](const Node &a, const Node &b) { return a.bound < b.bound; };
    priority_queue<Node, vector<Node>, decltype(cmp)> pq(cmp);

    Node root{0, 0, 0, 0.0};
    root.bound = compute_bound(root, n, W, items);
    pq.push(root);

    long long best = 0;

    while (!pq.empty()) {
        Node u = pq.top();
        pq.pop();

        if (u.bound <= best) continue;
        if (u.level >= n) continue;

        Node v_include;
        v_include.level = u.level + 1;
        v_include.weight = u.weight + items[u.level].weight;
        v_include.value = u.value + items[u.level].value;
        v_include.bound = 0.0;

        if (v_include.weight <= W) {
            if (v_include.value > best) best = v_include.value;
            v_include.bound = compute_bound(v_include, n, W, items);
            if (v_include.bound > best) pq.push(v_include);
        }

        Node v_exclude;
        v_exclude.level = u.level + 1;
        v_exclude.weight = u.weight;
        v_exclude.value = u.value;
        v_exclude.bound = compute_bound(v_exclude, n, W, items);
        if (v_exclude.bound > best) pq.push(v_exclude);
    }

    return best;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long W;
    if (!(cin >> n >> W)) {
        cerr << "Invalid input. Expected: n W then n lines of (weight value).\n";
        return 1;
    }

    vector<Item> items;
    items.reserve(n);
    for (int i = 0; i < n; i++) {
        long long w, v;
        cin >> w >> v;
        Item it;
        it.weight = static_cast<int>(w);
        it.value = static_cast<int>(v);
        it.ratio = (it.weight == 0) ? 0.0 : (static_cast<double>(it.value) / it.weight);
        items.push_back(it);
    }

    auto start = chrono::high_resolution_clock::now();
    long long ans = knapsack_branch_and_bound(n, W, items);
    auto stop = chrono::high_resolution_clock::now();

    chrono::duration<double> elapsed = stop - start;

    cout << "Maximum Profit: " << ans << "\n";
    cout << "Time taken: " << fixed << setprecision(9) << elapsed.count() << " seconds\n";

    return 0;
}
