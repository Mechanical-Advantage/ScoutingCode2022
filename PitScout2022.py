import csv
import sqlite3 as sql
from fpdf import FPDF
pdf = FPDF()
conn1 = sql.connect("c:\mascout\AdvantageScout\global.db")
cur1 = conn1.cursor()
cur1.execute("SELECT value FROM config WHERE key = 'event'")
Event = cur1.fetchall()[0][0]
conn = sql.connect("c:\mascout\AdvantageScout\data_2022.db")
cur = conn.cursor()
# event_name
cur.execute("SELECT * FROM pit WHERE Event = ? order by Team", (Event,))
Pitscout = cur.fetchall()

# THE LOOKUP
# if row[column] == 1:
#     lists[name_lookup[column]["section"]].append(name_lookup[column]["value"])
#
# THE JOIN
# ", ".join(lists[list_name])

# use for fields that have multiple items
name_lookup = {
    12: {
        "section": "auto",
        "value": "can taxi"
    },
    13: {
        "section": "auto",
        "value": "can deliver upper"
    },
    14: {
        "section": "auto",
        "value": "can deliver lower"
    },
    15: {
        "section": "shoot_to",
        "value": "upper goal"
    },
    16: {
        "section": "shoot_to",
        "value": "lower goal"
    },
    21: {
        "section": "shoot_from",
        "value": "fender"
    },
    22: {
        "section": "shoot_from",
        "value": "tarmac"
    },
    23: {
        "section": "shoot_from",
        "value": "launchpad"
    },
    24: {
        "section": "start_from",
        "value": "fender"
    },
    25: {
        "section": "start_from",
        "value": "tarmac"
    },
    26: {
        "section": "start_from",
        "value": "tarmac edge"
    },
    17: {
        "section": "climb_to",
        "value": "low bar"
    },
    18: {
        "section": "climb_to",
        "value": "mid bar"
    },
    19: {
        "section": "climb_to",
        "value": "high bar"
    },
    20: {
        "section": "climb_to",
        "value": "traversal bar"
    },
}
lists = {
    "auto": [],
    "shoot_to": [],
    "shoot_from": [],
    "start_from": [],
    "climb_to": []
}
# THE LOOKUP
# if row[column] == 1:
#     lists[name_lookup[column]["section"]].append(name_lookup[column]["value"])
#
# THE JOIN
# ", ".join(lists[list_name])

for row in Pitscout:
    lists = {
        "auto": [],
        "shoot_to": [],
        "shoot_from": [],
        "start_from": [],
        "climb_to": [],
    }
    for column in name_lookup.keys():
        if row[column] == 1:
            lists[name_lookup[column]["section"]].append(
                name_lookup[column]["value"])

    pdf.add_page()
    pdf.set_font('Arial', 'B', 30)
    pdf.cell(40, 10, 'Team ' + str(row[1]), ln=1)
    pdf.set_font('Arial', '', 14)
    pdf.cell(40, 10, 'Drive Train: ' + row[7], ln=1)
    pdf.cell(40, 10, 'Weight: ' + str(row[9]))
    pdf.cell(40, 10, 'Height: ' + str(row[10]), ln=1)
    pdf.cell(40, 10, 'Width: ' + str(row[10]))
    pdf.cell(40, 10, 'Length: ' + str(row[11]), ln=1)
    pdf.cell(60, 10, 'Max Auto Shots: ' + str(row[27]))
    pdf.cell(40, 10, 'Max Holding Capacity: ' + str(row[28]), ln=1)
    pdf.cell(40, 10, 'Auto Capabilities: ' + ", ".join(lists["auto"]), ln=1)
    pdf.cell(40, 10, 'Shooting Capabilities: ' +
             ", ".join(lists["shoot_to"]),  ln=1)
    pdf.cell(40, 10, 'Shooting Positions: ' +
             ", ".join(lists["shoot_from"]),  ln=1)
    pdf.cell(40, 10, 'Starting Positions: ' +
             ", ".join(lists["start_from"]), ln=1)
    pdf.cell(40, 10, 'Climb Levels: ' + ", ".join(lists["climb_to"]), ln=1)
    pdf.cell(40, 10, 'Comments: ' + str(row[2]), ln=1)

    if len(row[31]) >= 1:
        pdf.image("c:\mascout\\AdvantageScout\\" + row[31], 10, 120, 125)

pdf.output('pitscout2022.pdf', 'F')
conn.close()
conn1.close()
