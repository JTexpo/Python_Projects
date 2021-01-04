spam = ['apple','bananas','tofu','cats']

if __name__ == '__main__':
    first_str = ', '.join(spam[:-1])
    print('{}, and {}'.format(first_str,spam[-1]))
