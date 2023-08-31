# HL7 message parsing using Python

### Install hl7 library
1. python-hl7 is available on PyPi via pip or easy_install:

    `pip install -U hl7`

2. For recent versions of Debian and Ubuntu, the *python-hl7* package is available:

    `sudo apt-get install python-hl7`

Dig deeper, check [python-hl7 documentation](https://readthedocs.org/projects/python-hl7/downloads/pdf/latest/)

### Running code
    `python hl7_parsing_demo.py`
   
### Dependencies
1. A HL7 file containing possibly multiple hl7 messages. Use the provided *sample_hl7_01.hl7* file.
2. Code is designed to parse a HL7 VXU 2.5.1 message but other types of messages can be parsed with minor adjustments.

### Output
1. A CSV file with each row containing data extracted from each hl7 message in the input file. See *tabular_output.csv*.
2. The columns correspond to select data elements from a hl7 message.

### Algorithm
1. Parse each hl7 message in the file to a hl7 container object.
2. Convert the container object to a custom dictionary whose keys will correspond to select data elements of interest.
3. Append dictionary to a list.
4. Convert the list of dictionaries to a dataframe.
5. Output the dataframe to a CSV file.
