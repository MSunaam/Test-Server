from Tree.Models.HashFunc import HashFunc

test_data = "Helloo My name is Sunaam"

print(f"\033[1m\033[32mHash Function with 10 Rounds\033[0m\033[0m\t{HashFunc.custom_hash(test_data)}")
print(f"\033[1m\033[32mHash Function with 12 Rounds\033[0m\033[0m\t{HashFunc.custom_hash(test_data, rounds=12)}")