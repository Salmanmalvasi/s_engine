#include <iostream>
#include <vector>
#include <queue>
#include <string>
#include <ctime>

using namespace std;

struct Node {
    char data;
    int freq;
    Node* left;
    Node* right;
    Node(char c, int f) : data(c), freq(f), left(nullptr), right(nullptr) {}
};

struct Compare {
    bool operator()(Node* a, Node* b) {
        return a->freq > b->freq;
    }
};

void printCodes(Node* root, string code, vector<pair<char, string>>& codes) {
    if (!root) return;
    if (!root->left && !root->right) {
        codes.push_back({root->data, code});
        return;
    }
    printCodes(root->left, code + "0", codes);
    printCodes(root->right, code + "1", codes);
}

void huffmanCoding(vector<char>& chars, vector<int>& freq, vector<pair<char, string>>& codes) {
    priority_queue<Node*, vector<Node*>, Compare> minHeap;
    
    for (size_t i = 0; i < chars.size(); i++) {
        minHeap.push(new Node(chars[i], freq[i]));
    }
    
    while (minHeap.size() > 1) {
        Node* left = minHeap.top(); minHeap.pop();
        Node* right = minHeap.top(); minHeap.pop();
        Node* parent = new Node('$', left->freq + right->freq);
        parent->left = left;
        parent->right = right;
        minHeap.push(parent);
    }
    
    Node* root = minHeap.top();
    printCodes(root, "", codes);
}

int main() {
    int n;
    cin >> n;
    
    vector<char> chars(n);
    vector<int> freq(n);
    
    for (int i = 0; i < n; i++)
        cin >> chars[i];
    for (int i = 0; i < n; i++)
        cin >> freq[i];
    
    vector<pair<char, string>> codes;
    
    clock_t start = clock();
    huffmanCoding(chars, freq, codes);
    double timeTaken = double(clock() - start) / CLOCKS_PER_SEC;
    
    cout << "Huffman Codes:\n";
    for (auto& p : codes) {
        cout << p.first << " : " << p.second << "\n";
    }
    cout << "Number of symbols: " << n << "\n";
    cout << "Time taken: " << timeTaken << " seconds\n";
    
    return 0;
}
