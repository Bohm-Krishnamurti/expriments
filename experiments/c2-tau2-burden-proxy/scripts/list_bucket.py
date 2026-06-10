#!/usr/bin/env python3
"""List all keys under submissions/ on sierra-tau-bench-public (anonymous), following continuation tokens."""
import urllib.request, urllib.parse, xml.etree.ElementTree as ET, sys

BASE = "https://sierra-tau-bench-public.s3.amazonaws.com/"
NS = "{http://s3.amazonaws.com/doc/2006-03-01/}"

def list_all(prefix="submissions/"):
    keys, token = [], None
    while True:
        params = {"list-type": "2", "prefix": prefix, "max-keys": "1000"}
        if token:
            params["continuation-token"] = token
        url = BASE + "?" + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url) as r:
            root = ET.fromstring(r.read())
        for c in root.findall(NS + "Contents"):
            keys.append((c.find(NS + "Key").text, int(c.find(NS + "Size").text)))
        if root.find(NS + "IsTruncated").text == "true":
            token = root.find(NS + "NextContinuationToken").text
        else:
            break
    return keys

if __name__ == "__main__":
    keys = list_all()
    with open(sys.argv[1] if len(sys.argv) > 1 else "/dev/stdout", "w") as f:
        for k, s in keys:
            f.write(f"{s}\t{k}\n")
    print(f"total keys: {len(keys)}", file=sys.stderr)
