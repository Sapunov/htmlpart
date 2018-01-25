import lxml.html

# Spaghetti imports from http://lxml.de/tutorial.html
try:
    from lxml import etree
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
        except ImportError:
            try:
                # Normal cElementTree install
                import cElementTree as etree
            except ImportError:
                import elementtree.ElementTree as etree

from . import common


''' Tags that are usually displayed as blocks and tags which
    are rarely used in the middle of the words.

'''
DETACHABLE_TAGS = set((
    'abbr', 'acronym', 'address', 'article', 'aside', 'bdi', 'bdo',
    'blockquote', 'body', 'button', 'canvas', 'caption', 'center',
    'cite', 'code', 'comment', 'dd', 'del', 'details', 'dfn',
    'dir', 'div', 'dl', 'dt', 'embed', 'fieldset', 'figcaption',
    'figure', 'footer', 'form', 'frame', 'h1', 'h2', 'h3', 'h4',
    'h5', 'h6', 'header', 'hgroup', 'iframe', 'ins', 'isindex',
    'kbd', 'legend', 'li', 'main', 'map', 'marquee', 'menu',
    'meter', 'nav', 'noembed', 'noframes', 'noscript', 'object',
    'ol', 'optgroup', 'option', 'output', 'p', 'plaintext',
    'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 'section',
    'select', 'summary', 'table', 'tbody', 'td', 'textarea',
    'tfoot', 'th', 'thead', 'time', 'tr', 'ul', 'xmp'
))


''' Tags which is have no text inside.

'''
USELESS_TAGS = set((
    'script', 'style', 'link', 'meta', 'audio', 'applet',
    'base', 'basefont', 'bgsound', 'col', 'colgroup', 'command',
    'datalist', 'frameset', 'frame', 'iframe', 'keygen',
    'param', 'source'
))


def lxml_remove_tags(lxml_tree, tags_to_remove=USELESS_TAGS,
                     remove_comments=True):
    ''' Remove specific tags from lxml tree instance.

    Parameters
    ----------
    lxml_tree : instance of lxml.html.HtmlElement to clean
                from some tags.

    tags_to_remove : array-like of tag names to remove.

    remove_comments : bool, whether to remove comments from
                      tree.

    Returns
    -------
    lxml_tree : instance of lxml.html.HtmlElement without
                `tags_to_remove`.

    '''
    if not tags_to_remove is None:
        for element in lxml_tree.iter():
            if element.tag in tags_to_remove:
                element.getparent().remove(element)

    if remove_comments:
        for element in lxml_tree.iter():
            if isinstance(element, lxml.html.HtmlComment):
                element.getparent().remove(element)

    return lxml_tree


def html_remove_tags(html_string, tags_to_remove=USELESS_TAGS,
                     remove_comments=True):
    ''' Remove specific tags from passed html.

    Parameters
    ----------
    html_string : html string to clean from `tags_to_remove`.

    tags_to_remove : array-like of tag names to remove.

    remove_comments : bool, whether to remove comments from
                      tree.

    Returns
    -------
    clean_html : unicode string with html without
                 `tags_to_remove`.

    '''

    lxml_tree = lxml.html.fromstring(html_string)
    lxml_tree = lxml_remove_tags(lxml_tree, tags_to_remove, remove_comments)

    clean_html = etree.tounicode(lxml_tree)

    return clean_html


def separate_detachable(lxml_tree, tags_to_process=DETACHABLE_TAGS):
    ''' Adds framing whitespaces to the `tags_to_process`.

        The main idea here to add whitespaces to the left
        and right corners of the inside tag text and then
        use standard lxml function text_content() with
        deduplicate_spaces() afterwards. It's important to
        separate only detachable tags due to stay inner word
        formatting correct (Ex.: <p>p<big>Y</big>thon</p>).

    Parameters
    ----------
    lxml_tree : instance of lxml.html.HtmlElement to process.

    tags_to_process : array-like list of detachable tags.
                      By default it's equals to
                      `DETACHABLE_TAGS`, my own choice of
                      necessary tags from whole list of
                      html tags.

    Returns
    -------
    lxml_tree : instance of lxml.html.HtmlElement
                after processing.

    '''

    if not tags_to_process:
        return lxml_tree

    assert isinstance(tags_to_process, (list, set, tuple)), \
        '`tags_to_process` must be one of the [list, set, typle]'

    # For speed
    if not isinstance(tags_to_process, set):
        tags_to_process = set(tags_to_process)

    for element in lxml_tree.iter():
        if not isinstance(element, lxml.html.HtmlComment) \
                and element.tag in tags_to_process:
            element.text = ' {0} '.format(element.text or '')

    return lxml_tree


def lxml_extract_text(lxml_tree):
    ''' Extracts text from lxml tree instance.

    Parameters
    ----------
    lxml_tree : instance of lxml.html.HtmlElement to extract
                text.

    Returns
    -------
    text : string of plain text.

    '''

    lxml_tree = lxml_remove_tags(lxml_tree)
    lxml_tree = separate_detachable(lxml_tree)

    text = lxml_tree.text_content()
    text = common.deduplicate_spaces(text)

    return text


def html_extract_text(html_string):
    ''' Extracts text from lxml tree instance.

    Parameters
    ----------
    html_string : html string to extract text.

    Returns
    -------
    text : string of plain text.

    '''
    lxml_tree = lxml.html.fromstring(html_string)

    text = lxml_extract_text(lxml_tree)

    return text
