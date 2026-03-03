#include <chrono>
#include <cstdint>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>

using namespace std;

static vector<int> naive_match(const string &text, const string &pattern) {
    vector<int> pos;
    const int n = (int)text.size();
    const int m = (int)pattern.size();
    if (m == 0 || m > n) return pos;

    for (int i = 0; i + m <= n; i++) {
        int j = 0;
        while (j < m && text[i + j] == pattern[j]) j++;
        if (j == m) pos.push_back(i);
    }
    return pos;
}

static vector<int> rabin_karp_match(const string &text, const string &pattern) {
    vector<int> pos;
    const int n = (int)text.size();
    const int m = (int)pattern.size();
    if (m == 0 || m > n) return pos;

    const uint64_t base = 911382323u;

    uint64_t patHash = 0;
    uint64_t winHash = 0;
    uint64_t power = 1; // base^(m-1)

    for (int i = 0; i < m; i++) {
        patHash = patHash * base + (uint8_t)pattern[i];
        winHash = winHash * base + (uint8_t)text[i];
        if (i < m - 1) power *= base;
    }

    auto check_equal = [&](int start) -> bool {
        for (int j = 0; j < m; j++) {
            if (text[start + j] != pattern[j]) return false;
        }
        return true;
    };

    if (patHash == winHash && check_equal(0)) pos.push_back(0);

    for (int i = m; i < n; i++) {
        uint64_t lead = (uint8_t)text[i - m];
        winHash -= lead * power;
        winHash = winHash * base + (uint8_t)text[i];

        int start = i - m + 1;
        if (winHash == patHash && check_equal(start)) pos.push_back(start);
    }

    return pos;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    // Input format:
    // algo
    // text
    // pattern
    // algo = 0 -> naive, 1 -> rabin-karp

    int algo;
    string text, pattern;
    if (!(cin >> algo)) {
        cerr << "Invalid input. Expected: algo (0/1), text, pattern\n";
        return 1;
    }
    if (!(cin >> text >> pattern)) {
        cerr << "Invalid input. Expected: text and pattern (no spaces).\n";
        return 1;
    }

    auto start = chrono::high_resolution_clock::now();
    vector<int> matches;
    if (algo == 0)
        matches = naive_match(text, pattern);
    else
        matches = rabin_karp_match(text, pattern);
    auto stop = chrono::high_resolution_clock::now();

    chrono::duration<double> elapsed = stop - start;

    cout << "Matches: " << matches.size() << "\n";
    if (!matches.empty()) {
        cout << "Positions:";
        for (int p : matches) cout << ' ' << p;
        cout << "\n";
    }
    cout << "Time taken: " << fixed << setprecision(9) << elapsed.count() << " seconds\n";

    return 0;
}
