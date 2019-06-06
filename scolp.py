import copy
import datetime
import numbers
from enum import Enum, auto
from typing import List, Dict


class TitleMode(Enum):
    INLINE = auto()
    HEADER = auto()
    NONE = auto()


class Alignment(Enum):
    LEFT = auto()
    RIGHT = auto()
    CENTER = auto()
    AUTO = auto()


class Column:
    # noinspection PyTypeChecker
    def __init__(self):
        self.title = ""
        self.format: str = None
        self.width: int = None
        self.title_to_value_separator: str = None
        self.pad_fill_char: str = None
        self.pad_align: str = None
        self.column_separator: str = None
        self.type_to_format: Dict[type, str] = None


class Config:

    def __init__(self):
        self.columns: List[Column] = []

        self.output_each_n_rows = 1
        self.output_each_n_seconds = 0

        self.title_mode = TitleMode.HEADER
        self.header_repeat_row_count = 10
        self.header_repeat_row_count_first = 1
        self.header_line_char = "-"

        self.default_column = Column()
        self.default_column.width = 8
        self.default_column.format = None
        self.default_column.title_to_value_separator = "="
        self.default_column.pad_fill_char = " "
        self.default_column.column_separator = "|"
        self.default_column.pad_align = Alignment.AUTO
        self.default_column.type_to_format = {
            int: "{:,}",
            float: "{:,.3f}",
        }

        self.print_func = self._print_impl

    def add_column(self,
                   title: str, fmt=None, width=None,
                   title_to_value_separator=None, pad_fill_char=None, pad_align=None,
                   column_separator=None, type_to_format=None):
        col = Column()
        col.title = title
        col.format = fmt
        col.width = width
        col.title_to_value_separator = title_to_value_separator
        col.pad_fill_char = pad_fill_char
        col.pad_align = pad_align
        col.type_to_format = type_to_format
        col.column_separator = column_separator
        self.columns.append(col)
        return self

    def add_columns(self, *titles: str):
        for title in titles:
            self.add_column(title)

    @staticmethod
    def _print_impl(s: str):
        print(s, end="", flush=True)


class Scolp:

    def __init__(self, config: Config):
        self.config = copy.deepcopy(config)
        self.row_index = 0
        self.last_row_print_time_seconds = 0
        self.init_time = datetime.datetime.now()
        self._cur_col_index = 0
        self._cur_printed_row_index = -1
        self._enable_print_current_row = False
        self._force_print_row_index = 0

    def _print(self, s: str):
        self.config.print_func(s)

    def _println(self):
        self._print("\n")

    def _pad(self, s: str, col: Column, orig_value):
        width = self._get_config_param(col, "width")

        col.width = max(width, len(s))

        if len(s) == col.width:
            return s

        pad_fill_char = self._get_config_param(col, "pad_fill_char")

        align = self._get_config_param(col, "pad_align")
        if align == Alignment.AUTO and orig_value is not None:
            if isinstance(orig_value, numbers.Number):
                align = Alignment.RIGHT
            else:
                align = Alignment.LEFT

        if align == Alignment.RIGHT:
            padded = str.rjust(s, width, pad_fill_char)
        elif align == Alignment.CENTER:
            padded = str.center(s, width, pad_fill_char)
        else:
            padded = str.ljust(s, width, pad_fill_char)

        return padded

    def get_default_format_str(self, col: Column, value):
        type_to_format = self._get_config_param(col, "type_to_format")
        for typ, fmt in type_to_format.items():
            if isinstance(value, typ):
                return fmt
        return None

    def _format(self, col: Column, value):
        fmt = self._get_config_param(col, "format")
        if fmt is None:
            fmt = self.get_default_format_str(col, value)

        if fmt is None:
            fmt_val = str(value)
        else:
            try:
                fmt_val = str.format(fmt, value)
            except (ValueError, TypeError):
                fmt_val = str(value) + " (FMT_ERR)"

        fmt_val = self._pad(fmt_val, col, value)
        return fmt_val

    def _get_config_param(self, col: Column, param_name: str):
        col_param = col.__dict__[param_name]
        if col_param is not None:
            return col_param
        return self.config.default_column.__dict__[param_name]

    def _print_col_headers(self):
        self._println()
        for col in self.config.columns:
            title = self._pad(col.title, col, None)
            self._print(title)
            if col is not self.config.columns[-1]:
                column_separator = self._get_config_param(col, "column_separator")
                self._print(column_separator)
        self._println()

        for col in self.config.columns:
            horz_line = self.config.header_line_char * col.width
            self._print(horz_line)
            if col is not self.config.columns[-1]:
                column_separator = self._get_config_param(col, "column_separator")
                self._print(column_separator)
        self._println()

    def _print_column(self, var_value):
        col = self.config.columns[self._cur_col_index]

        if self._cur_col_index == 0:
            self._cur_printed_row_index += 1
            self.last_row_print_time_seconds = datetime.datetime.now().timestamp()

            if self.config.title_mode == TitleMode.HEADER and \
                    (self._cur_printed_row_index == self.config.header_repeat_row_count_first or
                     self._cur_printed_row_index % self.config.header_repeat_row_count == 0):
                self._print_col_headers()

        if self.config.title_mode == TitleMode.INLINE and col.title and not col.title.isspace():
            self._print(col.title)
            title_to_value_separator = self._get_config_param(col, "title_to_value_separator")
            self._print(title_to_value_separator)

        fmt_val = self._format(col, var_value)

        self._print(fmt_val)

        if self._cur_col_index == len(self.config.columns) - 1:
            self._println()
        else:
            column_separator = self._get_config_param(col, "column_separator")
            self._print(column_separator)

    def _update_print_enable_status(self):
        if self._cur_col_index != 0:
            return

        self._enable_print_current_row = \
            self.row_index == self._force_print_row_index or \
            self.row_index % self.config.output_each_n_rows == 0 and \
            datetime.datetime.now().timestamp() - self.last_row_print_time_seconds >= self.config.output_each_n_seconds

    def print(self, *var_values):
        if len(self.config.columns) == 0:
            self.config.add_column("(no title)")

        for var_value in var_values:
            self._update_print_enable_status()
            if self._enable_print_current_row:
                self._print_column(var_value)

            if self._cur_col_index == len(self.config.columns) - 1:
                self.row_index += 1
                self._cur_col_index = 0
            else:
                self._cur_col_index += 1

    def endline(self, msg=""):
        self._update_print_enable_status()
        if self._enable_print_current_row:
            self._print(msg)
            self._println()
        self.row_index += 1
        self._cur_col_index = 0

    def elapsed_since_init(self, round_seconds=True):
        elapsed = datetime.datetime.now() - self.init_time
        if round_seconds:
            rounded_seconds = round(elapsed.total_seconds())
            elapsed = datetime.timedelta(seconds=rounded_seconds)
        return elapsed

    def force_print_next_row(self):
        self._force_print_row_index = self.row_index
