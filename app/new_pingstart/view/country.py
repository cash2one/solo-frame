# coding=utf-8


class Country(object):
    info = {
        "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BA": "Bosnia and Herzegovina",
        "BB": "Barbados", "WF": "Wallis and Futuna", "BL": "St-Barth\u00e9lemy", "BM": "Bermuda",
        "BN": "Brunei Darussalam",
        "BO": "Bolivia", "BH": "Bahrain", "BI": "Burundi", "BJ": "Benin", "BT": "Bhutan", "JM": "Jamaica",
        "BV": "Bouvet Island", "BW": "Botswana", "WS": "Samoa", "BR": "Brazil", "BS": "Bahamas", "JE": "Jersey",
        "BY": "Belarus", "BZ": "Belize", "RU": "Russian Federation", "RW": "Rwanda", "RS": "Serbia",
        "TL": "Timor-Leste",
        "RE": "Reunion", "TM": "Turkmenistan", "TJ": "Tajikistan", "RO": "Romania", "TK": "Tokelau",
        "GW": "Guinea-Bissau",
        "GU": "Guam", "GT": "Guatemala", "GS": "South Georgia and the South Sandwich Islands", "GR": "Greece",
        "GQ": "Equatorial Guinea", "GP": "Guadeloupe", "JP": "Japan", "GY": "Guyana", "GG": "Guernsey",
        "GF": "French Guiana",
        "GE": "Georgia", "GD": "Grenada", "GB": "United Kingdom", "GA": "Gabon", "GN": "Guinea", "GM": "Gambia",
        "GL": "Greenland", "GI": "Gibraltar", "GH": "Ghana", "OM": "Oman", "TN": "Tunisia", "JO": "Jordan",
        "HR": "Croatia",
        "HT": "Haiti", "HU": "Hungary", "HK": "Hong Kong", "HN": "Honduras", "HM": "Heard Island and Mcdonald Islands",
        "VE": "Venezuela", "PR": "Puerto Rico", "PS": "Palestine", "PW": "Palau", "PT": "Portugal",
        "KN": "Saint Kitts and Nevis", "AF": "Afghanistan", "IQ": "Iraq", "PA": "Panama", "PF": "French Polynesia",
        "PG": "Papua New Guinea", "PE": "Peru", "PK": "Pakistan", "PH": "Philippines", "PN": "Pitcairn", "PL": "Poland",
        "PM": "Saint Pierre and Miquelon", "ZM": "Zambia", "EN": "Commonwealth of Independent States",
        "EH": "Western Sahara",
        "EE": "Estonia", "VL": "UpperVolfa", "EG": "Egypt", "ZA": "South Africa", "EC": "Ecuador", "IT": "Italy",
        "VN": "Vietnam", "SB": "Solomon Islands", "ET": "Ethiopia", "SO": "Somalia", "ZW": "Zimbabwe",
        "SA": "Saudi Arabia",
        "ES": "Spain", "ER": "Eritrea", "ME": "The Montenegro", "MD": "Moldova", "MG": "Madagascar", "MA": "Morocco",
        "MC": "Monaco", "UZ": "Uzbekistan", "MM": "Myanmar", "ML": "Mali", "MO": "Macao", "MN": "Mongolia",
        "MH": "Marshall Islands", "MK": "Macedonia", "UR": "Soviet Union", "MU": "Mauritius", "MT": "Malta",
        "MW": "Malawi",
        "MV": "Maldives", "MQ": "Martinique", "MP": "Northern Mariana Islands", "MS": "Montserrat", "MR": "Mauritania",
        "IM": "Isle of Man", "UG": "Uganda", "MY": "Malaysia", "MX": "Mexico", "IL": "Israel", "FR": "France",
        "AW": "Aruba",
        "SH": "Saint Helena", "FI": "Finland", "FJ": "Fiji", "FK": "Falkland Islands (Malvinas)", "FM": "Micronesia",
        "FO": "Faroe Islands", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway", "NA": "Namibia", "VU": "Vanuatu",
        "NC": "New Caledonia", "NE": "Niger", "NF": "Norfolk Island", "NG": "Nigeria", "NZ": "New Zealand",
        "NP": "Nepal",
        "NR": "Nauru", "NU": "Niue", "CK": "Cook Islands", "XK": "Kosova", "CI": "Cote D'Ivoire", "CH": "Switzerland",
        "CO": "Colombia", "CN": "China", "CM": "Cameroon", "CL": "Chile", "CC": "Cocos (Keeling) Islands",
        "CA": "Canada",
        "CG": "Congo", "CF": "Central African Republic", "CD": "Congo", "CZ": "Czech Republic", "CY": "Cyprus",
        "CX": "Christmas Island", "CR": "Costa Rica", "PY": "Paraguay", "CW": "Cura\u00e7ao", "CV": "Cape Verde",
        "CU": "Cuba",
        "SZ": "Swaziland", "SY": "Syrian Arab Republic", "SX": "Sint Maarten", "KG": "Kyrgyzstan", "KE": "Kenya",
        "SS": "South Sudan", "SR": "Suriname", "KI": "Kiribati", "KH": "Cambodia", "SV": "El Salvador", "KM": "Comoros",
        "ST": "Sao Tome and Principe", "SK": "Slovakia", "KR": "Korea", "SI": "Slovenia", "KP": "Korea", "KW": "Kuwait",
        "SN": "Senegal", "SM": "San Marino", "SL": "Sierra Leone", "SC": "Seychelles", "KZ": "Kazakhstan",
        "KY": "Cayman Islands", "SG": "Singapore", "SE": "Sweden", "SD": "Sudan", "DO": "Dominican Republic",
        "WI": "The Federation of the West Indies", "DM": "Dominica", "DJ": "Djibouti", "DK": "Denmark", "DH": "Dahomey",
        "DE": "Germany", "YE": "Yemen", "YG": "Yugoslavia", "DZ": "Algeria", "US": "United States", "UY": "Uruguay",
        "YT": "Mayotte", "UM": "United States Minor Outlying Islands", "LB": "Lebanon", "LC": "Saint Lucia",
        "LA": "Lao People's Democratic Republic", "TV": "Tuvalu", "TW": "Taiwan", "TT": "Trinidad and Tobago",
        "TR": "Turkey",
        "LK": "Sri Lanka", "LI": "Liechtenstein", "LV": "Latvia", "TO": "Tonga", "LT": "Lithuania", "LU": "Luxembourg",
        "LR": "Liberia", "LS": "Lesotho", "TH": "Thailand", "TF": "French Southern Territories", "TG": "Togo",
        "TD": "Chad",
        "TC": "Turks and Caicos Islands", "LY": "Libyan Arab Jamahiriya", "VA": "Holy See (Vatican City State)",
        "VC": "Saint Vincent and the Grenadines", "AE": "United Arab Emirates", "AD": "Andorra",
        "AG": "Antigua and Barbuda",
        "VG": "Virgin Islands", "AI": "Anguilla", "VI": "Virgin Islands", "IS": "Iceland", "IR": "Iran",
        "AM": "Armenia",
        "AL": "Albania", "AO": "Angola", "AN": "Netherlands Antilles", "AQ": "Antarctica", "AS": "American Samoa",
        "AR": "Argentina", "AU": "Australia", "AT": "Austria", "IO": "British Indian Ocean Territory", "IN": "India",
        "TZ": "Tanzania", "AZ": "Azerbaijan", "IE": "Ireland", "ID": "Indonesia", "UA": "Ukraine", "QA": "Qatar",
        "MZ": "Mozambique"
    }
