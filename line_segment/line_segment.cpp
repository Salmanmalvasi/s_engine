#include <iostream>
#include <vector>
#include <chrono>
#include <fstream>
#include <iomanip>

using namespace std;
using namespace std::chrono;

struct Point {
    long long x, y;
};

// To find orientation of ordered triplet (p, q, r).
// 0 --> p, q and r are collinear
// 1 --> Clockwise
// 2 --> Counterclockwise
int orientation(Point p, Point q, Point r) {
    long long val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y);
    if (val == 0) return 0;
    return (val > 0) ? 1 : 2;
}

// Given three collinear points p, q, r, the function checks if point q lies on line segment 'pr'
bool onSegment(Point p, Point q, Point r) {
    if (q.x <= max(p.x, r.x) && q.x >= min(p.x, r.x) &&
        q.y <= max(p.y, r.y) && q.y >= min(p.y, r.y))
        return true;
    return false;
}

// The main function that returns true if line segment 'p1q1' and 'p2q2' intersect.
bool doIntersect(Point p1, Point q1, Point p2, Point q2) {
    int o1 = orientation(p1, q1, p2);
    int o2 = orientation(p1, q1, q2);
    int o3 = orientation(p2, q2, p1);
    int o4 = orientation(p2, q2, q1);

    // General case
    if (o1 != o2 && o3 != o4)
        return true;

    // Special Cases
    if (o1 == 0 && onSegment(p1, p2, q1)) return true;
    if (o2 == 0 && onSegment(p1, q2, q1)) return true;
    if (o3 == 0 && onSegment(p2, p1, q2)) return true;
    if (o4 == 0 && onSegment(p2, q1, q2)) return true;

    return false;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cerr << "Usage: " << argv[0] << " <input_file>\n";
        return 1;
    }

    ifstream fin(argv[1]);
    if (!fin) {
        cerr << "Error opening file " << argv[1] << "\n";
        return 1;
    }

    int N;
    fin >> N;
    vector<pair<pair<Point, Point>, pair<Point, Point>>> inputs(N);
    for (int i = 0; i < N; ++i) {
        fin >> inputs[i].first.first.x >> inputs[i].first.first.y
            >> inputs[i].first.second.x >> inputs[i].first.second.y
            >> inputs[i].second.first.x >> inputs[i].second.first.y
            >> inputs[i].second.second.x >> inputs[i].second.second.y;
    }
    fin.close();

    int intersectCount = 0;

    auto start_time = high_resolution_clock::now();
    for (int i = 0; i < N; ++i) {
        if (doIntersect(inputs[i].first.first, inputs[i].first.second,
                        inputs[i].second.first, inputs[i].second.second)) {
            intersectCount++;
        }
    }
    auto end_time = high_resolution_clock::now();
    auto duration = duration_cast<nanoseconds>(end_time - start_time);

    cout << "\n==========================================\n";
    cout << "  ILP 14: Line Segment Intersection       \n";
    cout << "==========================================\n";
    cout << "Input Size (Pairs) : " << N << "\n";
    cout << "Intersections Found: " << intersectCount << "\n";
    cout << "Time Taken (ns)    : " << duration.count() << "\n";
    cout << "==========================================\n";

    return 0;
}
