# pyright: reportPrivateUsage=false
# -*- coding: utf-8 -*-

"""Test for parser classes"""

import pytest
from pyap import parser, exceptions, address, parse, parse_single_street


def test_api_parse():
    test_address = (
        "xxx 225 E. John Carpenter Freeway, " + "Suite 1500 Irving, Texas 75062 xxx"
    )
    addresses = parse(test_address, country="US")
    assert (
        str(addresses[0].full_address)
        == "225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062"
    )


def test_api_parse_canada():
    test_address = "xxx 33771 George Ferguson Way Abbotsford, BC V2S 2M5 xxx"
    addresses = parse(test_address, country="CA")
    assert (
        str(addresses[0].full_address)
        == "33771 George Ferguson Way Abbotsford, BC V2S 2M5"
    )


def test_api_parse_single_street():
    test_address = "255 SOUTH STREET"
    addresses = parse_single_street(test_address, country="US")
    assert str(addresses[0].full_street) == "255 SOUTH STREET"
    assert str(addresses[0].full_address) == "255 SOUTH STREET"


def test_address_class_init():
    addr = address.Address(
        country_id="US",
        match_end=10,
        match_start=5,
        region1="USA ",
        city="CityVille, ",
        full_street="Street 1b",
        full_address="Street 1b CityVille USA",
    )
    assert addr.region1 == "USA"

    assert addr.city == "CityVille"

    assert addr.full_street == "Street 1b"

    assert str(addr) == "Street 1b CityVille USA"


def test_no_country_selected_exception():
    with pytest.raises(TypeError):
        parser.AddressParser()  # type: ignore


def test_country_detection_missing():
    with pytest.raises(exceptions.CountryDetectionMissing):
        parser.AddressParser(country="TheMoon")  # type: ignore


def test_normalize_string():
    ap = parser.AddressParser(country="US")
    raw_string = (
        """, The  quick      \t, brown fox      jumps over the lazy dog, ‐ ‑ ‒ – — ―,"""
    )
    clean_string = ", The quick, brown fox jumps over the lazy dog, - - - - - -, "
    assert ap._normalize_string(raw_string) == clean_string


def test_combine_results():
    ap = parser.AddressParser(country="US")
    raw_dict = {"test_one": None, "test_one_a": 1, "test_two": None, "test_two_b": 2}
    assert ap._combine_results(raw_dict) == {"test_one": 1, "test_two": 2}


@pytest.mark.parametrize(
    "input,expected",
    [
        ("No address here", None),
        (
            "2590 Elm Road NE - Warren, OH 44483, US",
            {
                "street_number": "2590",
                "street_name": "Elm",
                "street_type": "Road",
                "post_direction": "NE",
                "city": "Warren",
                "region1": "OH",
                "postal_code": "44483",
                "full_address": "2590 Elm Road NE - Warren, OH 44483, US",
                "country": "US",
            },
        ),
        (
            "899 HEATHROW PARK LN 02-2135\nLAKE MARY,FL 32746",
            {
                "street_number": "899",
                "street_name": "HEATHROW PARK",
                "street_type": "LN",
                "city": "LAKE MARY",
                "region1": "FL",
                "postal_code": "32746",
                "full_address": "899 HEATHROW PARK LN 02-2135\nLAKE MARY, FL 32746",
            },
        ),
        (
            "696 BEAL PKWY NW\nFT WALTON BCH FL 32547",
            {
                "street_number": "696",
                "street_name": "BEAL",
                "street_type": "PKWY",
                "post_direction": "NW",
                "city": "FT WALTON BCH",
                "region1": "FL",
                "postal_code": "32547",
                "full_address": "696 BEAL PKWY NW\nFT WALTON BCH FL 32547",
            },
        ),
        (
            "xxx, 225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062 xxx",
            {
                "street_number": "225",
                "street_name": "E. John Carpenter",
                "street_type": "Freeway",
                "occupancy": "Suite 1500",
                "city": "Irving",
                "region1": "Texas",
                "postal_code": "75062",
                "full_address": (
                    "225 E. John Carpenter Freeway, Suite 1500 Irving, Texas 75062"
                ),
            },
        ),
        (
            "1300 E MOUNT GARFIELD ROAD, NORTON SHORES 49441",
            {
                "street_number": "1300",
                "street_name": "E MOUNT GARFIELD",
                "street_type": "ROAD",
                "city": "NORTON SHORES",
                "region1": None,
                "postal_code": "49441",
                "full_address": "1300 E MOUNT GARFIELD ROAD, NORTON SHORES 49441",
            },
        ),
        (
            "7601 Penn Avenue South, Richfield MN 55423",
            {
                "street_number": "7601",
                "street_name": "Penn",
                "street_type": "Avenue",
                "post_direction": "South",
                "city": "Richfield",
                "region1": "MN",
                "postal_code": "55423",
            },
        ),
        (
            "STAFFING LLC, 242 N AVENUE 25 SUITE 300, LOS ANGELES, CA 900031, Period ",
            {
                "street_number": "242",
                "typeless_street_name": "N AVENUE 25",
                "occupancy": "SUITE 300",
                "city": "LOS ANGELES",
                "region1": "CA",
                "postal_code": None,
            },
        ),
        (
            "2633 Camino Ramon Ste. 400 San Ramon, CA 94583-2176",
            {
                "street_number": "2633",
                "street_type": "Camino",
                "street_name": "Ramon",
                "occupancy": "Ste. 400",
                "city": "San Ramon",
                "region1": "CA",
                "postal_code": "94583-2176",
            },
        ),
        (
            "2006 Broadway Ave Suite 2A, PO Drawer J, Great Bend, KS 67530",
            {
                "street_number": "2006",
                "street_type": "Ave",
                "street_name": "Broadway",
                "occupancy": "Suite 2A",
                "city": "Great Bend",
                "region1": "KS",
                "po_box": "PO Drawer J",
                "postal_code": "67530",
            },
        ),
        (
            "One Baylor Plaza MS: BCM204\nHouston TX 77030-3411",
            {
                "street_number": "One",
                "street_type": "Plaza",
                "street_name": "Baylor",
                "mail_stop": "MS: BCM204",
                "city": "Houston",
                "region1": "TX",
                "postal_code": "77030-3411",
            },
        ),
        (
            "2817 PETERS ROAD BAY 52, Amazeville, AL 12345",
            {
                "street_number": "2817",
                "street_type": "ROAD",
                "street_name": "PETERS",
                "occupancy": "BAY 52",
                "city": "Amazeville",
                "region1": "AL",
                "postal_code": "12345",
            },
        ),
        (
            "6325F OPAL HEIGHTS BL\nSAN FRANCISCO CA 94131",
            {
                "street_number": "6325F",
                "street_type": "BL",
                "street_name": "OPAL HEIGHTS",
                "occupancy": None,
                "city": "SAN FRANCISCO",
                "region1": "CA",
                "postal_code": "94131",
            },
        ),
        (
            "2744W GRANDIOSE WAY#100\nLEHI UT 84043",
            {
                "street_number": "2744W",
                "street_type": "WAY",
                "street_name": "GRANDIOSE",
                "occupancy": "#100",
                "city": "LEHI",
                "region1": "UT",
                "postal_code": "84043",
            },
        ),
    ],
)
def test_parse_address(input: str, expected):
    ap = parser.AddressParser(country="US")
    if result := ap.parse(input):
        expected = expected or {}
        received = {key: getattr(result[0], key) for key in expected}
        assert received == expected
    else:
        assert expected is None


@pytest.mark.parametrize(
    "input,expected",
    [
        (
            "1111, 101-3RD STR SW, CALGARY, ALBERTA, T2P3E6",
            {
                "street_number": "1111",
                "street_type": "STR",
                "street_name": "101-3RD",
                "occupancy": None,
                "city": "CALGARY",
                "region1": "ALBERTA",
                "postal_code": "T2P3E6",
            },
        ),
    ],
)
def test_parse_address_canada(input: str, expected):
    ap = parser.AddressParser(country="CA")
    if result := ap.parse(input):
        expected = expected or {}
        received = {key: getattr(result[0], key) for key in expected}
        assert received == expected
    else:
        assert expected is None


def test_parse_po_box():
    ap = parser.AddressParser(country="US")

    address = ap.parse_single_street(
        "ELECTRIC WIRING SYSTEMS INC, 1111 ASHLEY STREET, P.O. BOX 99999, "
        "BOWLING GREEN, KY 444444-9999"
    )[0]
    assert address.po_box == "P.O. BOX 99999"

    address = ap.parse_single_street("P.O. BOX 99999, One Velvet Drive")[0]
    assert address.po_box == "P.O. BOX 99999"

    address = ap.parse_single_street("P.O. BOX 99999")[0]
    assert address.po_box == "P.O. BOX 99999"
