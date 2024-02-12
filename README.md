tex2nc
======

Script which converts LaTeX input to notcurses output.

Dependencies:

- Linux
- pdflatex
- notcurses 3.*

Uses a temporary directory in `/dev/shm` to store intermediate files.

Results are displayed in white text on black background.

Uses notcurses's pixel blitter for tmux compatibility.
