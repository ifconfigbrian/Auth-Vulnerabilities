# Generate a list of 4-digit codes
with open('2fa_codes.txt', 'w') as file:
    for i in range(10000):  # 0000 to 9999
        file.write(f'{i:04d}\n')

print("2FA codes generated and saved to '2fa_codes.txt'.")




