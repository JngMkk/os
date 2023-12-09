#include <iostream>
#include <list>
#include <unordered_map>

using namespace std;

class LRUCache {
    list<int> li;
    unordered_map<int, list<int>::iterator> hash;
    int csize;

public:
    LRUCache(int);
    void refer(int);
    void display();
};

LRUCache::LRUCache(int n) {
    csize = n;
}

void LRUCache::refer(int x) {
    if (hash.find(x) == hash.end()) {
        if (li.size() == csize) {
            int last = li.back();   // 가장 끝에 있는 것이 참조가 가장 오래된 것
            li.pop_back();
            hash.erase(last);
        }
    } else {
        li.erase(hash[x]);
    }

    li.push_front(x);               // 해당 페이지를 참조할 때, 가장 앞으로 추가.
    hash[x] = li.begin();           // 해시 테이블에 저장
}

void LRUCache::display() {
    for (auto it = li.begin(); it != li.end(); it++) {
        cout << (*it) << " ";
    }
    cout << "\n";
}

int main() {
    LRUCache ca(3);
    ca.refer(1);
    ca.display();
    ca.refer(3);
    ca.display();
    ca.refer(0);
    ca.display();
    ca.refer(3);
    ca.display();
    ca.refer(5);
    ca.display();
    ca.refer(6);
    ca.display();
    ca.refer(3);
    ca.display();
    
    return 0;
}

/*
1 
3 1 
0 3 1 
3 0 1 
5 3 0 
6 5 3 
3 6 5
*/
