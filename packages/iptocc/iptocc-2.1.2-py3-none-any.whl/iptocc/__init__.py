#!/usr/bin/env python
# __author__ = "Ronie Martinez"
# __copyright__ = "Copyright 2017-2020, Ronie Martinez"
# __credits__ = ["Ronie Martinez"]
# __maintainer__ = "Ronie Martinez"
# __email__ = "ronmarti18@gmail.com"
import logging
import os
import sys
import threading
from functools import lru_cache
from ipaddress import IPv4Address, IPv6Address, IPv6Network, ip_address
from typing import Union, Tuple

import pandas

from iptocc.exceptions import CountryCodeNotFound, CountryNotFound

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format="%(asctime)s\t%(levelname)s\t%(module)s\t%(message)s",
)
logger = logging.getLogger("iptocc")

pandas.set_option("display.max_columns", None)
pandas.set_option("display.expand_frame_repr", False)
pandas.set_option("max_colwidth", -1)

lock = threading.Lock()
_rir_database: pandas.DataFrame = None
_countries: dict = dict()


def convert_to_ip_object(
    row: dict,
) -> Union[Tuple[IPv4Address, IPv4Address], Tuple[IPv6Network, str], Tuple[str, str]]:
    if row["Type"] == "ipv4":
        start = IPv4Address(row["Start"])
        return start, start + int(row["Value"])
    elif row["Type"] == "ipv6":
        return IPv6Network(row["Start"] + "/" + row["Value"]), ""
    return row["Start"], ""


def load_rir_databases() -> None:
    get_rir_database()


def get_rir_database() -> pandas.DataFrame:
    global lock
    global _rir_database
    global _countries
    if _rir_database is None:
        with lock:
            if _rir_database is None:
                logger.info("Loading RIR databases")
                _rir_database = pandas.concat(read_rir_databases())
                _rir_database = _rir_database[
                    (
                        (_rir_database["Type"] == "ipv4")
                        | (_rir_database["Type"] == "ipv6")
                    )
                    & (_rir_database["Type"] != "*")
                ]
                _rir_database[["Start", "End"]] = _rir_database.apply(
                    convert_to_ip_object, axis=1, result_type="expand"
                )
                countries = pandas.read_csv(
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "iso3166.csv"
                    ),
                    names=["country_code", "country_name"],
                )
                _countries = dict(
                    zip(
                        countries["country_code"].values,
                        countries["country_name"].values,
                    )
                )
                logger.info("RIR databases loaded")
    return _rir_database


def read_rir_databases():
    headers = [
        "Registry",
        "Country Code",
        "Type",
        "Start",
        "Value",
        "Date",
        "Status",
        "Extensions",
    ]
    iptocc_dir = os.path.dirname(os.path.abspath(__file__))
    for rir_database in os.listdir(iptocc_dir):
        if rir_database.startswith("delegated-") and rir_database.endswith(
            "-extended-latest"
        ):
            rir_database_path = os.path.join(iptocc_dir, rir_database)
            yield pandas.read_csv(
                rir_database_path,
                delimiter="|",
                comment="#",
                names=headers,
                dtype=str,
                keep_default_na=False,
                na_values=[""],
                encoding="utf-8",
            )[4:]


@lru_cache(maxsize=100000)
def ipv4_get_country_code(address: IPv4Address) -> str:
    rir_database = get_rir_database()
    ipv4_database = rir_database[rir_database["Type"] == "ipv4"]
    result = ipv4_database[
        (ipv4_database["Start"] <= address) & (ipv4_database["End"] > address)
    ]
    try:
        return result["Country Code"].tolist()[0]
    except IndexError:
        raise CountryCodeNotFound


@lru_cache(maxsize=100000)
def ipv6_get_country_code(address: IPv6Address) -> str:
    rir_database = get_rir_database()  # pandas.DataFrame
    ipv6_database = rir_database[rir_database["Type"] == "ipv6"]
    result = ipv6_database[
        ipv6_database.apply(
            lambda row: address in row["Start"], axis=1, result_type="expand"
        )
    ]
    try:
        return result["Country Code"].tolist()[0]
    except IndexError:
        raise CountryCodeNotFound


def get_country_code(address: str) -> str:
    address = ip_address(address)
    if isinstance(address, IPv4Address):
        logger.info("%s is IPv4", address)
        return ipv4_get_country_code(address)
    logger.info("%s is IPv6", address)
    return ipv6_get_country_code(address)


def get_country(address: str) -> str:
    global _countries
    try:
        country_code = get_country_code(address)
    except CountryCodeNotFound:
        raise CountryNotFound
    return _countries[country_code]
