import datetime

import scolp


def is_prime(num):
    return 2 in [num, 2 ** num % num]


scolper = scolp.Scolp()
scolper.config.add_columns("time", "elapsed", "inspected_count", "prime_count", "last", "progress %")
scolper.config.output_each_n_seconds = 1

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
