import PyPDF2
import re
from typing import Sequence, Dict


def split_string_at_numbers(s):
    return list(filter(None, re.split(r'(\d+)', s)))


# Get list of recyclables from NEA pdf
pdf_file = open('classify_trash/list-of-items-that-are-recyclable-and-not.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
nea_recyclables = ""
for page_number in range(number_of_pages):
    page = read_pdf.getPage(page_number)
    page_content = page.extractText()
    nea_recyclables = nea_recyclables + page_content

# Format text
header = "List of common items that can and cannot be placed in the recycling bins S/N Material  Type Item Items that can be placed in the blue  commingled recycling bins Items that cannot be placed in the blue  commingled recycling bins"
manually_remove_text = "see no.42)"
nea_recyclables = (nea_recyclables
                   .lower()
                   .replace('\n', ' ')
                   .replace('/', ' ')
                   .replace(header.lower(), ' ')
                   .replace(manually_remove_text.lower(), ' '))
nea_recyclables = re.sub(' +', ' ', nea_recyclables)

# Manually add for Hackathon demo
manually_add_text = "plastic plastic bottle container water bottle"
nea_recyclables = nea_recyclables.replace("plastic plastic bottle container", manually_add_text)

nea_recyclables = split_string_at_numbers(nea_recyclables)
nea_recyclables = [word.strip()
                   for word in nea_recyclables
                   if not word.isdigit()]

# Tidy text into `material`, `item_name`, `action`, `special_instruction'
nea_recyclables = [{"material": i.split(' ', 1)[0],
                    "item_name": i.split(' ', 1)[1],
                    "action": "Unknown",
                    "special_instructions": "Unknown"}
                   for i in nea_recyclables]

for item in nea_recyclables:
    dispose_text = "dispose as general waste"
    donate_text = "donate"
    recycle_text_1 = "can be recycled"
    recycle_text_2 = "could be recycled"
    landed_estate_text = "only for landed estates"
    instructions_text = "please"

    # Non recyclables
    if dispose_text in item["item_name"]:
        item["action"] = "Non-recyclable"
        item["special_instructions"] = "None"
        item["item_name"] = (item["item_name"]
                             .replace(dispose_text, " ")
                             .strip())

    # Non recyclables that can be donated
    elif donate_text in item["item_name"] and "book" not in item["item_name"]:
        item["action"] = "Non-recyclable"
        item["special_instructions"] = (donate_text + " "
                                        + item["item_name"]
                                        .split(donate_text, 1)[1]
                                        .strip())
        item["item_name"] = (item["item_name"]
                             .split(donate_text, 1)[0]
                             .strip())

    # Recyclables that can be donated
    elif donate_text in item["item_name"]:
        item["action"] = "Recyclable"
        item["special_instructions"] = (donate_text + " "
                                        + item["item_name"]
                                        .split(donate_text, 1)[1]
                                        .strip())
        item["item_name"] = (item["item_name"]
                             .split(donate_text, 1)[0]
                             .strip())

    # E-waste
    elif ("e-waste" in item["item_name"]
          and (recycle_text_1 in item["item_name"]
               or recycle_text_2 in item["item_name"])):
        item["action"] = "E-waste"
        item["special_instructions"] = "None"
        item["item_name"] = (item["item_name"]
                             .split(recycle_text_1, 1)[0]
                             .split(recycle_text_2, 1)[0]
                             .strip())

    # Lighting waste
    elif ("lighting waste" in item["item_name"]
          and (recycle_text_1 in item["item_name"]
               or recycle_text_2 in item["item_name"])):
        item["action"] = "Lighting waste"
        item["special_instructions"] = "None"
        item["item_name"] = (item["item_name"]
                             .split(recycle_text_1, 1)[0]
                             .split(recycle_text_2, 1)[0]
                             .strip())

    # Items that only landed estates can recycle
    elif landed_estate_text in item["item_name"]:
        item["action"] = "Recyclable"
        item["special_instructions"] = (landed_estate_text + " "
                                        + item["item_name"]
                                        .split(landed_estate_text, 1)[1]
                                        .strip())
        item["item_name"] = (item["item_name"]
                             .split(landed_estate_text, 1)[0]
                             .strip())

    # Items that have instructions before recycling
    elif instructions_text in item["item_name"]:
        item["action"] = "Recyclable"
        item["special_instructions"] = (instructions_text + " "
                                        + item["item_name"]
                                        .split(instructions_text, 1)[1]
                                        .strip())
        item["item_name"] = (item["item_name"]
                             .split(instructions_text, 1)[0]
                             .strip())

    else:
        item["action"] = "Recyclable"
        item["special_instructions"] = "None"


def classify_recyclable_trash(trash: Sequence,
                              classification: Sequence[Dict]=nea_recyclables):
    for t in trash:
        for c in classification:
            if t in c["item_name"]:
                return c

    return {'material': 'Unknown',
            'item_name': 'Unknown',
            'action': 'Unknown',
            'special_instructions': 'None'}
