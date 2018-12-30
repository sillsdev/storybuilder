#!/usr/bin/env python3
""" Splits a book of the bible according to the story json object """

import re

import sys

sys.path.insert(0, "../audio_slice")
import slice


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
            book[-1].append(re.sub(r"\\v [0-9]+ ", "", line).strip())
    return book


def flatten(double_list, start_pair, end_pair):
    """ flattens a list of lists from the start to the end """

    if start_pair[0] == end_pair[0]:
        return double_list[start_pair[0]][start_pair[1] : end_pair[1]]
    else:
        return (
            double_list[start_pair[0]][start_pair[1] :]
            + sum(double_list[start_pair[0] + 1 : end_pair[0]], [])
            + double_list[end_pair[0]][: end_pair[1] + 1]
        )


def to_index(string):
    """ turns a one indexed string to a 0 indexed int """
    return int(string) - 1


def split_texts(story, book):
    """
    returns a list of individiaul pages based at the JSON story object and a
    book in the form List[chapter][verse]
    """
    verse_pages = []
    for page in story["pages"]:
        nonnumber = r"[^0-9]"
        start = list(map(to_index, re.split(nonnumber, page["ref_start"])))
        end = list(map(to_index, re.split(nonnumber, page["ref_end"])))

        verse_pages.append(" ".join(flatten(book, start, end)))

    return verse_pages


def to_time_string(seconds):
    """ formats some float quantity of seconds as a time string """
    hours = seconds // (60 * 60)
    minutes = seconds // (60) % 60
    milliseconds = seconds * 1000 % 1000
    seconds = int(seconds) % 60
    return f"{hours}:{minutes}:{seconds}, {milliseconds}"


def subtitle(story, book):
    """
    turn a story json object and a the associated book into a single string
    that represents the appropriate contents of a srt file
    """
    page_texts = split_texts(story, book)
    timings = slice.get_timings(story)
    subtitle = ""
    for (ind, (page, timing)) in enumerate(zip(page_texts, timings)):
        "\n".join(
            "{}\n{} --> {}\n{}".format(
                ind + 1,
                to_time_string(timing[0]),
                to_time_string(timing[1]),
                page,
            )
        )
    return subtitle
