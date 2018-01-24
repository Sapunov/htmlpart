import re


def deduplicate_spaces(text):
    ''' Removes duplicate whitespace characters in text.

    Parameters
    ----------
    text : string of input text.

    Returns
    -------
    result : string without duplicated whitespace characters.

    '''
    result = re.sub(r'(\s){2,}', ' ', text)
    result = result.strip()

    return result
