#!/usr/bin/env python3

"""
@file hw.py
@version 0.0.1b
@brief Defines the class that runs the module as a program.


For more information, see:

    https://github.com/fuzzyklein2/workshop-0.0.1b
"""

# The initial output of any CGI script is mandatory.
print('Content-Type: text/html\n')                  

from pathlib import Path
import sys
import urllib.parse


LOCATION_PATH = Path.home() / '.pygnition.location.txt'
IGNITION_PATH = LOCATION_PATH.read_text().strip()
sys.path.insert(0, str(IGNITION_PATH))
print(f'''<html><body>
<p>Running <code>{Path(__file__).name}</code> ...</p>
''')

# # print('<!DOCTYPE html>')
# print(f'''<html><body><p>Running <code>{__file__}</code></p>''')

try:
    from pygnition.imports import *
    print('<p><code>pygnition./code> imported successfully.</p>')
except ModuleNotFoundError:
    print(f"""<pre style="color: red; font-weight: bold">
ERROR: Program module not found!
IGNITION_PATH={IGNITION_PATH}
    </pre>
    """)

from pygnition.configure import *
print(f'<p>{CHECK_PICT}<code>configure</code> module imported successfully.</p>')

from pygnition.lumberjack import *
print(f'<p>{CHECK_PICT}<code>lumberjack</code> imported successfully.</p>')

from pygnition.environment import *
print(f'<p>{CHECK_PICT}<code>environment</code> imported successfully.</p>')

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

"""
# --- Example usage ---
if __name__ == "__main__":
    data = get_cgi_params(single_values=True)
    print("Content-Type: text/plain\n")
    print("Params:", data)
"""

class CGISettings():
    def __init__(self):
        self.params = get_cgi_params()

    def output(self):
        print(f"""<p><code>cgpygnition./code> parameters:</p><pre style="font-weight: bold">
{pformat(self.params)}
</pre>
""")


# class CGIProgram(Program):
#     pass

if __name__ == '__main__':
    print(f'<p><code>{sys.argv=}</code></p>')

    settings = CGISettings()

    settings.output()
    
    print(f'<p><code>{Path(__file__).name}</code> execution complete.</p></body></html>')
