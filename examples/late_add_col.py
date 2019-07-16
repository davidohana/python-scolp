import datetime

import scolp

s = scolp.Scolp()
s.config.add_columns('date', 'a')
s.config.default_column.type_to_format[datetime.datetime] = '{:%c %Z}'
s.print(datetime.datetime.utcnow(), 'foo')
s.print(datetime.datetime.utcnow(), 'bar')

s.config.add_column('b')
s.print_col_headers()
s.print(datetime.datetime.utcnow(), 'fizz', 'buzz')
s.print(datetime.datetime.utcnow(), 'tom', 'jerry')

