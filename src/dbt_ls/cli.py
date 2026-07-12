import argparse
import logging

from dbt_ls import __version__
from dbt_ls.server import server
print(__version__)
def main():
    banner = f"""
   ╔═══════════════════════════════════════╗
   ║                                       ║
   ║      _ _     _        _               ║
   ║   __| | |__ | |_     | |___           ║
   ║  / _` | '_ \\| __|____| / __|          ║
   ║ | (_| | |_) | ||_____| \\__ \\          ║
   ║  \\__,_|_.__/ \\__|    |_|___/          ║
   ║                                       ║
   ║   {__version__:^5} · Language Server · stdio     ║
   ║                                       ║
   ╚═══════════════════════════════════════╝
    """
    print(banner)

    p = argparse.ArgumentParser()
    p.add_argument("--tcp", action="store_true")
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=8765)
    args = p.parse_args()
    if args.tcp:
        server.start_tcp(args.host, args.port)
    else:
        server.start_io()
    logging.info("DBT Language Server started")


if __name__ == "__main__":
    main()
