count = 0

# 0
for num in range(1000):
    if '0' in str(num):
        count += 1
        print(num)

print("Number of '0' numbers from 0 to 999:", count,"\n")

count = 0

# 0 and 9  
for num in range(1000):
    if '0' in str(num) and '9' in str(num):
        count += 1
        print(num)
                
print("Number of '0+9' numbers from 0 to 999:", count,"\n")

count = 0
# 8 and 9  
for num in range(1000):
    if '8' in str(num) and '9' in str(num):
        count += 1
        print(num)
                
print("Number of '8+9' numbers from 0 to 999:", count,"\n")