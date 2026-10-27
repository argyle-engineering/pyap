# pyright: reportPrivateUsage=false
# -*- coding: utf-8 -*-

"""
Tests for Australian address parser.

Positive address examples informed by Geoscape G-NAF (data.gov.au, CC BY 4.0)
and the ACNC Register of Australian Charities (data.gov.au, CC BY 3.0 AU).
"""

import re
import pytest
import itertools
from pyap import parser, utils, parse
import pyap.source_AU.data as data_au


def execute_matching_test(input, expected, pattern):
    match = utils.match(pattern, input, re.VERBOSE)
    is_found = match is not None
    if expected:
        assert is_found == expected
        assert match.group(0) == input  # type: ignore
    else:
        assert (is_found == expected) or (match.group(0) != input)  # type: ignore


unit_slash_pattern = r"(?P<slash>{})".format(data_au.unit_slash)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("12", True),
        ("12A", True),
        ("12-14", True),
        ("12345", True),
        ("123456", False),
    ],
)
def test_street_number(input, expected):
    execute_matching_test(input, expected, data_au.street_number)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("2/", True),
        ("12A/", True),
        ("2/ ", True),
    ],
)
def test_unit_slash(input, expected):
    execute_matching_test(input, expected, unit_slash_pattern)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("St", True),
        ("Street", True),
        ("Tce", True),
        ("Terrace", True),
        ("Hwy", True),
        ("Highway", True),
        ("Pde", True),
        ("Cct", True),
        ("Rd", True),
        ("Xyz", False),
    ],
)
def test_street_type(input, expected):
    execute_matching_test(input, expected, data_au.street_type)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("Unit 5", True),
        ("U 804", True),
        ("Shop 3", True),
        ("Suite 11", True),
        ("Lot 12", True),
        ("Apt 2B", True),
    ],
)
def test_occupancy(input, expected):
    execute_matching_test(input, expected, data_au.occupancy)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("Level 15", True),
        ("L 5", True),
        ("L5", True),
        ("Floor 3", True),
    ],
)
def test_floor(input, expected):
    execute_matching_test(input, expected, data_au.floor)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("Po Box 3122", True),
        ("P.O. Box 201", True),
        ("GPO Box 1234", True),
        ("Locked Bag 42", True),
        ("Private Bag 100", True),
        ("RMB 1234", True),
        ("RSD 5678", True),
    ],
)
def test_po_box(input, expected):
    execute_matching_test(input, expected, data_au.po_box)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("N", True),
        ("NE", True),
        ("Upper", True),
        ("Lower", True),
    ],
)
def test_post_direction(input, expected):
    execute_matching_test(input, expected, data_au.post_direction)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("NSW", True),
        ("Vic", True),
        ("QLD", True),
        ("Qld", True),
        ("WA", True),
        ("ACT", True),
        ("New South Wales", True),
        ("Western Australia", True),
        ("wa", False),
        ("sa", False),
        ("nt", False),
    ],
)
def test_region1(input, expected):
    execute_matching_test(input, expected, data_au.region1)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("2042", True),
        ("204", False),
        ("20422", False),
        ("12042", False),
    ],
)
def test_postal_code(input, expected):
    match = utils.match(data_au.postal_code, input, re.VERBOSE)
    if expected:
        assert match is not None
        assert match.group("postal_code") == input.strip()  # type: ignore
    else:
        assert match is None or match.group("postal_code") != input.strip()  # type: ignore


@pytest.mark.parametrize(
    "input,expected",
    [
        ("Australia", True),
        ("AUS", True),
        ("AU", True),
        ("Austria", False),
    ],
)
def test_country(input, expected):
    execute_matching_test(input, expected, data_au.country)


@pytest.mark.parametrize(
    "input,expected",
    [
        ("2/45 Smith St, Newtown NSW 2042", True),
        ("433 Princes Hwy, Officer VIC 3809", True),
        ("Po Box 3122, West Tamworth NSW 2340", True),
        ("P.O. Box 201, Bendigo VIC 3552", True),
        ("Level 15, 216 St Georges Tce, Perth WA 6000", True),
        ("1/28 Breynia Street, Figtree NSW 2525", True),
        ("12-14 Mcnicol St, Geelong West VIC 3218", True),
        ("1a Park Bvd, Ferntree Gully VIC 3156", True),
        ("500 Pacific Hwy, Belmont NSW 2280", True),
        ("101 Tram Road, Doncaster VIC 3108", True),
        ("292 Canterbury Rd, Surrey Hills VIC 3127", True),
        ("20 Milan Tce, Stirling SA 5152", True),
        ("55 Clyde St, Mollymook Beach NSW 2539", True),
        ("49 Kildare Rd, Blacktown NSW 2148", True),
        ("3126 Geelong-bacchus Marsh Rd, Balliang East VIC 3340", True),
        ("478 George St, Sydney NSW 2000", True),
        ("213-217 North Road, Albany WA 6330", True),
        ("614 Burbridge Rd, West Beach SA 5024", True),
        ("2 Bingar Street, Yenda NSW 2681", True),
        ("14 Xuereb St, Tallawong NSW 2762", True),
        ("216 St Georges Tce Perth WA 6000", True),
        ("45 Smith St, Newtown NSW", True),
        ("1 Main St, Brisbane QLD 4000, Australia", True),
        ("(02) 9555 1234", False),
        ("0412 345 678", False),
        ("12 345 678 901", False),
        ("45 Smith St, Newtown", False),
        ("He moved to NSW in 2020", False),
        ("wa s good day", False),
    ],
)
def test_full_address(input, expected):
    execute_matching_test(input, expected, data_au.full_address)


def test_full_address_parts():
    example_addresses = [
        {
            "full_address": "2/45 Smith St, Newtown NSW 2042",
            "occupancy": "2",
            "street_number": "45",
            "street_name": "Smith",
            "street_type": "St",
            "city": "Newtown",
            "region1": "NSW",
            "postal_code": "2042",
        },
        {
            "full_address": "Level 15, 216 St Georges Tce, Perth WA 6000",
            "floor": "Level 15",
            "street_number": "216",
            "street_name": "St Georges",
            "street_type": "Tce",
            "city": "Perth",
            "region1": "WA",
            "postal_code": "6000",
        },
        {
            "full_address": "Po Box 3122, West Tamworth NSW 2340",
            "po_box": "Po Box 3122",
            "city": "West Tamworth",
            "region1": "NSW",
            "postal_code": "2340",
        },
    ]
    filler_text = (
        "This is filler text that can be inserted both before and after addresses"
    )
    punctuation = ["\n", ", ", ". ", " "]

    for address_parts in example_addresses:
        for filler_before, filler_after in itertools.product(
            [False, True], [False, True]
        ):
            for join_string in punctuation:
                filler_text_before = (
                    (filler_text + join_string) if filler_before else ""
                )
                filler_text_after = (join_string + filler_text) if filler_after else ""
                address_text = (
                    filler_text_before
                    + address_parts["full_address"]
                    + filler_text_after
                )

                parsed = parse(address_text, country="AU")
                assert len(parsed) == 1
                for k, v in address_parts.items():
                    if k == "full_address":
                        assert parsed[
                            0
                        ].full_address == parser.AddressParser._normalize_string(v)
                    else:
                        assert parsed[0].__getattribute__(k) == v
