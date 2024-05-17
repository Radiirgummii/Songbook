from typing import Union, Never

def decode_lines(line: str) -> tuple[list[str], list[Union[str, Never]]]:
    """Recusively splits the string into line_par and chords"""
    if "{" in line or "}" in line:
        splitted_line = line.rsplit("}",1)
        splitted_line2 = splitted_line[0].rsplit("{",1)
        line_part, chords = decode_lines(splitted_line2[0])
        line_part.append(splitted_line[1])
        chords.append(splitted_line2[1])
        return line_part, chords
    else:
        return [line], []