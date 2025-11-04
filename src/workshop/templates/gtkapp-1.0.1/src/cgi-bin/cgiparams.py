#!/usr/bin/env python3
import os
import sys
import urllib.parse

def get_cgi_params(single_values: bool = False) -> dict:
    """Return CGI params as a dictionary (works for GET and POST)."""
    params = {}

    # --- GET params ---
    query_string = os.environ.get("QUERY_STRING", "")
    if query_string:
        params.update(urllib.parse.parse_qs(query_string))

    # --- POST params ---
    if os.environ.get("REQUEST_METHOD", "").upper() == "POST":
        try:
            content_length = int(os.environ.get("CONTENT_LENGTH", 0))
        except ValueError:
            content_length = 0

        if content_length > 0:
            post_data = sys.stdin.read(content_length)
            post_params = urllib.parse.parse_qs(post_data)
            # merge with GET
            for k, v in post_params.items():
                params.setdefault(k, []).extend(v)

    # Collapse lists to single values if requested
    if single_values:
        params = {k: v[0] if v else None for k, v in params.items()}

    return params

# --- Example usage ---
if __name__ == "__main__":
    data = get_cgi_params(single_values=True)
    print("Content-Type: text/plain\n")
    print("Params:", data)
