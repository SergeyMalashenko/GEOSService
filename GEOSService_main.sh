#!/bin/bash
curl --location --request POST 'http://localhost:5000/api/buffer' \
--header 'Content-Type: application/json' \
--data-raw '
{
    "axis": {
        "regions": [
            {
                "polygons": [
                    [
                        {
                            "x": "2220908.78159082",
                            "y": "577637.63071684"
                        },
                        {
                            "x": "2220909.19752439",
                            "y": "577638.08471045"
                        },
                        {
                            "x": "2220908.4867991",
                            "y": "577638.735852903"
                        },
                        {
                            "x": "2220907.69921122",
                            "y": "577637.876196737"
                        },
                        {
                            "x": "2220908.34239803",
                            "y": "577637.286930758"
                        },
                        {
                            "x": "2220908.78159082",
                            "y": "577637.63071684"
                        }
                    ]
                ]
            }
        ],
        "lines": [
            {
                "points": [
                    {
                        "x": "2220942.407",
                        "y": "577604.686"
                    },
                    {
                        "x": "2220908.47",
                        "y": "577637.936"
                    }
                ]
            }
        ]
    },
    "resolution":4,
    "tolerance":0.5
}
'
