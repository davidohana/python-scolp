import datetime

import scolp


def is_prime(num):
    return 2 in [num, 2 ** num % num]


scolp_cfg = scolp.Config()
scolp_cfg.add_column("time", width=20)
scolp_cfg.add_columns("elapsed",
                      "inspected_count",
                      "prime_count")
scolp_cfg.add_column("last", width=11)
scolp_cfg.add_column("progress", fmt="{:.1%}")
scolp_cfg.header_repeat_row_count_first = 0
scolp_cfg.default_column.type_to_format[datetime.datetime] = "{:%Y-%m-%d %H:%M:%S}"
scolper = scolp.Scolp(scolp_cfg)

prime_count = 0
last_prime = None
i = 500_000_000
target_count = 30
while prime_count < target_count:
    scolper.print(datetime.datetime.now(), scolper.elapsed_since_init(), scolper.row_index + 1)
    if is_prime(i):
        last_prime = i
        prime_count += 1
    progress = prime_count / target_count
    scolper.print(prime_count, last_prime, progress)
    i += 1
