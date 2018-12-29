#!/usr/bin/env python3
""" Splits a book of the bible according to the story json object """

import re


def gen_book(bookfile):
    """
    Takes an opened SFM file and reads it into a list of lists, such that any
    verse can be indexed by chapter and verse in the format
    `book[chapter][verse]`
    """
    book = []
    for line in bookfile:
        if re.match(r"\\c", line):
            book.append([])
        elif re.match(r"\\v", line):
            book[-1].append(re.sub(r"\\v [0-9]+ ", "", line))
    return book


def flatten(double_list, start_pair, end_pair):
    """ flattens a list of lists from the start to the end """
    return (
        double_list[start_pair[0]][start_pair[1] :]
        + sum(double_list[start_pair[0] + 1 : end_pair[0]], [])
        + double_list[end_pair[0]][: end_pair[1]]
    )


def split_texts(story, book):
    """
    returns a list of individiaul pages based at the JSON story object and a
    book in the form List[chapter][verse]
    """
    verse_pages = []
    for page in story["pages"]:
        nonnumber = r"[^0-9]"
        start = list(map(int, re.split(nonnumber, page["ref_start"])))
        end = list(map(int, re.split(nonnumber, page["ref_end"])))

        verse_pages.append(sum(flatten(book, start, end), ""))

    return verse_pages
