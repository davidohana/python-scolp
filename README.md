# Scolp

## Introduction

Scolp is Streaming Column Printer for Python 3.6 or later.

Scolp let you easily print masses of tabular data in a streaming fashion. It is perfect for apps that need to print progress reports in columns.

Main features:

* Auto-adjusting column width according to the largest value so far or column header width.

* Control verbosity of printing by:
    - printing ``1`` of each ``n`` rows
    - printing no more than ``1`` row per ``n`` seconds

* Control format of printed values by:
    - setting global defaults
    - setting defaults per variable type (``int``, ``float``, ``str``, ``datetime``)
    - setting explicit formatting per column

* Control alignment of printed values:
    - left
    - right
    - center
    - auto: numbers to the right, strings or other types to the left.

* Control cosmetics of columns (initial width, padding fill char, alignment, and more..) by:
    - setting global defaults
    - setting explicit formatting per column

* Control column title printing style:
    - Inline in each row
    - As headers, repeating each n rows

* Easily print row count or time since execution started without need to keep track of those values yourself.

## Examples

#### Example 1

Lets build a program that find prime numbers. We will print the count of primes
we found so far and the last prime found.

```python
import datetime, scolp

def is_prime(num):
    return 2 in [num, 2 ** num % num]

# define columns
scolp_cfg = scolp.Config()
scolp_cfg.add_column("time")
scolp_cfg.add_column("elapsed")
scolp_cfg.add_column("inspected_count")
scolp_cfg.add_column("prime_count")
scolp_cfg.add_column("last")
scolp_cfg.add_column("progress %")
scolp_cfg.output_each_n_seconds = 1
scolper = scolp.Scolp(scolp_cfg)

prime_count = 0
last_prime = None
i = 9_999_800
target_count = 30
while prime_count < target_count:
    if is_prime(i):
        last_prime = i
        prime_count += 1
    progress = prime_count / target_count * 100
    scolper.print(datetime.datetime.now(), scolper.elapsed_since_init(),
                  scolper.row_index + 1, prime_count, last_prime, progress)
    i += 1
```

Output: 

(Note how the header repeats, the column width auto-expanding and the numbers are aligned to the right)

```
time    |elapsed |inspected_count|prime_count|last    |progress %
--------|--------|---------------|-----------|--------|----------
2019-06-05 11:49:31.271191|0:00:00 |              1|          0|None    |     0.000

time                      |elapsed |inspected_count|prime_count|last    |progress %
--------------------------|--------|---------------|-----------|--------|----------
2019-06-05 11:49:32.306225|0:00:01 |             27|          1|9,999,823|     3.333
2019-06-05 11:49:33.325694|0:00:02 |             53|          1|9,999,823|     3.333
2019-06-05 11:49:34.341678|0:00:03 |             79|          3|9,999,877|    10.000
2019-06-05 11:49:35.378966|0:00:04 |            105|          6|9,999,901|    20.000
2019-06-05 11:49:36.399298|0:00:05 |            131|          8|9,999,929|    26.667
2019-06-05 11:49:37.415522|0:00:06 |            157|         11|9,999,943|    36.667
2019-06-05 11:49:38.450551|0:00:07 |            183|         13|9,999,973|    43.333
2019-06-05 11:49:39.478987|0:00:08 |            209|         14|9,999,991|    46.667
2019-06-05 11:49:40.485409|0:00:09 |            233|         15|10,000,019|    50.000

time                      |elapsed |inspected_count|prime_count|last      |progress %
--------------------------|--------|---------------|-----------|----------|----------
2019-06-05 11:49:41.508298|0:00:10 |            259|         15|10,000,019|    50.000
2019-06-05 11:49:42.543115|0:00:11 |            283|         16|10,000,079|    53.333
2019-06-05 11:49:43.555733|0:00:12 |            306|         17|10,000,103|    56.667
2019-06-05 11:49:44.572379|0:00:13 |            328|         18|10,000,121|    60.000
2019-06-05 11:49:45.574066|0:00:14 |            349|         20|10,000,141|    66.667
2019-06-05 11:49:46.583462|0:00:15 |            372|         21|10,000,169|    70.000
2019-06-05 11:49:47.594724|0:00:16 |            396|         22|10,000,189|    73.333
2019-06-05 11:49:48.639124|0:00:17 |            420|         22|10,000,189|    73.333
2019-06-05 11:49:49.661211|0:00:18 |            441|         24|10,000,229|    80.000
2019-06-05 11:49:50.691037|0:00:19 |            463|         27|10,000,261|    90.000

time                      |elapsed |inspected_count|prime_count|last      |progress %
--------------------------|--------|---------------|-----------|----------|----------
2019-06-05 11:49:51.721844|0:00:20 |            487|         28|10,000,271|    93.333
2019-06-05 11:49:52.733437|0:00:22 |            510|         29|10,000,303|    96.667
2019-06-05 11:49:53.750463|0:00:23 |            534|         29|10,000,303|    96.667
```

#### Example 2

Now, lets change the code of the previous example to add a bit of custom formatting:

```python
scolp_cfg = scolp.Config()
scolp_cfg.add_column("time", width=20)
scolp_cfg.add_column("elapsed")
scolp_cfg.add_column("inspected_count")
scolp_cfg.add_column("prime_count")
scolp_cfg.add_column("last", width=11)
scolp_cfg.add_column("progress", fmt="{:.1%}")
scolp_cfg.output_each_n_seconds = 1
scolp_cfg.header_repeat_row_count_first = 0
scolp_cfg.default_column.column_separator = " "
scolp_cfg.default_column.type_to_format[datetime.datetime] = "{:%Y-%m-%d %H:%M:%S}"
scolper = scolp.Scolp(scolp_cfg)

prime_count = 0
last_prime = None
i = 9_999_800
target_count = 30
while prime_count < target_count:
    if is_prime(i):
        last_prime = i
        prime_count += 1
    progress = prime_count / target_count
    scolper.print(datetime.datetime.now(), scolper.elapsed_since_init(),
                    scolper.row_index + 1, prime_count, last_prime, progress)
i += 1
```

Output:

```
time                 elapsed  inspected_count prime_count last        progress
-------------------- -------- --------------- ----------- ----------- --------
2019-06-05 11:54:46  0:00:00                1           0 None            0.0%
2019-06-05 11:54:47  0:00:01               23           0 None            0.0%
2019-06-05 11:54:48  0:00:02               45           1   9,999,823     3.3%
2019-06-05 11:54:49  0:00:03               67           2   9,999,863     6.7%
2019-06-05 11:54:50  0:00:04               90           5   9,999,889    16.7%
2019-06-05 11:54:51  0:00:05              115           7   9,999,907    23.3%
2019-06-05 11:54:52  0:00:06              139          10   9,999,937    33.3%
2019-06-05 11:54:53  0:00:07              164          11   9,999,943    36.7%
2019-06-05 11:54:54  0:00:08              188          13   9,999,973    43.3%
2019-06-05 11:54:55  0:00:09              212          14   9,999,991    46.7%

time                 elapsed  inspected_count prime_count last        progress
-------------------- -------- --------------- ----------- ----------- --------
2019-06-05 11:54:56  0:00:10              237          15  10,000,019    50.0%
2019-06-05 11:54:57  0:00:11              261          15  10,000,019    50.0%
2019-06-05 11:54:58  0:00:12              284          16  10,000,079    53.3%
2019-06-05 11:54:59  0:00:13              308          17  10,000,103    56.7%
2019-06-05 11:55:00  0:00:14              331          18  10,000,121    60.0%
2019-06-05 11:55:01  0:00:15              355          20  10,000,141    66.7%
2019-06-05 11:55:02  0:00:16              379          21  10,000,169    70.0%
2019-06-05 11:55:03  0:00:17              403          22  10,000,189    73.3%
2019-06-05 11:55:04  0:00:18              426          23  10,000,223    76.7%
2019-06-05 11:55:05  0:00:20              448          25  10,000,247    83.3%

time                 elapsed  inspected_count prime_count last        progress
-------------------- -------- --------------- ----------- ----------- --------
2019-06-05 11:55:06  0:00:21              471          27  10,000,261    90.0%
2019-06-05 11:55:07  0:00:22              493          28  10,000,271    93.3%
2019-06-05 11:55:08  0:00:23              516          29  10,000,303    96.7%
2019-06-05 11:55:09  0:00:24              539          29  10,000,303    96.7%
```

#### Example 3

Lets build an HTTP big-file downloader.

```python
import datetime, urllib3, scolp

url = "http://speedtest.tele2.net/1GB.zip"
path = "downloaded.tmp"
chunk_size_bytes = 1000

scolp_cfg = scolp.Config()
scolp_cfg.add_column("time", fmt="{:%H:%M:%S}")
scolp_cfg.add_column("elapsed")
scolp_cfg.add_column("downloaded", width=16, fmt="{:,} B")
col = scolp_cfg.add_column("speed", width=14, pad_align=scolp.Alignment.RIGHT)
col.type_to_format = {float: "{:,.1f} kB/s"}

scolp_cfg.output_each_n_seconds = 1
scolp_cfg.title_mode = scolp.TitleMode.INLINE
scolp_cfg.default_column.column_separator = "  |  "
scolper = scolp.Scolp(scolp_cfg)

http = urllib3.PoolManager()
r = http.request('GET', url, preload_content=False)

dl_bytes = 0

def progress_update():
    elapsed_sec = scolper.elapsed_since_init().total_seconds()
    speed_kbps = dl_bytes / elapsed_sec / 1000 if elapsed_sec > 0 else "unknown"
    scolper.print(datetime.datetime.now(), scolper.elapsed_since_init(), dl_bytes, speed_kbps)

with open(path, 'wb') as out:
    while True:
        data = r.read(chunk_size_bytes)
        if not data:
            break
        out.write(data)
        dl_bytes += len(data)
        progress_update()

scolper.force_print_next_row()
progress_update()
r.release_conn()
```

Output:

```
time=14:30:11  |  elapsed=0:00:00   |  downloaded=         1,000 B  |  speed=       unknown
time=14:30:12  |  elapsed=0:00:01   |  downloaded=       801,000 B  |  speed=    801.0 kB/s
time=14:30:13  |  elapsed=0:00:02   |  downloaded=     1,743,000 B  |  speed=    871.5 kB/s
time=14:30:14  |  elapsed=0:00:03   |  downloaded=     2,758,000 B  |  speed=    919.3 kB/s
time=14:30:15  |  elapsed=0:00:04   |  downloaded=     3,779,000 B  |  speed=    944.8 kB/s
time=14:30:16  |  elapsed=0:00:05   |  downloaded=     4,794,000 B  |  speed=    958.8 kB/s
time=14:30:17  |  elapsed=0:00:06   |  downloaded=     5,809,000 B  |  speed=    968.2 kB/s
time=14:30:18  |  elapsed=0:00:07   |  downloaded=     6,824,000 B  |  speed=    974.9 kB/s
time=14:30:19  |  elapsed=0:00:08   |  downloaded=     7,839,000 B  |  speed=    979.9 kB/s
time=14:30:20  |  elapsed=0:00:09   |  downloaded=     8,857,000 B  |  speed=    984.1 kB/s
time=14:30:21  |  elapsed=0:00:10   |  downloaded=     9,799,000 B  |  speed=    979.9 kB/s
time=14:30:22  |  elapsed=0:00:11   |  downloaded=    10,814,000 B  |  speed=    983.1 kB/s
time=14:30:23  |  elapsed=0:00:12   |  downloaded=    11,838,000 B  |  speed=    986.5 kB/s
time=14:30:24  |  elapsed=0:00:13   |  downloaded=    12,855,000 B  |  speed=    988.8 kB/s
time=14:30:25  |  elapsed=0:00:14   |  downloaded=    13,870,000 B  |  speed=    990.7 kB/s
time=14:30:26  |  elapsed=0:00:15   |  downloaded=    14,891,000 B  |  speed=    992.7 kB/s
time=14:30:27  |  elapsed=0:00:16   |  downloaded=    15,906,000 B  |  speed=    994.1 kB/s
time=14:30:28  |  elapsed=0:00:18   |  downloaded=    25,600,000 B  |  speed=  1,422.2 kB/s
time=14:30:29  |  elapsed=0:00:19   |  downloaded=    37,146,000 B  |  speed=  1,955.1 kB/s
time=14:30:30  |  elapsed=0:00:20   |  downloaded=    47,847,000 B  |  speed=  2,392.3 kB/s
time=14:30:31  |  elapsed=0:00:21   |  downloaded=    60,962,000 B  |  speed=  2,903.0 kB/s
time=14:30:32  |  elapsed=0:00:22   |  downloaded=    72,931,000 B  |  speed=  3,315.0 kB/s
time=14:30:33  |  elapsed=0:00:23   |  downloaded=    85,094,000 B  |  speed=  3,699.7 kB/s
time=14:30:34  |  elapsed=0:00:24   |  downloaded=   104,857,600 B  |  speed=  4,369.1 kB/s
```


# Requirements

Scolp has no 3rd party requirements other than Python 3.6 or later.


# Getting Started

Scolp is available via PyPi and can be installed using:

```pip install scolp```.

