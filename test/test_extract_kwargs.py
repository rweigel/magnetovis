from magnetovis.Objects.Axis import Script

from magnetovis import extract_kwargs, extract_function_call

print(extract_kwargs(Script))

print(extract_kwargs("circle(a=1)"))

print(extract_function_call(Script))
#print(extract_script(Script, None))
