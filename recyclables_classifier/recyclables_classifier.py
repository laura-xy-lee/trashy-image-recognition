import PyPDF2
# from itertools import chain

pdf_file = open('recyclables_classifier/list-of-items-that-are-recyclable-and-not.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()

header = "List of common items that can and cannot be placed in the recycling bins S/N Material  Type Item Items that can be placed in the blue  commingled recycling bins Items that cannot be placed in the blue  commingled recycling bins"

# Get material types
material_types = []
for page_number in range(number_of_pages):
    page = read_pdf.getPage(page_number)
    page_content = page.extractText()

    page_content = page_content.lower()
    page_content = page_content.replace('\n',' ')
    page_content = page_content.replace(header.lower(), '')

    for i in range(len(page_content.split())):
        word = page_content.split()[i]
        # The word after a digit is always the material type
        if word.isdigit():
            material_type = page_content.split()[i+1]
            material_types.append(material_type)

material_types = set(material_types)
# print("Material types are", material_types)

all_items = []
for page_number in range(number_of_pages):
    page = read_pdf.getPage(page_number)
    page_content = page.extractText()

    page_content = page_content.lower()
    page_content = page_content.replace('\n',' ')
    page_content = page_content.replace(header.lower(), '')

    for i in range(len(page_content.split())-1):
        word = page_content.split()[i]
        word_after = page_content.split()[i+1]

        # Get item name and information
        item_info = []
        if word.isdigit() and word_after in material_types:
            for j in range(i+2, len(page_content.split())):
                word_j = page_content.split()[j]
                if word_j.isdigit():
                    break
                else:
                    item_info.append(word_j)
            item_info = ' '.join(item_info)

            # Tidy item information
            # Items that cannot be recycled at all
            if "dispose as general waste" in item_info:
                item_info = item_info.replace("dispose as general waste", "")
                all_items.append([word_after,
                                  item_info.strip(),
                                  "This is not recyclable"])

            # Items that cannot be recycled but can be donated
            elif len(item_info.split("donate")) > 1 and "book" not in item_info:
                all_items.append([word_after,
                                  item_info.split("donate")[0].strip(),
                                  'This is not recyclable, but please donate' + item_info.split("donate")[1]])


            # Items that can be recycled but can be donated
            elif len(item_info.split("donate")) > 1:
                all_items.append([word_after,
                                  item_info.split("donate")[0].strip(),
                                  'This is recyclable, but please donate' + item_info.split("donate")[1]])

            # Items that can only be recycled in special bins
            elif "recycled" in item_info:
                item_info = item_info.replace("could be recycled", "can be recycled").split("can be recycled")
                all_items.append([word_after,
                                  item_info[0].strip(),
                                  "This is recyclable, but only" + item_info[1]])

            # Items that only landed estates can recycle
            elif "landed estates" in item_info:
                item_info = item_info.split("only for landed estates")
                all_items.append([word_after,
                                  item_info[0].strip(),
                                  "This is recyclable, but only for landed estates" + item_info[1]])

            # Items that need instructions before recycling
            elif "please" in item_info:
                item_info = item_info.split("please")
                instruction = [item_info[instruction_id].replace("-", "").strip() for instruction_id in range(1, len(item_info))]
                instruction = " and ".join(instruction)
                all_items.append([word_after,
                                  item_info[0].strip(),
                                  "This is recyclable, but before that, please " + instruction])

            else:
                all_items.append([word_after,
                                  item_info.strip(),
                                  "This is recyclable"])

# # Tidy item name
# for item in all_items:
#
#     # Remove unnecessary text
#     strings = ['(glossy and non-glossy)', '(with and without plastic window)', "(except for"]
#     if any(s in item[1] for s in strings):
#         pass
#         # print([item[0],
#         #        [item[1].split("(")[0].strip()],
#         #        item[2]])
#
#     # If examples of items are given, add to list
#     elif "e.g." in item[1]:
#         item_name = item[1].split("(e.g.")
#
#         item_name = item_name[1].split(",") + [item_name[0]]
#         item_name = [i.replace("etc", "").strip() for i in item_name]
#         item_name = [i.replace(")", "").strip() for i in item_name]
#         item_name = [i.split(" -") for i in item_name]
#         item_name = list(chain.from_iterable(item_name))
#         item_name = [i.split("/") for i in item_name]
#         item_name = list(chain.from_iterable(item_name))
#         item_name = [i.replace(".", "").strip() for i in item_name]
#         item_name = [i.split(" and ") for i in item_name]
#         item_name = list(chain.from_iterable(item_name))
#         item_name = [i.split(" or ") for i in item_name]
#         item_name = list(chain.from_iterable(item_name))
#
#         item_name = [i.strip() for i in item_name]
#         item_name = list(filter(None, item_name))
#         # print([item[0],
#         #        item_name,
#         #        item[2]])
#
#     else:
#         print(item)


def classify(item_label):

    _material_type = "UNKNOWN"
    _instruction = "Please dispose as general waste"

    for guess in item_label:

        for classification in all_items:
            for g in guess.split(","):
                if g.lower() in classification[1]:
                    _material_type = classification[0].upper()
                    _instruction = classification[2]
                    print("item is", g.lower())
                    print("classification is", classification[1])
                    return {"material_type": _material_type,
                            "instruction": _instruction}

    return {"material_type": _material_type,
            "instruction": _instruction}
