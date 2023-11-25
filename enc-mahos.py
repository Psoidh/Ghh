#!/usr/bin/env python
# coding: utf-8
# مهووس


import os
import sys
import subprocess
import argparse
import random
import time
import marshal
import lzma
import gzip
import bz2
import binascii
import zlib





def prett(text):
    return text.title().center(os.get_terminal_size().columns)


PYTHON_VERSION = "python" + ".".join(str(i) for i in sys.version_info[:2])
try:
    import requests
    import tqdm
    import colorama
    import pyfiglet
except ModuleNotFoundError:
    if (
        subprocess.run(
            [PYTHON_VERSION, "-m", "pip", "install", "-r", "requirements.txt"]
        ).returncode
        == 0
    ):
        print("\x1b[1m\x1b[92m" + prett("[+] dependencies installed"))
        sys.exit("\x1b[1m\x1b[92m" + prett("[+] run the program again"))
    elif subprocess.run(["pip3", "install", "-r", "requirements.txt"]).returncode == 0:
        print("\x1b[1m\x1b[92m" + prett("[+] dependencies installed"))
        sys.exit("\x1b[1m\x1b[92m" + prett("[+] run the program again"))
    else:
        print(
            "\x1b[1m\x1b[31m"
            + prett("[!] something error occured while installing dependencies")
        )
        sys.exit(
            "\x1b[1m\x1b[31m"
            + prett("maybe pip isn't installed or requirements.txt file not available?")
        )
BLU = colorama.Style.BRIGHT + colorama.Fore.BLUE
CYA = colorama.Style.BRIGHT + colorama.Fore.CYAN
GRE = colorama.Style.BRIGHT + colorama.Fore.GREEN
YEL = colorama.Style.BRIGHT + colorama.Fore.YELLOW
RED = colorama.Style.BRIGHT + colorama.Fore.RED
MAG = colorama.Style.BRIGHT + colorama.Fore.MAGENTA
LIYEL = colorama.Style.BRIGHT + colorama.Fore.LIGHTYELLOW_EX
LIRED = colorama.Style.BRIGHT + colorama.Fore.LIGHTRED_EX
LIMAG = colorama.Style.BRIGHT + colorama.Fore.LIGHTMAGENTA_EX
LIBLU = colorama.Style.BRIGHT + colorama.Fore.LIGHTBLUE_EX
LICYA = colorama.Style.BRIGHT + colorama.Fore.LIGHTCYAN_EX
LIGRE = colorama.Style.BRIGHT + colorama.Fore.LIGHTGREEN_EX
CLEAR = "cls" if os.name == "nt" else "clear"
COLORS = BLU, CYA, GRE, YEL, RED, MAG, LIYEL, LIRED, LIMAG, LIBLU, LICYA, LIGRE
FONTS = (
    "basic",
    "o8",
    "cosmic",
    "graffiti",
    "chunky",
    "epic",
    "poison",
    "doom",
    "avatar",
)

global LATEST_VER
colorama.init(autoreset=True)


def encode(source: str) -> str:
    selected_mode = random.choice((lzma, gzip, bz2, binascii, zlib))
    marshal_encoded = marshal.dumps(compile(source, "enc-mahos", "exec"))
    if selected_mode is binascii:
        return "import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads(binascii.a2b_base64({})))".format(
            binascii.b2a_base64(marshal_encoded)
        )
    return "import marshal,lzma,gzip,bz2,binascii,zlib;exec(marshal.loads({}.decompress({})))".format(
        selected_mode.__name__, selected_mode.compress(marshal_encoded)
    )


def logo() -> None:
    _ = subprocess.run([CLEAR], shell=True)
    font = random.choice(FONTS)
    color1 = random.choice(COLORS)
    color2 = random.choice(COLORS)
    while color1 == color2:
        color2 = random.choice(COLORS)
    print(color1 + "_" * os.get_terminal_size().columns, end="\n" * 2)
    print(
        color2
        + pyfiglet.figlet_format(
            "enc\nmahos",
            font=font,
            justify="center",
            width=os.get_terminal_size().columns,
        ),
        end="",
    )
    print(color1 + "_" * os.get_terminal_size().columns, end="\n" * 2)


def parse_args():
    parser = argparse.ArgumentParser(description="تعليمات مهمه جدا".title())
    parser._optionals.title = "يرجى اتباعاها".title()
    parser.add_argument(
        "-i", "--input", type=str, help="ادخل اسم الملف".title(), required=True
    )
    parser.add_argument(
        "-o", "--output", type=str, help="ادخل اسم الملف بعد التشفير".title(), required=True
    )
    parser.add_argument(
        "-c",
        "--complexity",
        type=int,
        help="عدد التشفير من 1 - 100 اقصى عدد".title(),
        required=True,
    )
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()
    return parser.parse_args()


def check_update():
    LATEST_VER = requests.get(
        "https://raw.githubusercontent.com/Psoidh/Insta/main/enc-mahos"
    ).text.strip()
    with open(".version") as version:
        return True if float(version.read().strip()) < float(LATEST_VER) else False


def update():
    if ".git" in os.listdir():
        _ = subprocess.run(["git", "stash"], check=True)
        _ = subprocess.run(["git", "pull"], check=True)
    else:
        latest_source = requests.get(
            "https://raw.githubusercontent.com/Psoidh/Insta/main/encode"
        ).content
        with open("enc-mahos.py", "wb") as file:
            file.write(latest_source)
        with open(".version", "w") as file:
            file.write(LATEST_VER)


def main():
    args = parse_args()
    if check_update():
        print(RED + prett("[!] update available"))
        print(LIGRE + prett("[+] updating..."))
        update()
        print(LIGRE + prett("[+] successfully updated..."))
        sys.exit(LIGRE + prett("run the program again"))
    print(random.choice(COLORS) + "\t[+] encoding ".title() + args.input)
    with tqdm.tqdm(total=args.complexity) as pbar:
        with open(args.input) as iput:
            for i in range(args.complexity):
                if i == 0:
                    encoded = encode(source=iput.read())
                else:
                    encoded = encode(source=encoded)
                time.sleep(0.1)
                pbar.update(1)
    with open(args.output, "w") as output:
        output.write(
            f'# Encoded By @maho_s9\n# https://t.me/maho9s\n# اصدار بايثون {PYTHON_VERSION} \n# الاصدار الاول ١.٦\ntry:\n\t{encoded}\nexcept KeyboardInterrupt:\n\texit()'
        )
    print(LIGRE + "\t[+] تم التشفير بنجاح\n\tsaved as ".title() + args.output)


if __name__ == "__main__":
    logo()
    main()
    
