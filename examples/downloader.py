import datetime, urllib3, scolp

url = "http://speedtest.tele2.net/100MB.zip"
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
