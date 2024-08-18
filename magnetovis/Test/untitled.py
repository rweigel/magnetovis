demo_script = "sdfds\n# Demo 1\nsdfsdfdsfds\n# Demo 2\n sdfsdfsd"
import re
starts = []
for match in re.finditer("# Demo ", demo_script):
    starts.append(match.start())

print(starts)
parts = []
for idx in range(len(starts)-1):
    print(match.start(), match.end())
    parts.append(demo_script[starts[idx]:starts[idx+1]])

parts.append(demo_script[starts[idx+1]:])
print(parts)