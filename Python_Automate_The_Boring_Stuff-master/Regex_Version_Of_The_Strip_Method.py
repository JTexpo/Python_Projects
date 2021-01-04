import re

def re_strip(my_string,my_strip_string = ' '):
    for char in my_strip_string:
        if ord(char) < 48 or (ord(char) > 90 and ord(char) < 97) or ord(char) > 122:
            char = '\\' + char
        my_string = re.compile(char).sub(r'',my_string)
    return my_string
   

if __name__ == "__main__":
    test_str_one = '     cats     '
    test_str_two = '...hey,,,, bob'
    test_str_thr = 'abc123def456ghi'
    print(re_strip(test_str_one))
    print(re_strip(test_str_two,".,"))
    print(re_strip(test_str_thr,'123456789'))
