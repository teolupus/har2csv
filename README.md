# har2csv

Python script that converts har2csv for website performance analysis.

./har2csv.py harfile [-f filter-host]

Use filter-host to match the hostname in the URL with the provided string. Only
entries that match will be processed.

CSV output includes: id, url, urlparts.hostname, size-bytes, size-kilobytes, mimetype, start-time,end-time,total-time, time-blocked, time-dns, time-connect, time-send, time-wait, time-receive, time-ssl.
