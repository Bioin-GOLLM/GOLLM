import os

def count_lines(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    return len(lines)

def make_subsets(file, num_subsets):
    with open(file, 'r') as f:
        lines = f.readlines()
    total_lines = len(lines)
    subset_size = total_lines // num_subsets
    remainder = total_lines % num_subsets

    subsets = []
    start_index = 0
    for i in range(num_subsets):
        end_index = start_index + subset_size + (1 if i < remainder else 0)
        subsets.append(lines[start_index:end_index])
        start_index = end_index

    return subsets

def find_largest_divisor(number):
    largest_divisor = None
    for x in range(1, 101):
        if number % x == 0:
            largest_divisor = x
    return largest_divisor

def main():
    file = "C:/Users/aivan/Desktop/BIOIN 401/GOLLM/data/matching_pmids.txt"
    lines = count_lines(file)
    num_subsets = find_largest_divisor(lines)        # largest divisor for our subset.
    print(f"The number of lines in the file is: {lines} and it will be divided into {num_subsets} subsets")
    
    subsets = make_subsets(file, num_subsets)

    os.makedirs("data/subsets", exist_ok=True)
    for i, subset in enumerate(subsets):
        with open(f"data/subsets/subset_{i + 1}.txt", 'w') as f:
            f.writelines(subset)
        print(f"Subset {i + 1} contains {len(subset)} lines")
    
    print("Subsets have been created")

if __name__ == "__main__":
    main()