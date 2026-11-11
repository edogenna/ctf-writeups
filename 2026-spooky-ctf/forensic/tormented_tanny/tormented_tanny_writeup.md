# SpookyCTF 2026 - Tormented Tanny Writeup

## Challenge Description

**Category:** Forensics

For this challenge, we are provided with an image file named `TormentedTanny.jpg` (which actually appears to be a PNG under the hood based on its chunk structure). The goal is to investigate the file and uncover a hidden flag.

## Analysis and Extraction

A standard first step in image forensics is to check the file's metadata and look for embedded strings. We can do this using command-line tools like `exiftool` or `strings`. 

Running the `strings` command on the image reveals a lot of standard PNG chunk headers (`IHDR`, `IDAT`, etc.) and XMP metadata XML tags. However, upon closer inspection of the output (as seen in the provided `stringhe_2.txt` file), we can spot pieces of the flag scattered across different metadata fields.

The flag has been split into three distinct parts:

### Part 1: The Title
Looking near the top of the strings output, we see a `tEXtTitle` chunk:
```text
tEXtTitle
spooky{tormented_tanner_
```
This gives us the beginning of our flag: `spooky{tormented_tanner_`

### Part 2: The Description
Continuing down into the XMP metadata XML structure, specifically within the `<dc:description>` tags, we find the next piece:
```xml
  <dc:description>
   <rdf:Alt>
    <rdf:li xml:lang='x-default'>hates_his_</rdf:li>
   </rdf:Alt>
  </dc:description>
```
This gives us the middle section: `hates_his_`

### Part 3: EXIF / Trailing String
Right after the XMP packet ends and near the EXIF header (`deXIfMM`), we see the final string before the image data (`IDAT`) begins:
```text
vetsulin}
```
This gives us the final part to close the curly brace: `vetsulin}`

## Conclusion

By carefully examining the metadata and strings embedded within the image file, we were able to find three separate strings. Concatenating them in order gives us the complete flag.

**Flag:** `spooky{tormented_tanner_hates_his_vetsulin}`