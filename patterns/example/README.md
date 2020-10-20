# Example Pattern readme

This directory demonstrates how to model a simple pattern within this repository.

The pattern itself is the default pattern boilerplate you get with the "New Pattern" button in the Pixelblaze IDE.

The portable form of a Pixelblaze pattern is a file with the `.epe` extension. The `.epe` format stores the source(s), name, id, and preview image within a JSON object.

These components are destructured when stored in this repo so that their component parts may be more easily collaborated with through source control tools.

Some data from this structure doesn't have a good alternative representation, so the remainder of the `.epe` data is stored in the `meta.json` text file with human-readable formatting. The pattern `name` and `id` are some of the attributes stored in `meta.json`.

The parent directory name loosely matches the pattern name, but needn't exactly match when the name contains characters that may be difficult to use as a directory name (like `/` or `-`).

# File Structure

```
{name}/
    sources/
        main.js
    preview.jpg
    meta.json
    README.md (this file)
```
