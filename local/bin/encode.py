import argparse
import uuid
from datetime import datetime, timezone
import os
from bs4 import BeautifulSoup
import re
import subprocess
import shutil
import pathlib
import platform

DELIMITERS = {
    'STX': '\u0002',
    'ETX': '\u0003',
    'FS': '\u001C',
    'GS': '\u001D',
    'RS': '\u001E',
    'US': '\u001F',
    'CR': '\r',
    'LF': '\n',
    'LS': ';'
}

OPENSSL_BIN = "C:\\Program Files\\OpenSSL-Win64\\bin"

def get_lynx_executable():
    lynx_env = os.environ.get("LYNX_PATH")
    if lynx_env and os.path.isfile(lynx_env):
        return lynx_env
    found = shutil.which("lynx")
    return found if found else None

def clean_html_with_lynx(html_path: str) -> str:
    lynx_exec = get_lynx_executable()
    # print(f"Detected lynx executable: {lynx_exec}")

    if not lynx_exec:
        print("Error: lynx not found. Please install lynx or set the LYNX_PATH environment variable.")
        return ""

    try:
        lynx_dir = os.path.dirname(lynx_exec)
        cwd = lynx_dir if os.path.isdir(lynx_dir) else None
        env = os.environ.copy()
        env["PATH"] = OPENSSL_BIN + os.pathsep + env["PATH"]

        abs_path = pathlib.Path(html_path).resolve()
        if not abs_path.exists():
            raise FileNotFoundError(f"File not found: {abs_path}")

        if abs_path.suffix != ".html":
            raise ValueError("Input file must have a .html extension to be processed correctly by Lynx")

        file_uri = abs_path.as_uri()

        result = subprocess.check_output([
            lynx_exec,
            "-dump",
            "-nolist",
            "-nomargins",
            "-nonumbers",
            "-width=1000",
            file_uri
        ], text=True, cwd=cwd, env=env)
        return result
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError) as e:
        print(f"Error using lynx: {e}")
        return ""
    except OSError as e:
        print(f"Execution failed: {e}")
        return ""

def encode_corpus(text: str, filename: str = "untitled.txt") -> str:
    uid = str(uuid.uuid4())[:8]
    timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
    title = os.path.splitext(os.path.basename(filename))[0].replace('_', ' ')

    text = re.sub(r'(?<!\w)\.(?=\s+[A-Z])', DELIMITERS['LS'], text)
    text = re.sub(r'(?<!\s),(?!\s)', '', text)
    text = re.sub(r'\s+([;:.!?])', r'\1', text)
    text = re.sub(r'([;:.!?])(?!\s|$)', r'\1 ', text)

    corpus = DELIMITERS['STX']
    corpus += f"filename≜{filename}{DELIMITERS['LS']}"
    corpus += f"uid≜{uid}{DELIMITERS['LS']}"
    corpus += f"timestamp≜{timestamp}{DELIMITERS['LS']}"
    corpus += f"title≜{title}{DELIMITERS['LF']}"
    corpus += text
    corpus += DELIMITERS['ETX']
    return f"```{corpus}```"

def main():
    parser = argparse.ArgumentParser(description="Encode cleaned Wikipedia HTML into symbolic corpus format")
    parser.add_argument("input", help="Path to raw HTML input file")
    parser.add_argument("output", help="Path to output .txt corpus file")
    args = parser.parse_args()

    clean_text = clean_html_with_lynx(args.input)

    encoded = encode_corpus(clean_text, filename=args.output)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"Encoded corpus written to {args.output}")

if __name__ == "__main__":
    main()
