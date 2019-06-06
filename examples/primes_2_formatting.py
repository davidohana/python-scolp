import datetime

import scolp


def is_prime(num):
    return 2 in [num, 2 ** num % num]


scolper = scolp.Scolp()
scolper.config.add_column("time", width=20)
scolper.config.add_columns("elapsed",
                           "inspected_count",
                           "prime_count")
scolper.config.add_column("last", width=11)
scolper.config.add_column("progress", fmt="{:.1%}")
scolper.config.output_each_n_seconds = 1
scolper.config.header_repeat_row_count_first = 0
scolper.config.default_column.column_separator = " "
scolper.config.default_column.type_to_format[datetime.datetime] = "{:%Y-%m-%d %H:%M:%S}"

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
