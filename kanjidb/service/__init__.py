__all__ = ["setup_logging", "run", "main"]
import os
import sys
import argparse
import json
from aiohttp import web
import logging
from kanjidb.service.app import Application
from kanjidb.service import configuration


def setup_logging(
    *,
    access_logfile=None,
    access_maxbytes=None,
    access_backupcount=None,
    error_logfile=None,
    error_maxbytes=None,
    error_backupcount=None
):
    """Setup logging handlers.

    This setup two `RotatingFileHandler` for `aiohttp.access` and `aiohttp.server` logs.

    :param access_logfile: path for access logfile or `None`
    :param access_maxbytes: max bytes per access logfile
    :param access_backupcount: max number of access logfile to keep
    :param error_logfile: path for error logfile or `None`
    :param error_maxbytes: max bytes per error logfile
    :param error_backupcount: max number of error logfile to keep
    """
    from logging.handlers import RotatingFileHandler

    if access_logfile:
        logging.getLogger("aiohttp.access").addHandler(
            RotatingFileHandler(
                access_logfile,
                maxBytes=access_maxbytes,
                backupCount=access_backupcount,
            )
        )
    if error_logfile:
        logging.getLogger("aiohttp.server").addHandler(
            RotatingFileHandler(
                error_logfile, maxBytes=error_maxbytes, backupCount=error_backupcount,
            )
        )


def run(*, swagger_yml: str, swagger_url: str, base_url: str, port: int, db):
    app = Application(
        swagger_yml=swagger_yml, swagger_url=swagger_url, base_url=base_url, db=db
    )
    web.run_app(app, port=port)


def main(argv):
    parser = argparse.ArgumentParser(prog="Service", description="Help")
    parser.add_argument("directory", type=str, help="config directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity level")
    args = parser.parse_args(args=argv)

    config_dir = args.directory
    if not os.path.isdir(config_dir):
        raise NotADirectoryError(config_dir)

    config = configuration.load(os.path.join(config_dir, "config.cnf"))

    logging.basicConfig(level=logging.INFO)

    setup_logging(
        access_logfile=config["logging"].get("access-logfile", None),
        access_maxbytes=int(config["logging"].get("access-maxbytes", None)),
        access_backupcount=int(config["logging"].get("access-backupcount", None)),
        error_logfile=config["logging"].get("error-logfile", None),
        error_maxbytes=int(config["logging"].get("error-maxbytes", None)),
        error_backupcount=int(config["logging"].get("error-backupcount", None)),
    )

    with open(config["service"]["db-file"], "rb") as f:
        content = f.read()
        db = json.loads(content.decode(), encoding="utf8")

    run(
        swagger_yml=config["service"]["swagger-yml"],
        swagger_url=config["service"]["swagger-url"],
        base_url=config["service"]["base-url"],
        port=int(config["service"]["port"]),
        db=db,
    )


if __name__ == "__main__":
    main(sys.argv)
