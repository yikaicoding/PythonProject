import time
import random

class Medicine:
    def __init__(self, product_id: int, name: str, price: float, stock: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock = stock

    def __str__(self):
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock}")


class LinearProbingHashTable:
    def __init__(self, initial_size=101):
        self.size = initial_size
        self.keys = [None] * self.size
        self.values = [None] * self.size
        self.deleted = [False] * self.size
        self.count = 0

    def hash_function(self, key: int) -> int:
        return key % self.size

    def _is_prime(self, n: int) -> bool:
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    def _next_prime(self, n: int) -> int:
        while not self._is_prime(n):
            n += 1
        return n

    def _rehash(self):
        old_keys = self.keys
        old_values = self.values
        old_deleted = self.deleted

        new_size = self._next_prime(self.size * 2)
        self.size = new_size
        self.keys = [None] * new_size
        self.values = [None] * new_size
        self.deleted = [False] * new_size
        self.count = 0

        for i in range(len(old_keys)):
            if old_keys[i] is not None and not old_deleted[i]:
                self.insert(old_keys[i], old_values[i])

    def insert(self, key: int, value: Medicine) -> int:
        if (self.count + 1) / self.size >= 0.7:
            self._rehash()

        index = self.hash_function(key)
        first_deleted_index = None

        while self.keys[index] is not None:
            if self.keys[index] == key and not self.deleted[index]:
                self.values[index] = value
                return index
            if self.deleted[index] and first_deleted_index is None:
                first_deleted_index = index
            index = (index + 1) % self.size

        target_index = first_deleted_index if first_deleted_index is not None else index
        self.keys[target_index] = key
        self.values[target_index] = value
        self.deleted[target_index] = False
        self.count += 1
        return target_index

    def search(self, key: int):
        index = self.hash_function(key)
        start_index = index

        while self.keys[index] is not None:
            if self.keys[index] == key and not self.deleted[index]:
                return self.values[index]
            index = (index + 1) % self.size
            if index == start_index:
                break
        return None


def search_array(array_storage: list, product_id: int):
    for item in array_storage:
        if item.product_id == product_id:
            return item
    return None


def preload_data(hash_table: LinearProbingHashTable, array_storage: list):
    # Sample record matching prompt
    sample_med = Medicine(1042, "Paracetamol 500mg", 5.90, 120)
    hash_table.insert(sample_med.product_id, sample_med)
    array_storage.append(sample_med)

    # Synthetic test records for benchmark
    for i in range(1000, 2000):
        if i == 1042:
            continue
        med = Medicine(i, f"Medicine-{i}", round(random.uniform(2.0, 150.0), 2), random.randint(1, 200))
        hash_table.insert(med.product_id, med)
        array_storage.append(med)


def main():
    hash_table = LinearProbingHashTable()
    array_storage = []

    preload_data(hash_table, array_storage)

    while True:
        print("\nPharmacy Inventory System")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Exit")

        choice = input("Enter choice: ").strip()

        if choice == '1':
            try:
                pid = int(input("Enter Product ID: "))
                name = input("Enter Product Name: ").strip()
                price = float(input("Enter Price: "))
                stock = int(input("Enter Stock Quantity: "))

                product = Medicine(pid, name, price, stock)
                slot = hash_table.insert(pid, product)
                array_storage.append(product)

                print(f"Product inserted successfully into slot [{slot}]")
            except ValueError:
                print("Invalid input! Enter numbers for ID, Price, and Stock.")

        elif choice == '2':
            try:
                target_id = int(input("Enter Product ID to search: "))

                t0 = time.perf_counter()
                found_ht = hash_table.search(target_id)
                ht_time = time.perf_counter() - t0

                t1 = time.perf_counter()
                found_arr = search_array(array_storage, target_id)
                arr_time = time.perf_counter() - t1

                if found_ht:
                    print("Product Found!")
                    print(found_ht)
                    print(f"Search completed in {ht_time:.6f} seconds (Hash Table)")
                    print(f"Search completed in {arr_time:.6f} seconds (Array - same record)")
                else:
                    print("Product Not Found!")
                    print(f"Search completed in {ht_time:.6f} seconds (Hash Table)")
                    print(f"Search completed in {arr_time:.6f} seconds (Array - checked all records)")
            except ValueError:
                print("Invalid Product ID!")

        elif choice == '3':
            print("Exiting Inventory System. Goodbye!")
            break
        else:
            print("Invalid choice! Select 1, 2, or 3.")


if __name__ == "__main__":
    main()