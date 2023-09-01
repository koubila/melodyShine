import sys

if len(sys.argv) > 1:
    form_id = sys.argv[1]
    modified_id = "http://209.97.183.63/partitions/" + form_id + ".xml"  # Add .xml to the form_id
    print(modified_id)
else:
    print("Form ID not provided.")