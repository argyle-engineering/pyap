# -*- coding: utf-8 -*-

"""
    pyap.source_AU.data
    ~~~~~~~~~~~~~~~~~~~

    Regular expression definitions for detecting Australian addresses.

    Street type vocabulary derived from Geoscape G-NAF (STREET_TYPE_AUT),
    data.gov.au, CC BY 4.0.

    :copyright: (c) 2015 by Vladimir Goncharov.
    :license: MIT, see LICENSE for more details.
"""

from pyap.utils import str_list_to_upper_lower_regex, street_type_list_to_regex

part_divider = r"(?:[\,\ \.\-]{0,3}[\,\n][\,\ \.\-]{0,3})"
space_pattern = r"(?:[\ \t]{1,3})"

# Geoscape G-NAF STREET_TYPE_AUT (names and abbreviations); directions omitted.
street_type_list = [
    "ACCESS",
    "ACCS",
    "ACRE",
    "AIRWALK",
    "ALLEY",
    "ALLEYWAY",
    "ALLY",
    "ALWY",
    "AMBL",
    "AMBLE",
    "ANNEX",
    "APP",
    "APPROACH",
    "ARC",
    "ARCADE",
    "ARTERIAL",
    "ARTERY",
    "ARTL",
    "ARTY",
    "AV",
    "AVENUE",
    "AWLK",
    "BA",
    "BANAN",
    "BANK",
    "BAY",
    "BCH",
    "BDGE",
    "BDWY",
    "BDY",
    "BEACH",
    "BEND",
    "BIDI",
    "BOARDWALK",
    "BOULEVARD",
    "BOULEVARDE",
    "BOUNDARY",
    "BOWL",
    "BR",
    "BRACE",
    "BRAE",
    "BRAN",
    "BRANCH",
    "BRDWLK",
    "BREAK",
    "BRET",
    "BRETT",
    "BRIDGE",
    "BRK",
    "BROADWALK",
    "BROADWAY",
    "BROW",
    "BSWY",
    "BULL",
    "BUSWAY",
    "BVD",
    "BVDE",
    "BWLK",
    "BYPA",
    "BYPASS",
    "BYWAY",
    "BYWY",
    "CAUSEWAY",
    "CCT",
    "CENTRE",
    "CENTREWAY",
    "CH",
    "CHASE",
    "CIR",
    "CIRCLE",
    "CIRCLET",
    "CIRCUIT",
    "CIRCUS",
    "CL",
    "CLDE",
    "CLOSE",
    "CLR",
    "CLT",
    "CLUSTER",
    "CMMN",
    "CMMNS",
    "CNCD",
    "CNR",
    "CNTN",
    "CNWY",
    "COLONNADE",
    "COMMON",
    "COMMONS",
    "CON",
    "CONCORD",
    "CONCOURSE",
    "CONNECTION",
    "CONNECTOR",
    "CONR",
    "COPSE",
    "CORNER",
    "CORSO",
    "COURSE",
    "COURT",
    "COURTYARD",
    "COVE",
    "CPS",
    "CR",
    "CRCS",
    "CRESCENT",
    "CREST",
    "CRF",
    "CRIEF",
    "CRK",
    "CROOK",
    "CROSS",
    "CROSSING",
    "CROSSOVER",
    "CRSE",
    "CRSG",
    "CRSS",
    "CRST",
    "CRUISEWAY",
    "CRVR",
    "CSAC",
    "CSO",
    "CSWY",
    "CT",
    "CTR",
    "CTYD",
    "CUL-DE-SAC",
    "CUT",
    "CUTT",
    "CUTTING",
    "CUWY",
    "DALE",
    "DASH",
    "DE",
    "DELL",
    "DENE",
    "DEVIATION",
    "DIP",
    "DISTRIBUTOR",
    "DIV",
    "DIVIDE",
    "DOCK",
    "DOM",
    "DOMAIN",
    "DOWN",
    "DOWNS",
    "DR",
    "DRIVE",
    "DRIVEWAY",
    "DSTR",
    "DVWY",
    "DWNS",
    "EASEMENT",
    "EDGE",
    "ELB",
    "ELBOW",
    "END",
    "ENT",
    "ENTRANCE",
    "ESMT",
    "ESP",
    "ESPLANADE",
    "EST",
    "ESTATE",
    "EXP",
    "EXPRESSWAY",
    "EXTENSION",
    "EXTN",
    "FAIRWAY",
    "FAWY",
    "FBRK",
    "FIREBREAK",
    "FIRELINE",
    "FIRETRACK",
    "FIRETRAIL",
    "FITR",
    "FLAT",
    "FLATS",
    "FLNE",
    "FLTS",
    "FOLLOW",
    "FOLW",
    "FOOTWAY",
    "FORD",
    "FORESHORE",
    "FORK",
    "FORM",
    "FORMATION",
    "FREEWAY",
    "FRNT",
    "FRONT",
    "FRONTAGE",
    "FRTG",
    "FSHR",
    "FTRK",
    "FTWY",
    "FWY",
    "GAP",
    "GARDEN",
    "GARDENS",
    "GATE",
    "GATEWAY",
    "GDN",
    "GDNS",
    "GLADE",
    "GLDE",
    "GLEN",
    "GLY",
    "GR",
    "GRA",
    "GRANGE",
    "GREEN",
    "GRN",
    "GROVE",
    "GTE",
    "GULLY",
    "GWY",
    "HARBOUR",
    "HAVEN",
    "HEATH",
    "HEIGHTS",
    "HIGHROAD",
    "HIGHWAY",
    "HIKE",
    "HILL",
    "HILLS",
    "HIRD",
    "HLLW",
    "HOLLOW",
    "HRBR",
    "HTH",
    "HTS",
    "HUB",
    "HVN",
    "HWY",
    "ID",
    "INLET",
    "INLT",
    "INTERCHANGE",
    "INTG",
    "ISLAND",
    "JNC",
    "JUNCTION",
    "KEY",
    "KEYS",
    "KNOL",
    "KNOLL",
    "LADDER",
    "LADR",
    "LANDING",
    "LANE",
    "LANEWAY",
    "LDG",
    "LEAD",
    "LEADER",
    "LEDR",
    "LINE",
    "LINK",
    "LINKWAY",
    "LKT",
    "LNKWAY",
    "LNWY",
    "LOOKOUT",
    "LOOP",
    "LYNN",
    "LYNNE",
    "MALL",
    "MANOR",
    "MANR",
    "MART",
    "MAZE",
    "MEAD",
    "MEANDER",
    "MEW",
    "MEWS",
    "MILE",
    "MNDR",
    "MOTORWAY",
    "MTWY",
    "MZ",
    "NEST",
    "NOOK",
    "NORTH",
    "NTH",
    "OTLK",
    "OTLT",
    "OUTLET",
    "OUTLOOK",
    "OVAL",
    "PALMS",
    "PARADE",
    "PARADISE",
    "PARK",
    "PARKWAY",
    "PASS",
    "PASSAGE",
    "PATH",
    "PATHWAY",
    "PDE",
    "PENINSULA",
    "PERCH",
    "PIAZ",
    "PIAZZA",
    "PKT",
    "PL",
    "PLACE",
    "PLAZA",
    "PLMS",
    "PLZA",
    "PNT",
    "POCKET",
    "POINT",
    "PORT",
    "PRCH",
    "PRDS",
    "PREC",
    "PRECINCT",
    "PROM",
    "PROMENADE",
    "PRST",
    "PSGE",
    "PSLA",
    "PURSUIT",
    "PWAY",
    "PWY",
    "QDRT",
    "QUAD",
    "QUADRANT",
    "QUAY",
    "QUAYS",
    "QY",
    "QYS",
    "RAMBLE",
    "RAMP",
    "RANGE",
    "RCH",
    "RD",
    "RDGE",
    "RDS",
    "RDWY",
    "REACH",
    "REEF",
    "RES",
    "RESERVE",
    "REST",
    "RETREAT",
    "RETURN",
    "RIDE",
    "RIDGE",
    "RIGHT OF WAY",
    "RING",
    "RISE",
    "RISING",
    "RIVER",
    "RMBL",
    "RND",
    "RNGE",
    "ROAD",
    "ROADS",
    "ROADWAY",
    "ROFW",
    "ROTARY",
    "ROUND",
    "ROUTE",
    "ROW",
    "ROWE",
    "RSNG",
    "RTE",
    "RTN",
    "RTT",
    "RTY",
    "RUE",
    "RUN",
    "RVR",
    "SBWY",
    "SDNG",
    "SERVICEWAY",
    "SHUN",
    "SHUNT",
    "SIDING",
    "SKLN",
    "SKYLINE",
    "SLOPE",
    "SLPE",
    "SOUTH",
    "SPUR",
    "SQ",
    "SQUARE",
    "ST",
    "STAI",
    "STEPS",
    "STH",
    "STPS",
    "STRA",
    "STRAIGHT",
    "STRAIT",
    "STRAND",
    "STREET",
    "STRIP",
    "STRP",
    "STRT",
    "SUBWAY",
    "SVWY",
    "TARN",
    "TCE",
    "TERRACE",
    "THFR",
    "THOROUGHFARE",
    "THROUGHWAY",
    "THRU",
    "TKWY",
    "TLWY",
    "TMWY",
    "TOLLWAY",
    "TOP",
    "TOR",
    "TRACK",
    "TRAIL",
    "TRAMWAY",
    "TRAVERSE",
    "TRIANGLE",
    "TRK",
    "TRL",
    "TRUNKWAY",
    "TUNL",
    "TUNNEL",
    "TURN",
    "TVSE",
    "TWIST",
    "UNDERPASS",
    "UPAS",
    "VALE",
    "VALLEY",
    "VERGE",
    "VIAD",
    "VIADUCT",
    "VIEW",
    "VIEWS",
    "VILLA",
    "VILLAGE",
    "VILLAS",
    "VISTA",
    "VLGE",
    "VLLA",
    "VLLS",
    "VLLY",
    "VSTA",
    "VUE",
    "VWS",
    "WADE",
    "WALK",
    "WALKWAY",
    "WATERS",
    "WATERWAY",
    "WAY",
    "WD",
    "WDS",
    "WHARF",
    "WHRF",
    "WKWY",
    "WOOD",
    "WOODS",
    "WTRS",
    "WTWY",
    "WYND",
    "YARD",
    "YARDS",

]

street_type_re = street_type_list_to_regex(street_type_list)

street_number = r"""
                    (?P<street_number>
                        (?:(?<![\.0-9])
                            \d{1,5}[A-Za-z]?
                            (?:\-\d{1,5}[A-Za-z]?)?
                        (?![\d]))
                    )
"""

street_name = r"""
                    (?P<street_name>
                        (?(street_number)
                            [a-zA-Z0-9][a-zA-Z0-9 \.\-\']{0,40}?
                            |
                            [a-zA-Z][a-zA-Z \.\-\']{0,40}?
                        )
                    )
"""

street_type = r"""
                    (?P<street_type>
                        {street_type_re}
                    )
""".format(
    street_type_re=street_type_re,
)

post_direction = r"""
                    (?P<post_direction>
                        (?:
                            N(?:orth)?\b|E(?:ast)?\b|S(?:outh)?\b|W(?:est)?\b|
                            NE\b|NW\b|SE\b|SW\b|
                            [Uu]pper\b|[Ll]ower\b|[Ee]xtension\b|[Ii]nner\b|[Oo]uter\b
                        )
                    )
"""

unit_slash = r"""
                    (?P<occupancy_b>
                        [A-Za-z]?\d{1,5}[A-Za-z]?
                    )
                    \ ?/\ ?
"""

flat_type_words = [
    "Unit",
    "U",
    "Shop",
    "Suite",
    "Se",
    "Ste",
    "Apartment",
    "Apt",
    "Flat",
    "Villa",
    "Townhouse",
    "Lot",
    "Site",
    "Office",
    "Room",
    "Factory",
    "Studio",
    "Stu",
    "Warehouse",
    "Whse",
    "Townhouse",
    "Tnhs",
    "Duplex",
    "Dupl",
    "Kiosk",
    "Ksk",
    "Cottage",
    "Ctge",
    "Garage",
    "Grge",
    "Shed",
    "Section",
    "Sec",
]

flat_type_tokens = sorted(
    {word for word in flat_type_words if word != "U"},
    key=len,
    reverse=True,
)
flat_types_re = str_list_to_upper_lower_regex(flat_type_tokens) + r"|\bU\b"

occupancy = r"""
                    (?P<occupancy_a>
                        (?:
                            {flat_types}
                        )
                        {space}?
                        [A-Za-z\#\-\&\d]{{1,7}}
                        {space}?
                    )
""".format(
    flat_types=flat_types_re,
    space=space_pattern,
)

floor = r"""
                    (?P<floor>
                        (?:
                            (?:[Ll]|[Ll]evel|[Ll]vl|[Ff]|[Ff]loor|[Gg]|[Gg]round|
                               [Bb]|[Bb]asement|[Ll][Gg]|[Uu][Gg]|[Mm]|[Mm]ezzanine)
                            {space}?
                            \d+[A-Za-z]{{0,2}}
                        )
                        {space}?
                    )
""".format(
    space=space_pattern,
)

building = r"""
                    (?P<building_id>
                        (?:
                            [Bb][Uu][Ii][Ll][Dd][Ii][Nn][Gg]|[Bb][Ll][Dd][Gg]
                        )
                        {space}
                        \d{{0,4}}[A-Za-z]?
                        {space}?
                    )
""".format(
    space=space_pattern,
)

po_box = r"""
                    (?P<po_box>
                        (?:
                            (?:[Gg]\.?[Pp]\.?[Oo]\.?|[Pp]\.?[Oo]\.?)\ ?[Bb][Oo][Xx]
                            |[Ll]ocked\ [Bb]ag
                            |[Pp]rivate\ [Bb]ag
                            |RMB|RSD|CMB
                        )
                        {space}?
                        \d+
                    )
""".format(
    space=space_pattern,
)

street_body = r"""
            (?P<line2>
                (?:
                    {floor} {part_divider}?
                )?
                (?:
                    {occupancy} {part_divider}?
                )?
                (?:
                    {building} {part_divider}?
                )?
            )
            (?P<line1>
                (?:
                    {unit_slash}
                )?
                (?:
                    {street_number}{space}
                )?
                {street_name}{space}?
                (?:{street_type}{space}?)?
                (?:{post_direction})?
            )
""".format(
    street_number=street_number,
    street_name=street_name,
    street_type=street_type,
    post_direction=post_direction,
    unit_slash=unit_slash,
    floor=floor,
    building=building,
    occupancy=occupancy,
    part_divider=part_divider,
    space=space_pattern,
)

full_street = r"""
    (?P<full_street>
        (?:
            {po_box}
            |
            {street_body}
        )
    )
""".format(
    po_box=po_box,
    street_body=street_body,
)

region1 = r"""
        (?P<region1>
            (?:
                NSW\b|[Nn][Ss][Ww]\b|
                VIC\b|[Vv][Ii][Cc]\b|
                QLD\b|[Qq][Ll][Dd]\b|
                TAS\b|[Tt][Aa][Ss]\b|
                SA\b|WA\b|NT\b|ACT\b|
                [Nn][Ee][Ww]\ [Ss][Oo][Uu][Tt][Hh]\ [Ww][Aa][Ll][Ee][Ss]|
                [Vv][Ii][Cc][Tt][Oo][Rr][Ii][Aa]|
                [Qq][Uu][Ee][Ee][Nn][Ss][Ll][Aa][Nn][Dd]|
                [Ss][Oo][Uu][Tt][Hh]\ [Aa][Uu][Ss][Tt][Rr][Aa][Ll][Ii][Aa]|
                [Ww][Ee][Ss][Tt][Ee][Rr][Nn]\ [Aa][Uu][Ss][Tt][Rr][Aa][Ll][Ii][Aa]|
                [Tt][Aa][Ss][Mm][Aa][Nn][Ii][Aa]|
                [Nn][Oo][Rr][Tt][Hh][Ee][Rr][Nn]\ [Tt][Ee][Rr][Rr][Ii][Tt][Oo][Rr][Yy]|
                [Aa][Uu][Ss][Tt][Rr][Aa][Ll][Ii][Aa][Nn]\ [Cc][Aa][Pp][Ii][Tt][Aa][Ll]\ [Tt][Ee][Rr][Rr][Ii][Tt][Oo][Rr][Yy]
            )
        )
"""

city = r"""
        (?P<city>
            [A-Za-z0-9][A-Za-z0-9 \.\-\']*(?:\ [A-Za-z0-9][A-Za-z0-9 \.\-\']*)*
        )
"""

postal_code = r"""
        (?P<postal_code>
            (?:(?<![\d])\d{4}(?![\d]))
        )
"""

country = r"""
        (?P<country>
            [Aa][Uu][Ss][Tt][Rr][Aa][Ll][Ii][Aa]|
            [Aa][Uu][Ss]\b|
            [Aa][Uu][Ss][Tt][Rr][Aa][Ll][Ii][Aa][Nn]|
            (?<![A-Za-z])[Aa][Uu](?![A-Za-z])
        )
"""

address_tail_divider = r"(?:{part_divider}|{space})".format(
    part_divider=part_divider,
    space=space_pattern,
)

full_address = r"""
    (?<![A-Za-z0-9])
    (?P<full_address>
        {full_street}
        {address_tail_divider}
        {city}
        {address_tail_divider}?
        {region1}
        (?:{space}?{postal_code})?
        (?:{part_divider}{country})?
    )
""".format(
    full_street=full_street,
    address_tail_divider=address_tail_divider,
    part_divider=part_divider,
    city=city,
    region1=region1,
    postal_code=postal_code,
    country=country,
    space=space_pattern,
)
