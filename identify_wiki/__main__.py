import sys
from argparse import ArgumentParser
from multiprocessing import Pool
from time import time

from . import identify_subject


def identify_worker(wid):
    """
    Facilitate multiprocessing and UTF-8 encode the result of an
    identify_subject call.

    :param wid: The wiki ID to call identify_subject on
    :type wid: string

    :return: A comma-separated list containing the wiki ID, its hostname, and
        best-matching subjects
    :rtype: string
    """
    return identify_subject(wid)
    #return identify_subject(wid).encode('utf-8')
    try:
        return identify_subject(wid).encode('utf-8')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        return '%s,ERROR,ERROR' % wid


def get_args():
    parser = ArgumentParser()
    parser.add_argument(
        '-i', '--input', dest='input', type=str, action='store',
        help='Input file containing newline-separated wiki IDs')
    parser.add_argument(
        '-o', '--output', dest='output', type=str, action='store',
        help='Output file to write identified wiki subjects')
    parser.add_argument(
        '-n', '--number', dest='number', type=int, action='store',
        default=5000, help='Number of wikis to iterate over')
    return parser.parse_args()


def main():
    args = get_args()

    start = time()
    with open(args.output, 'w') as f:
        wids = [line.strip() for line in
                open(args.input).readlines()[:args.number]]
        mapped = Pool(processes=8).map_async(identify_worker, wids)
        mapped.wait()
        print >> f, '\n'.join([x for x in mapped.get()])
    end = time()
    total = end - start
    print '%d seconds elapsed' % total


def nonasync_main():
    args = get_args()

    start = time()
    with open(args.output, 'w') as f:
        wids = [line.strip() for line in
                open(args.input).readlines()[:args.number]]
        for wid in wids:
            print >> f, identify_subject(wid)
    end = time()
    total = end - start
    print '%d seconds elapsed' % total

if __name__ == '__main__':
    #main()
    nonasync_main()
