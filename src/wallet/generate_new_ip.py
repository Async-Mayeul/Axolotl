def convert_ip_to_transaction(ip):
    ip_splited = ip.split('.')

    first_byte = hex(int(ip_splited[0]))
    second_byte = hex(int(ip_splited[1]))
    three_byte = hex(int(ip_splited[2]))
    four_byte = hex(int(ip_splited[3]))

    if len(first_byte) != 4:
        first_byte = first_byte[0:2] + '0' + first_byte[2:]
    if len(three_byte) != 4:
        three_byte = three_byte[0:2] + '0' + three_byte[2:]
    if len(second_byte) != 4:
        second_byte = second_byte[0:2] + '0' + second_byte[2:]
    if len(four_byte) != 4:
        four_byte = four_byte[0:2] + '0' + four_byte[2:]

    transaction_two = first_byte + second_byte[2:] 
    transaction_one = three_byte + four_byte[2:]
    
    transaction_two = int(transaction_two, 16) ^ 0xffff
    transaction_one = int(transaction_one, 16) ^ 0xffff

    transaction_two = str(transaction_two / 1000000)
    transaction_one = str(transaction_one / 1000000)

    return transaction_two, transaction_one


def main():
    ip = input("Enter the IP you want to backup : ")
    transaction_two, transaction_one = convert_ip_to_transaction(ip)
    print("First transaction to do : {transaction_one}\n".format(transaction_one=transaction_one))
    print("Second transaction to do : {transaction_two}\n".format(transaction_two=transaction_two))

if __name__ == "__main__":
    main()
