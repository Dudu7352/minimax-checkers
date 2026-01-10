def side_by_side(*strs: list[str]):
    str_arrs = [s.split("\n") for s in strs]
    result = ""
    for i in range(len(str_arrs[0])):
        result += "    ".join(s[i] for s in str_arrs)
        result += "\n"
    return result