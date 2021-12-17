from magnetovis.Objects.Axis import Script

from magnetovis import extract_kwargs

print(extract_kwargs(Script))

print(extract_kwargs("circle(a=1)"))

#print(extract_script(Script, None))
