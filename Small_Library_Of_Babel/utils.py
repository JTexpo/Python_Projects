import math


# --------------
# MATH FUNCTIONS
# --------------
def power_of_2(number: int) -> int:
    """Given a number, returns which power that number is of 2.

    Args:
        number (int): a number which is a power of 2

    Returns:
        int: the power that 2 needs to be raised to to achieve in input number
    """
    number_log_2 = math.log(number, 2)
    return None if int(number_log_2) != number_log_2 else int(number_log_2)


def base_10_to_base_encode(number: int, encode_string: str) -> str:
    """Converts base 10 number into any base / code, given a string of what that code can be

    Args:
        number (int): the base 10 number you wish to convert
        encode_string (str): the new bases reference

    Returns:
        str: a new encoded number depending on the base
    """
    if number == 0:
        return "0"

    result = ""
    encode_string_len = len(encode_string)
    while number > 0:
        digit = number % encode_string_len
        result = encode_string[digit] + result
        number //= encode_string_len

    return result


def base_encode_to_base_10(string: str, encode_string: str) -> int:
    """converts any base coded number to base 10, given that you have the encoded schema

    Args:
        string (str): the coded number
        encode_string (str): a string of the coded schema mappings

    Returns:
        int: a base 10 number related to the one encoded
    """
    result = 0

    encode_string_len = len(encode_string)
    for char_index in range(len(string)):
        result += encode_string.index(string[char_index]) * (
            encode_string_len ** (len(string) - char_index - 1)
        )

    return result

def get_users_library_option() -> str:
    return input(
        """What would you like todo?
1. Search for book with string
2. Search for book with section / wall / shelf / volumn / page
0. Leave
: """
    )

# ---------------------------
# STRING ENCRYPTION FUNCTIONS
# ---------------------------
def get_user_search_string() -> str:
    return input(
        """What is the content that you are looking for?
: """
    )


def groom_user_search_string(user_string: str, max_size: int) -> str:
    if len(user_string) > max_size:
        print(
            f"Sorry, but that string is too long. Lucky, there is a book which contains :\n{user_string[:max_size]}"
        )
        return user_string[:max_size]
    elif len(user_string) < max_size:
        return user_string.ljust(max_size, " ")
    return user_string


def get_book_location(
    user_string: str,
    VAILD_CHARACTERS: str,
    VALID_ENCRYPTED_CHARACTERS: str,
    WALLS_SPACE: int,
    SHELVES_SPACE: int,
    VOLUMN_SPACE: int,
    PAGES_SPACE: int,
):
    """A function to return the cryptic book location

    Args:
        user_string (str): the string which is contained in a book
        VAILD_CHARACTERS (str): an encoding of all of the allowed user inputs
        VALID_ENCRYPTED_CHARACTERS (str): an encoding of all of the allowed characters for the section
        WALLS_SPACE (int): bit size of how much the wall takes up
        SHELVES_SPACE (int): bit size of how much the shelves takes up
        VOLUMN_SPACE (int): bit size of how much the volumns takes up
        PAGES_SPACE (int): bit size of how much the pages takes up

    Returns:
        The encrypted details on where to find the inputed string in the library
    """
    reserve_space = WALLS_SPACE + SHELVES_SPACE + VOLUMN_SPACE + PAGES_SPACE

    # 1. Base Valid Characters -> Base 10
    base_10_encode = base_encode_to_base_10(user_string, VAILD_CHARACTERS)

    # 2. Base 10 -> Base 2
    base_2_encode = str(bin(base_10_encode))[2:]

    # 3. Chop off the total of bits that the walls, shelves, volumns, pages take up
    # 3ex : assuming that all are 2, that is a bit space of 1 meaning a binary string of
    # 111001010010 becomes 11100101 0010
    base_2_details = base_2_encode[-reserve_space:]
    base_2_section = base_2_encode[:-reserve_space]

    # 4. the longer section Base 2 -> Base 10
    base_10_section = int(base_2_section, 2)

    # 5. Base 10 -> Base Encrypted Characters
    section = base_10_to_base_encode(base_10_section, VALID_ENCRYPTED_CHARACTERS)

    # 6. The remaning binary space from step 3 is then interpeted in base 10 value
    wall = int(base_2_details[:WALLS_SPACE], 2)
    shelf = int(base_2_details[WALLS_SPACE : WALLS_SPACE + SHELVES_SPACE], 2)
    volumn = int(
        base_2_details[
            WALLS_SPACE + SHELVES_SPACE : +WALLS_SPACE + SHELVES_SPACE + VOLUMN_SPACE
        ],
        2,
    )
    page = int(base_2_details[-PAGES_SPACE:], 2)

    # +1's because we are not computers and start at index 1 not 0
    return (section, wall + 1, shelf + 1, volumn + 1, page + 1)


def print_book_detail(section, wall, shelf, volumn, page):
    print(
        f"""\nSection : {section}\nWall    : {wall}\nShelf   : {shelf}\nVolumn  : {volumn}\nPage    : {page}\n"""
    )


# ---------------------------
# STRING DECRYPTION FUNCTIONS
# ---------------------------
def get_user_int_detail(section_type:str, section_size:int)->int:
    """A function to get the users input, since people are prone to not putting in the right input for whichever reason

    Args:
        section_type (str): the name of the section : wall / shelf / volumn / page
        section_size (int): the size of the section (initalized at the start of the main.py script)

    Returns:
        int: the valid number that we need for successful execution
    """
    detail = None
    while detail == None:
        user_input = input(
            f"Please select a {section_type} range 1 -> {section_size}.\n: "
        )
        try:
            user_int = int(user_input)
        except Exception as error:
            continue

        if user_int <= 0 or user_int > section_size:
            continue

        detail = user_int

    return detail


def get_user_search_location(WALLS: int, SHELVES: int, VOLUMN: int, PAGES: int):
    """Collecting all of the details of the encryption

    Args:
        WALLS (int): size of how many walls are allowed
        SHELVES (int): size of how many shelves are allowed
        VOLUMN (int): size of how many volumns are allowed
        PAGES (int): size of how many pages are allowed

    Returns:
        tuple: all of the details over the encrypted key
    """
    section = input(
        "Please enter the section of the library where you wish to go to.\n: "
    )
    wall = get_user_int_detail("wall", WALLS)
    shelf = get_user_int_detail("shelf", SHELVES)
    volumn = get_user_int_detail("volumn", VOLUMN)
    page = get_user_int_detail("page", PAGES)

    # -1's because computers are not us and start at 0 not 1
    return (section, wall - 1, shelf - 1, volumn - 1, page - 1)


def get_book_content(
    VAILD_CHARACTERS: str,
    VALID_ENCRYPTED_CHARACTERS: str,
    section: str,
    wall: int,
    shelf: int,
    volumn: int,
    page: int,
    WALLS_SPACE: int,
    SHELVES_SPACE: int,
    VOLUMN_SPACE: int,
    PAGES_SPACE: int,
) -> str:
    """Doing the reverse lookup on the encrypted values

    Args:
        VAILD_CHARACTERS (str): an encoding of all of the allowed user inputs
        VALID_ENCRYPTED_CHARACTERS (str): an encoding of all of the allowed characters for the section
        section (str): user input for the section index
        wall (int): user input for the wall index
        shelf (int): user input for the shelf index
        volumn (int): user input for the volumn index
        page (int): user input for the page index
        WALLS_SPACE (int): bit size of how much the wall takes up
        SHELVES_SPACE (int): bit size of how much the shelves takes up
        VOLUMN_SPACE (int): bit size of how much the volumns takes up
        PAGES_SPACE (int): bit size of how much the pages takes up

    Returns:
        str: the decrypted content
    """
    # Do all of the steps, but now reverse

    # 1. The remaning binary space from step 3 is then interpeted in base 10 value
    base_2_details = f'{bin(wall)[2:].rjust(WALLS_SPACE,"0")}{bin(shelf)[2:].rjust(SHELVES_SPACE,"0")}{bin(volumn)[2:].rjust(VOLUMN_SPACE,"0")}{bin(page)[2:].rjust(PAGES_SPACE,"0")}'

    # 2. Base Encrypted Characters -> Base 10
    base_10_section = base_encode_to_base_10(section, VALID_ENCRYPTED_CHARACTERS)

    # 3. the longer section Base 10 -> Base 2
    base_2_section = bin(base_10_section)[2:]

    # 4. Merge total of bits that the walls, shelves, volumns, pages take up
    base_2_encode = f"{base_2_section}{base_2_details}"

    # 2. Base 2 -> Base 10
    base_10_encode = int(base_2_encode, 2)

    # 1. Base 10 -> Base Valid Characters
    content = base_10_to_base_encode(base_10_encode, VAILD_CHARACTERS)

    return content
