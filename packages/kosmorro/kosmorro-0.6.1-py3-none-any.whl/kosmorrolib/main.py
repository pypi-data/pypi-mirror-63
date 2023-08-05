#!/usr/bin/env python3

#    Kosmorro - Compute The Next Ephemerides
#    Copyright (C) 2019  Jérôme Deuchnord <jerome@deuchnord.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import locale
import re
import sys

from datetime import date
from termcolor import colored

from kosmorrolib.version import VERSION
from kosmorrolib import dumper
from kosmorrolib import core
from kosmorrolib import events
from kosmorrolib.i18n import _
from .ephemerides import EphemeridesComputer, Position
from .exceptions import UnavailableFeatureError


def main():
    output_formats = get_dumpers()
    args = get_args(list(output_formats.keys()))

    if args.special_action is not None:
        return 0 if args.special_action() else 1

    year = args.year
    month = args.month
    day = args.day

    compute_date = date(year, month, day)

    if day is not None and month is None:
        month = date.today().month

    if args.latitude is None or args.longitude is None:
        position = None
    else:
        position = Position(args.latitude, args.longitude)

    if args.format == 'pdf':
        print(_('Save the planet and paper!\n'
                'Consider printing you PDF document only if really necessary, and use the other side of the sheet.'))
        if position is None:
            print()
            print(colored(_("PDF output will not contain the ephemerides, because you didn't provide the observation "
                            "coordinate."), 'yellow'))

    try:
        ephemeris = EphemeridesComputer(position)
        ephemerides = ephemeris.compute_ephemerides(year, month, day)

        events_list = events.search_events(compute_date)

        selected_dumper = output_formats[args.format](ephemerides, events_list,
                                                      date=compute_date, timezone=args.timezone,
                                                      with_colors=args.colors)
        output = selected_dumper.to_string()
    except UnavailableFeatureError as error:
        print(colored(error.msg, 'red'))
        return 2

    if args.output is not None:
        try:
            with open(args.output, 'wb') as output_file:
                output_file.write(output)
        except OSError as error:
            print(_('Could not save the output in "{path}": {error}').format(path=args.output,
                                                                             error=error.strerror))
    elif not selected_dumper.is_file_output_needed():
        print(output)
    else:
        print(colored(_('Selected output format needs an output file (--output).'), color='red'))
        return 1

    return 0


def get_dumpers() -> {str: dumper.Dumper}:
    return {
        'text': dumper.TextDumper,
        'json': dumper.JsonDumper,
        'pdf': dumper.PdfDumper
    }


def output_version() -> bool:
    python_version = '%d.%d.%d' % (sys.version_info[0], sys.version_info[1], sys.version_info[2])
    print('Kosmorro %s' % VERSION)
    print(_('Running on Python {python_version}').format(python_version=python_version))

    return True


def clear_cache() -> bool:
    confirm = input(_("Do you really want to clear Kosmorro's cache? [yN] ")).upper()
    if re.match(locale.nl_langinfo(locale.YESEXPR), confirm) is not None:
        try:
            core.clear_cache()
        except FileNotFoundError:
            pass
    elif confirm != '' and re.match(locale.nl_langinfo(locale.NOEXPR), confirm) is None:
        print(_('Answer did not match expected options, cache not cleared.'))
        return False

    return True


def get_args(output_formats: [str]):
    today = date.today()

    parser = argparse.ArgumentParser(description=_('Compute the ephemerides and the events for a given date,'
                                                   ' at a given position on Earth.'),
                                     epilog=_('By default, only the events will be computed for today ({date}).\n'
                                              'To compute also the ephemerides, latitude and longitude arguments'
                                              ' are needed.').format(date=today.strftime(dumper.FULL_DATE_FORMAT)))

    parser.add_argument('--version', '-v', dest='special_action', action='store_const', const=output_version,
                        default=None, help=_('Show the program version'))
    parser.add_argument('--clear-cache', dest='special_action', action='store_const', const=clear_cache, default=None,
                        help=_('Delete all the files Kosmorro stored in the cache.'))
    parser.add_argument('--format', '-f', type=str, default=output_formats[0], choices=output_formats,
                        help=_('The format under which the information have to be output'))
    parser.add_argument('--latitude', '-lat', type=float, default=None,
                        help=_("The observer's latitude on Earth"))
    parser.add_argument('--longitude', '-lon', type=float, default=None,
                        help=_("The observer's longitude on Earth"))
    parser.add_argument('--day', '-d', type=int, default=today.day,
                        help=_('A number between 1 and 28, 29, 30 or 31 (depending on the month). The day you want to '
                               ' compute the ephemerides for. Defaults to {default_day} (the current day).').format(
                                   default_day=today.day))
    parser.add_argument('--month', '-m', type=int, default=today.month,
                        help=_('A number between 1 and 12. The month you want to compute the ephemerides for.'
                               ' Defaults to {default_month} (the current month).').format(default_month=today.month))
    parser.add_argument('--year', '-y', type=int, default=today.year,
                        help=_('The year you want to compute the ephemerides for.'
                               ' Defaults to {default_year} (the current year).').format(default_year=today.year))
    parser.add_argument('--timezone', '-t', type=int, default=0,
                        help=_('The timezone to display the hours in (e.g. 2 for UTC+2 or -3 for UTC-3).'))
    parser.add_argument('--no-colors', dest='colors', action='store_false',
                        help=_('Disable the colors in the console.'))
    parser.add_argument('--output', '-o', type=str, default=None,
                        help=_('A file to export the output to. If not given, the standard output is used. '
                               'This argument is needed for PDF format.'))

    return parser.parse_args()
