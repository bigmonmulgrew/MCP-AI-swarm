Dataset example:

{
    "_id": "68f1f2891291222c1367e675",
    "created": "17/10/2025",
    "datasource": "68f1f2511291222c1367e66c",
    "group": "67c95459bd679456b91c8d69",
    "index": "68f1f2891291222c1367e674",
    "name": "G-XWBM",
    "variables": [
        {
            "dtype": "float",
            "id": "68f1f2891291222c1367e671",
            "index": false,
            "label": "alt",
            "name": "alt",
            "threshold_id": "68f1f3f7038234ce6e64f64e",
            "units": "m"
        },
        {
            "dtype": "float",
            "id": "68f1f2891291222c1367e672",
            "index": false,
            "label": "lat",
            "name": "lat",
            "units": ""
        },
        {
            "dtype": "float",
            "id": "68f1f2891291222c1367e673",
            "index": false,
            "label": "lon",
            "name": "lon",
            "units": ""
        },
        {
            "dtype": "timestamp",
            "format": "%Y-%m-%dT%H:%M:%SZ",
            "id": "68f1f2891291222c1367e674",
            "index": true,
            "label": "timestamp",
            "name": "timestamp",
            "units": ""
        }
    ]
}



Data Example:

{
    "dimensions": [
        "index",
        "68f1f2891291222c1367e675_68f1f2891291222c1367e671",
        "68f1f2891291222c1367e675_68f1f2891291222c1367e672",
        "68f1f2891291222c1367e675_68f1f2891291222c1367e673"
    ],
    "id": "68f1f2891291222c1367e675",
    "source": [
        [
            1760650094000,
            0.0,
            51.46917,
            -0.47692
        ],
        [
            1760650214000,
            0.0,
            51.46917,
            -0.47716
        ],
        [
            1760650223000,
            0.0,
            51.46917,
            -0.47737
        ],
        [
            1760650236000,
            0.0,
            51.46917,
            -0.4776
        ],
        [
            1760650248000,
            0.0,
            51.46913,
            -0.47787
        ],
        [
            1760650259000,
            0.0,
            51.46912,
            -0.47815
        ],
        [
            1760650268000,
            0.0,
            51.46915,
            -0.47837
        ],
]
}
