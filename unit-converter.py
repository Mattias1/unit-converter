#
#  Unit converter
# ================
#
# A commandline unit-converter.
# Just take the value to convert as input, nothing more,
#   and output all things I might want to convert it to.
#
import sys
import re
import time

times = 'seconds, minutes, hours, days, weeks, years'
velocities = 'm/s, km/h, mph'
accelerations = 'g, m/s2, m/min2, mph2, km/h2, m/h2'
temperatures = 'C, K, F'
distances = 'milimeters, centimeters, kilometers, inches, feet, yards, miles, meters'
units = [times, velocities, accelerations, temperatures, distances]


def main():
    # Get the input (from command line if present otherwise from input)
    s = ''.join(sys.argv[1:]) or input('Enter a number with unit to convert: ')
    s = s.replace(' ', '')
    s = substituteunits(s)
    # Try to convert and print the output
    try:
        value, unit = parse(s)
        baseValue = toBase(value, unit)
        tuples = fromBase(baseValue, unit)
        for v, u in tuples:
            if v == int(v):
                print('  {} {}'.format(int(v), u))
            else:
                print('  {0:.2f} {1}'.format(v, u))
        # Special case for the unix time epoch
        if unit in times:
            unixtime = int(time.time()) + int(baseValue)
            print('Unix time {} {} from now: {}'.format(value, unit, unixtime))
    except:
        print('Conversion fail')


def toBase(value, unit):
    # Convert the value with it's unit to the base unit of this type (aka, velocity or temp)
    convert = {
        'seconds': value,
        'minutes': value * 60,
        'hours': value * 3600,
        'days': value * 86400,
        'weeks': value * 604800,
        'years': value * 86400 * 365.242,

        'm/s': value,
        'km/h': value / 3.6,
        'mph': value * 0.44704,

        'g': value * 9.80665,
        'm/s2': value,
        'm/min2': value / 3600.0,
        'mph2': value / 8053.0,
        'km/h2': value / 12960.0,
        'm/h2': value / 12960000.0,

        'C': value,
        'K': value - 273.15,
        'F': (value - 32) / 1.8,

        'milimeters': value,
        'centimeters': value * 10,
        'meters': value * 1000,
        'kilometers': value * 1000000,
        'inches': value * 25.4,
        'feet': value * 304.8,
        'yards': value * 914.4,
        'miles': value * 1609344
    }
    return convert[unit]


def fromBase(value, unit):
    # Convert this base-unit value to all possible other units of this type (aka, velocity or temp)
    convert = {
        'seconds': value,
        'minutes': value / 60.0,
        'hours': value / 3600.0,
        'days': value / 86400.0,
        'weeks': value / 604800.0,
        'years': value / (86400 * 365.242),

        'm/s': value,
        'km/h': value * 3.6,
        'mph': value / 0.44704,

        'g': value / 9.80665,
        'm/s2': value,
        'm/min2': value * 3600,
        'mph2': value * 8053,
        'km/h2': value * 12960,
        'm/h2': value * 12960000,

        'C': value,
        'K': value + 273.15,
        'F': value * 1.8 + 32,

        'milimeters': value,
        'centimeters': value / 10.0,
        'meters': value / 1000.0,
        'kilometers': value / 1000000.0,
        'inches': value / 25.4,
        'feet': value / 304.8,
        'yards': value / 914.4,
        'miles': value / 1609344
    }
    for unitstring in units:
        unitlist = unitstring.split(', ')
        if unit in unitlist:
            return [(convert[u], u) for u in unitlist]


def parse(s):
    for unit in ', '.join(units).split(', '):
        if s[-len(unit):].lower() == unit.lower():
            return (eval(s[:-len(unit)]), unit)
    return (0, '')


def substituteunits(s):
    subs = {
        's': 'seconds',
        'second': 'seconds',
        'sec': 'seconds',
        'secs': 'seconds',
        'minute': 'minutes',
        'min': 'minutes',
        'mins': 'minutes',
        'h': 'hours',
        'hour': 'hours',
        'd': 'days',
        'day': 'days',
        'w': 'weeks',
        'week': 'weeks',
        'y': 'years',
        'year': 'years',

        'mm': 'milimeters',
        'milimeter': 'milimeters',
        'cm': 'centimeters',
        'centimeter': 'centimeters',
        'm': 'meters',
        'meter': 'meters',
        'km': 'kilometers',
        'kilometer': 'kilometers',
        "''": 'inches',
        'inch': 'inches',
        'foot': 'feet',
        "'": 'feet',
        'ft': 'feet',
        'yd': 'yards',
        'yard': 'yards',
        'mi': 'miles',
        'mile': 'miles',

        'celcius': 'C',
        'kelvin': 'K',
        'fahrenheit': 'F'
    }
    for key, value in subs.items():
        s = re.sub('(.*[0-9]){}$'.format(key), '\\1{}'.format(value), s)
    return s


if __name__ == '__main__':
    main()
