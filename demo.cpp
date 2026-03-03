#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include<climits>
#include <queue>
using namespace std;
struct Node{
    char data;
    int freq;
    Node* left;
    Node* right;
    Node(char n,int m){
        data = n;
        freq = m;
        left=right=nullptr;
    }
};
struct compare{
    bool operator()(Node* a,Node* b){
        return a->freq > b->freq;
    }
};
void printCodes(Node* root,string code){
    if(!root){
        return;
    }
    if(!root->left && !root->right){
        cout<<root->data<<" : "<<code<<endl;
        return;
    }
    printCodes(root->left,code+"0");
    printCodes(root->right,code+"1");
}
void huffmanCoding(vector<char>& chars,vector<int>& freq){
    priority_queue<Node*,vector<Node*>,compare> minheap;
    for(int i=0;i<chars.size();i++){
        minheap.push(new Node(chars[i],freq[i]));
    }
    while(minheap.size()>1){
        Node* left = minheap.top();
        minheap.pop();
        Node* right = minheap.top();
        minheap.pop();
        Node* parent = new Node('$',left->freq+right->freq);
        parent->left = left;
        parent->right = right;
        minheap.push(parent);
    }
    Node* root = minheap.top();
    printCodes(root,"");
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
    huffmanCoding(chars, freq);
    return 0;
}
