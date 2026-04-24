import sys 

class _Node:
    """
    A node in a single linked list
    """
    def __init__(self, key, value, next_node=None):
        self.key   = key
        self.value = value
        self.next  = next_node


class HashTable:
    """
    Hash map implemented with separate chaining,
    where each bucket is a linked list of key-value pairs.
    #TODO  ######################## MAYBE DELETE ######################### 
        ht[key]          → get value (raises KeyError if missing)
        ht[key] = value  → insert or update
        del ht[key]      → delete (raises KeyError if missing)
        key in ht        → membership test
        ht.keys()        → iterator over keys
        ht.values()      → iterator over values
        len(ht)          → number of pairs

    """
    _UPPER_LOAD = 1.0  
    _LOWER_LOAD = 0.25 

    #TODO only expanitory for Petter, maybe delete afterwards
    # Minimum array size: never shrink below this so we don't
    # thrash on tiny tables (resizing often, shrinking and growing).
    _MIN_SIZE = 1

    def __init__(self):
        #start with an array of size 1 
        self._m = self._MIN_SIZE
        self._n = 0
        self._table = [None] * self._m
    
    def _hash(self, key):
        """
        Compute the hash value of the key and map it to a bucket index.
        """
        return abs(hash(key)) % self._m         #Python's built-in hash func can return negative values
    

    def _find(self, key):
        """
        Locate a node in the chain for the given key.

        Returns:
            prev: the node preceding the target node (or None if target is at head)
            curr: the node containing the key (or None if not found)
        """
        idx  = self._hash(key)
        prev = None
        curr = self._table[idx]
        while curr is not None:
            if curr.key == key:
                return prev, curr      #found
            prev = curr
            curr = curr.next
        return prev, None              #not found


    def __contains__(self, key):
        """
        Checks if the key exists in the hash table. Returns True if found, False otherwise.
        """
        _, node = self._find(key)

        if node is not None:
            return True
        else:
            return False
    

    def __getitem__(self, key):
        """
        Retrieves the value associated with the given key. Raises KeyError if the key is not found.

        Returns:
            node.value: The value associated with the key.
        """
        _, node = self._find(key)
        if node is None:
            raise KeyError(key)
        return node.value


    def __setitem__(self, key, value):
        """
        Inserts a new key-value pair or updates the value of an existing key.
        After insertion, checks if the load factor exceeds the upper bound and resizes if necessary.
    
        """
        _, node = self._find(key)
        if node is not None:
            #if key is already present, update the value
            node.value = value
        else:
            #insert new node at the head of the chain
            idx = self._hash(key)
            self._table[idx] = _Node(key, value, self._table[idx])
            self._n += 1
            # check load factor upper bound
            if self._n / self._m > self._UPPER_LOAD:
                self._resize(self._m * 2)


    def __delitem__(self, key):
        """
        Deletes the key-value pair associated with the given key. Raises KeyError if the key is not found.
        After deletion, checks if the load factor falls below the lower bound and resizes if necessary.

        """
        prev, node = self._find(key)
        if node is None:
            raise KeyError(key)
        idx = self._hash(key)
        if prev is None:
            #node is the head of the chain
            self._table[idx] = node.next
        else:
            #bypass the node
            prev.next = node.next
        self._n -= 1
        #check load factor lower bound (but keep minimum size)
        new_m = self._m // 2
        if (new_m >= self._MIN_SIZE and self._n / self._m < self._LOWER_LOAD):
            self._resize(new_m)


    def _resize(self, new_m):
        """
        Resizes the hash table to the new size and rehashes all existing key-value pairs.
        """
        new_m = max(new_m, self._MIN_SIZE)
        old_table = self._table
        self._m = new_m
        self._table = [None] * new_m
        self._n = 0       #will be increased as we re-insert nodes into new table 
        #re-insert all existing pairs
        for head in old_table:
            curr = head
            while curr is not None:
                #insert at beginning of new chain (no duplicate check needed: old table had no duplicates)
                idx = self._hash(curr.key)
                self._table[idx] = _Node(curr.key, curr.value, self._table[idx])
                self._n += 1
                curr = curr.next


    def keys(self):
        """
        Returns a list of all keys in the table.
        """
        result = []
        for head in self._table:
            curr = head
            while curr is not None:
                result.append(curr.key)
                curr = curr.next
        return result

    def values(self):
        """
        Returns a list of all values in the table.
        """
        result = []
        for head in self._table:
            curr = head
            while curr is not None:
                result.append(curr.value)
                curr = curr.next
        return result


    def __len__(self):
        return self._n
    

    #TODO delete afterward
    # -----------------------------------------------------------
    # Debug helper – useful during development 
    # -----------------------------------------------------------
    def _debug_print(self):
        print(f"  m={self._m}, n={self._n}, α={self._n/self._m:.2f}")
        for i, head in enumerate(self._table):
            if head is not None:
                chain = []
                curr = head
                while curr:
                    chain.append(f"({curr.key!r}:{curr.value})")
                    curr = curr.next
                print(f"  [{i}] -> " + " -> ".join(chain))


def main():
    d = HashTable()
    i = 0

    for line in sys.stdin:
        word = line.strip()

        #TODO delete this statement?
        #if not word:
        #    continue

        is_present = word in d        #uses __contains__
        remove_it  = (i % 16 == 0)

        if is_present:
            if remove_it:
                del d[word]           #uses __delitem__
            else:
                d[word] = d[word] + 1 #uses __getitem__ + __setitem__
        elif not remove_it:
            d[word] = 1               #uses __setitem__

        i += 1

    if len(d) == 0:
        return

    #find max count
    best_count = max(d.values())

    #among all keys with that count, find alphabetically first
    best_word = None
    for k in d.keys():
        if d[k] == best_count:
            if best_word is None or k < best_word:
                best_word = k

    print(best_word, best_count)


if __name__ == "__main__":
    main()


