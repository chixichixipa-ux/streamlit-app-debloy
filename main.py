fruit_list
#リストから偶数だけを抽出する関数
def extract_even_numbers(numbers):
    even_numbers = []
    for number in numbers:
        if number % 2 == 0:
            even_numbers.append(number)
    return even_numbers = ['apple', 'banana', 'cherry', 'date', 'elderberry']  