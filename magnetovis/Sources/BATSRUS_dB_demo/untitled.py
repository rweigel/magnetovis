def timestr(filename, date=None):
    import re
    parts = re.search('_e(\d{8})\-(\d{6})\-(\d{3})', filename).groups()
    print(parts)
    time = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6] + "." + parts[2]
    if date is None:
        date = parts[0][0:4] + "-" + parts[0][4:6] + "-" + parts[0][6:8]

    print(date)
    return date + "T" + time

print(timestr('3d__var_1_e20000101-001000-000.out.cdf.vtk.j_phi'))