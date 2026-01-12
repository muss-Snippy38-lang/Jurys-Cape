# app/services/law_mapper.py

# A small sample mapping. In a real app, you'd load a full JSON file here.
MAPPING_DATA = {
    "302": {"bns": "101", "title": "Murder", "note": "Punishment is now under Section 103."},
    "420": {"bns": "318", "title": "Cheating", "note": "Now part of 'Offences against Property'."},
    "376": {"bns": "64", "title": "Rape", "note": "Definitions tightened; higher penalties."},
}

def get_bns_equivalent(ipc_section: str):
    section = ipc_section.replace("Section ", "").strip()
    return MAPPING_DATA.get(section, {"error": "Section mapping not found in local database."})