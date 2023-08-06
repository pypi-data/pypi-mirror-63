#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Filter IPTV m3u playlists according to customized criteria.

File: main.py
Author: huxuan
Email: i(at)huxuan.org
"""
import argparse
import shutil

from iptvtools import __version__
from iptvtools import exceptions
from iptvtools.config import Config
from iptvtools.constants import defaults
from iptvtools.constants import helps
from iptvtools.models import Playlist


def parse_args():
    """Arguments Parsers."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--min-height', default=defaults.MIN_HEIGHT, type=int,
                        help=helps.MIN_HEIGHT)
    parser.add_argument('-c', '--config', default=defaults.CONFIG,
                        help=helps.CONFIG)
    parser.add_argument('-i', '--inputs', nargs='*', default=defaults.INPUTS,
                        help=helps.INPUTS)
    parser.add_argument('-I', '--interval', default=defaults.INTERVAL,
                        type=int, help=helps.INTERVAL)
    parser.add_argument('-o', '--output', default=defaults.OUTPUT,
                        help=helps.OUTPUT)
    parser.add_argument('-r', '--replace-group-by-source', action='store_true',
                        help=helps.REPLACE_GROUP_BY_SOURCE)
    parser.add_argument('-R', '--resolution-on-title', action='store_true',
                        help=helps.RESOLUTION_ON_TITLE)
    parser.add_argument('-s', '--sort-keys', nargs='*',
                        default=defaults.SORT_KEYS, help=helps.SORT_KEYS)
    parser.add_argument('-t', '--templates', nargs='*',
                        default=defaults.TEMPLATES, help=helps.TEMPLATES)
    parser.add_argument('-T', '--timeout', default=defaults.TIMEOUT, type=int,
                        help=helps.TIMEOUT)
    parser.add_argument('-u', '--udpxy', default=defaults.UDPXY,
                        help=helps.UDPXY)
    parser.add_argument('-v', '--version', action='version',
                        version=__version__)
    return parser.parse_args()


def main():
    """Filter m3u playlists."""
    args = parse_args()

    if args.min_height or args.resolution_on_title:
        if shutil.which('ffprobe') is None:
            raise exceptions.FFmpegNotInstalledError()

    Config.init(args.config)
    playlist = Playlist(args)
    playlist.parse()
    playlist.filter()
    playlist.export()
    if playlist.inaccessible_urls:
        print('Inaccessible Urls:')
        print('\n'.join(sorted(playlist.inaccessible_urls)))
    if playlist.poor_urls:
        print('Poor resolution Urls:')
        print('\n'.join(sorted(playlist.poor_urls)))


if __name__ == '__main__':
    main()
