#!/usr/bin/python

"""Reads a har file from the filesystem, converts to CSV, then dumps to
stdout.
"""
import argparse
import json
import datetime
import pytz
from dateutil.parser import parse
from urlparse import urlparse

def main(harfile_path, host_filter):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    harfile = open(harfile_path)
    harfile_json = json.loads(harfile.read())
    i = 0
    end = datetime.datetime(2009,10,12,0,0,0,0,pytz.UTC)

    print "#,url,hostname,size_bytes,size_kb,mimetype,start_time,end_time,total_time,time_blocked,time_dns,time_connect, time_send,time_wait,time_receive,time_ssl"

    for entry in harfile_json['log']['entries']:
        i = i + 1

        """ Parse URL """
        url = entry['request']['url']
        urlparts = urlparse(entry['request']['url'])

        if host_filter:
            if host_filter not in urlparts.hostname:
                continue

        """ Parse size """
        size_bytes = entry['response']['bodySize']
        size_kilobytes = float(entry['response']['bodySize'])/1024
        
        """ Parse mimetype """
        mimetype = 'unknown'
        if 'mimeType' in entry['response']['content']:
            mimetype = entry['response']['content']['mimeType']

        """ Parse timings """
        start_time = parse(entry['startedDateTime'])
        if i == 1:
            begin = start_time

        total_time = 0

        time_blocked = entry['timings']['blocked']
        if time_blocked != -1:
            total_time += time_blocked

        time_dns = entry['timings']['dns']
        if time_dns != -1:
            total_time += time_dns

        time_connect = entry['timings']['connect']
        if time_connect != -1:
            total_time += time_connect

        time_send = entry['timings']['send']
        total_time += time_send

        time_wait = entry['timings']['wait']
        total_time += time_wait

        time_receive = entry['timings']['receive']
        total_time += time_receive

        time_ssl = entry['timings']['ssl']
        if time_ssl != -1:
            total_time += time_ssl

        end_time = start_time + datetime.timedelta(milliseconds=total_time)
        if end_time > end:
            end = end_time

        print '%s,"%s",%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s' % (i, url,
                urlparts.hostname, size_bytes, size_kilobytes, mimetype,
                start_time,end_time,total_time, time_blocked, time_dns,
                time_connect, time_send, time_wait, time_receive, time_ssl) 

    print ''
    print 'start time: %s' % (begin)
    print 'end time: %s' % (end)
    print 'duration: %s' % (end - begin)

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='parsehar',
        description='Parse .har files into comma separated values (csv).')
    argparser.add_argument('harfile', type=str, nargs=1,
                        help='path to harfile to be processed.')
    argparser.add_argument('-f', '--filter', type=str, required=False,
            dest='host_filter', help='only show entries that match this hostname.')
    args = argparser.parse_args()

    main(args.harfile[0], args.host_filter)
