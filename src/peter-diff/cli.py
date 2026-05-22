import sys
import difflib
import shutil

# ANSI codes
_RESET  = "\033[0m"
_RED    = "\033[41m"   # deleted  (left)
_GREEN  = "\033[42m"   # inserted (right)
_YELLOW = "\033[43m"   # changed chars
_BOLD   = "\033[1m"


def _color_ok():
    return sys.stdout.isatty()


def _pad(text, width):
    """Truncate or pad *text* to exactly *width* visible characters."""
    if len(text) > width:
        return text[: width - 1] + "…"
    return text.ljust(width)


def _colored(text, code):
    if _color_ok():
        return code + text + _RESET
    return text


def _marker(tag, side):
    """Return a single visible marker char for no-colour terminals."""
    if tag == "equal":
        return " "
    if tag == "delete":
        return "<" if side == "left" else " "
    if tag == "insert":
        return " " if side == "left" else ">"
    return "|"


def _char_diff(left, right, col):
    """
    Return (left_str, right_str) with only the differing characters highlighted,
    each padded/truncated to exactly *col* visible characters.
    """
    matcher = difflib.SequenceMatcher(None, left, right, autojunk=False)
    l_segs, r_segs = [], []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        ls, rs = left[i1:i2], right[j1:j2]
        if tag == "equal":
            l_segs.append((ls, None))
            r_segs.append((rs, None))
        elif tag == "replace":
            l_segs.append((ls, _YELLOW))
            r_segs.append((rs, _YELLOW))
        elif tag == "delete":
            l_segs.append((ls, _RED))
        elif tag == "insert":
            r_segs.append((rs, _GREEN))

    def render(segs):
        out, vis = [], 0
        for text, code in segs:
            if vis >= col:
                break
            room = col - vis
            if len(text) > room:
                text = text[: room - 1] + "…"
            out.append((code + text + _RESET) if code else text)
            vis += len(text)
        if vis < col:
            out.append(" " * (col - vis))
        return "".join(out)

    return render(l_segs), render(r_segs)


def side_by_side_diff(lines1, lines2, file1, file2, only_diff=False):
    term_w = shutil.get_terminal_size((160, 40)).columns
    # layout: "NNNN M content … │ NNNN M content …"
    #          4  + 1+1+1 = 7 chars overhead each side  +  3 for " │ "
    overhead = 7 + 3 + 7
    col = max(20, (term_w - overhead) // 2)

    sep = "─" * (col + 8) + "┼" + "─" * (col + 7)
    use_color = _color_ok()

    # Header
    print(sep)
    lh = (_BOLD if use_color else "") + _pad(file1, col) + (_RESET if use_color else "")
    rh = (_BOLD if use_color else "") + _pad(file2, col) + (_RESET if use_color else "")
    print(f"{'':4} {'':1} {lh} │ {'':4} {'':1} {rh}")
    print(sep)

    def emit(lnum, rnum, l_raw, r_raw, tag):
        lnum_s = str(lnum) if lnum else ""
        rnum_s = str(rnum) if rnum else ""
        lm = _marker(tag, "left")
        rm = _marker(tag, "right")

        if use_color and tag == "replace":
            # character-level highlighting
            l_pad, r_pad = _char_diff(l_raw, r_raw, col)
        else:
            l_pad = _pad(l_raw, col)
            r_pad = _pad(r_raw, col)
            if use_color:
                if tag == "delete":
                    l_pad = _colored(l_pad, _RED)
                elif tag == "insert":
                    r_pad = _colored(r_pad, _GREEN)

        print(f"{lnum_s:<4} {lm} {l_pad} │ {rnum_s:<4} {rm} {r_pad}")

    matcher = difflib.SequenceMatcher(None, lines1, lines2, autojunk=False)
    lnum = rnum = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for l, r in zip(lines1[i1:i2], lines2[j1:j2]):
                lnum += 1; rnum += 1
                if not only_diff:
                    emit(lnum, rnum, l.rstrip("\n"), r.rstrip("\n"), "equal")

        elif tag == "replace":
            lc, rc = lines1[i1:i2], lines2[j1:j2]
            for k in range(max(len(lc), len(rc))):
                l_raw = r_raw = ""
                ln = rn = None
                if k < len(lc):
                    lnum += 1; ln = lnum; l_raw = lc[k].rstrip("\n")
                if k < len(rc):
                    rnum += 1; rn = rnum; r_raw = rc[k].rstrip("\n")
                emit(ln, rn, l_raw, r_raw, "replace")

        elif tag == "delete":
            for l in lines1[i1:i2]:
                lnum += 1
                emit(lnum, None, l.rstrip("\n"), "", "delete")

        elif tag == "insert":
            for r in lines2[j1:j2]:
                rnum += 1
                emit(None, rnum, "", r.rstrip("\n"), "insert")

    print(sep)


def main():
    args = sys.argv[1:]
    only_diff = "-o" in args
    args = [a for a in args if a != "-o"]
    if len(args) != 2:
        print("Usage: peter-diff [-o] file1 file2", file=sys.stderr)
        sys.exit(1)
    file1, file2 = args[0], args[1]
    try:
        with open(file1) as f1, open(file2) as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    side_by_side_diff(lines1, lines2, file1, file2, only_diff=only_diff)


if __name__ == "__main__":
    main()

