# SpookyCTF 2026 - Tangled Writeup

## Challenge Description

**Category:** Forensics

In this challenge, we are provided with an image file named `tangled.jpg` (or `tangled.png` based on the extraction artifacts). The challenge title and the spiderweb imagery hint that something might be "tangled" or hidden within the file itself. Our objective is to untangle the hidden data and retrieve the flag.

## Analysis and Extraction

The first step in image forensics is to check for hidden embedded files or appended data. We can start by running the `strings` command on the image to see if there is any readable text.

Looking at the output (saved as `stringhe.txt`), we can clearly see the standard structure of a PNG file with chunks like `IHDR`, `sRGB`, `IDAT`, and `IEND`. However, right after the `IEND` chunk (which normally marks the absolute end of a PNG file), we spot something suspicious: the string `flag.txtux`. 

This strongly indicates that another file, likely an archive, has been appended to the end of the image.

### Using Binwalk

To automatically detect and extract the embedded data, we can use `binwalk`:

```bash
binwalk -e tangled.png
```

`binwalk` successfully detects the appended data and extracts it into a new directory named `_tangled.png.extracted`.

## Recovering the Flag

Looking inside the `_tangled.png.extracted` folder, we find a few extracted artifacts, including zlib compressed data (`3CA.zlib`) and a ZIP archive (`EE80D.zip`).

Since we saw `flag.txt` in the strings output, the ZIP archive is our primary target. We can unzip it:

```bash
unzip EE80D.zip
```

This extracts a file named `flag.txt`. When we read the contents of this text file, we find our flag!

```bash
cat flag.txt
spooky{8_l3gs_4nd_4_z1p}
```

## Conclusion

This was a classic steganography/forensics challenge involving file carving. By realizing that extra data was appended after the image's EOF (End of File) marker, we were able to use `binwalk` to extract the hidden ZIP archive and read the flag inside.