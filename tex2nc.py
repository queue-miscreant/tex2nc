import subprocess
import tempfile
import os.path
import notcurses.notcurses as nc
import shutil
import random

LATEX_FILE = "texput"
LATEX_ARGS = ["latex"]
DVIPNG_ARGS = ["dvipng", "-fg", "White", "-bg", "Black", "-T", "tight", "-D", "231.26"]

LATEX_START = """
\\documentclass{article}
\\usepackage{amsmath,amsfonts,amsthm}
\\usepackage{xcolor}
\\usepackage[active]{preview}
\\begin{document}
\\begin{preview}
\\[
"""

LATEX_END = """
\\]
\\end{preview}
\\end{document}
"""

class TexError(Exception):
    def __init__(self, *args, latex_output=None, dvi_output=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.add_note(f"latex output:\n{latex_output}")
        self.add_note(f"dvipng output:\n{latex_output}")

def texify(string, tempdir):
    latex_process = subprocess.Popen(
        LATEX_ARGS + ["-output-directory=" + tempdir],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    latex_output, _ = latex_process.communicate((LATEX_START + string + LATEX_END).encode())
    latex_process.wait()

    outfile = os.path.join(tempdir, f"{LATEX_FILE}.png")

    dvi_process = subprocess.Popen(
        DVIPNG_ARGS + [
            os.path.join(tempdir, f"{LATEX_FILE}.dvi"),
            "-o",
            outfile,
        ],
        stdout=subprocess.PIPE
    )

    dvi_output, _ = dvi_process.communicate()
    latex_process.wait()

    if not os.path.exists(outfile):
        raise TexError(
            "Could not generate valid image",
            latex_output=latex_output.decode(),
            dvi_output=dvi_output.decode(),
        )

    return outfile

def main():
    temp_path = os.path.join("/dev/shm/", "latex-" + "".join([str(random.randrange(0, 10)) for i in range(3)]))
    os.mkdir(temp_path)

    tex_file = texify(input(), temp_path)

    direct = nc.Ncdirect()
    nc.lib.ncdirect_render_image(
        direct.nc,
        tex_file.encode(),
        nc.lib.NCALIGN_LEFT,
        nc.lib.NCBLIT_PIXEL,
        nc.lib.NCSCALE_SCALE,
    )

    shutil.rmtree(temp_path)

if __name__ == "__main__":
    main()
