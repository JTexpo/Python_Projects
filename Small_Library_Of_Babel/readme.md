# Small Library of Babel

The library of babel's code is not open sourced, and has lead to some confusion with friends and family on how the website is able to generate all possible strings. This is a theory of what I believe the code to look similar to, as the website is no more than cryptography and demostrates a theoretical set of all strings from 0 -> 3200 characters; however, is only a look-up / encode for the inputs given.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Encode a String (Find a Book)](#encode-a-string-find-a-book)
  - [Decode a String (Find the Contents of a Book)](#decode-a-string-find-the-contents-of-a-book)
- [Contributing](#contributing)
- [Contact](#contact)

## Features

- Dynamic cryptography for generating and encoding strings
- Encoding strings to find corresponding books in the library
- Decoding encoded books to retrieve the original content

## Installation

Ensure that you have Python 3.11 or later installed on your system.

## Usage

To run the application, execute the following command in your terminal:

```
python3 main.py
```

### Encode a String (Find a Book)
1. Upon running the application, you will see the following prompt:
```
Welcome to JTexpo's rendition on the library of babel.
What would you like todo?
1. Search for book with string
2. Search for book with section / wall / shelf / volumn / page
0. Leave
```
2. Select option 1 to search for a book by a specific string.
```
: 1
```
3. Enter the content you are looking for. For example:
```
What is the content that you are looking for?
: this is a test
```
4. The application will provide you with the book's location information, including the section, wall, shelf, volume, and page:
```
Section : bTw_2hJml[Jt9It'6wGf/!n:K4yLu!3)P-A5lTXz"gH}!ast#44Dy)|<oac&tDZq#?2suSBx62eDCH
Wall    : 3
Shelf   : 1
Volumn  : 14
Page    : 429
```

### Decode a String (Find the Contents of a Book)
1. Upon running the application, you will see the following prompt:
```
Welcome to JTexpo's rendition on the library of babel.
What would you like todo?
1. Search for book with string
2. Search for book with section / wall / shelf / volumn / page
0. Leave
```
2. Select option 1 to search for a book by a specific string.
```
: 1
```
3. Enter the section of the library you wish to access. For example:
```
Please enter the section of the library where you wish to go to.
: bTw_2hJml[Jt9It'6wGf/!n:K4yLu!3)P-A5lTXz"gH}!ast#44Dy)|<oac&tDZq#?2suSBx62eDCH
```
4. Provide the range for the wall, shelf, volume, and page as prompted.
```
Please select a wall range 1 -> 4.
: 3
Please select a shelf range 1 -> 8.
: 1
Please select a volumn range 1 -> 32.
: 14
Please select a page range 1 -> 512.
: 429
```
5. The application will display the content of the book:
```
That book contains the following content:
this is a test     
```

## Contributing

Contributions to the Small Library of Babel project are welcome! If you have any bug reports, feature suggestions, or code contributions, please make a request!

## Contact

If you have any questions, feedback, or need further assistance, please feel free to reach out:

GitHub : Here!
YouTube : https://www.youtube.com/@jtexpo

We appreciate your interest and support!
