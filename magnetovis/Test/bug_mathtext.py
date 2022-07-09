# https://matplotlib.org/stable/tutorials/text/mathtext.html
#  "Regular text and mathtext can be interleaved within the same string."

# Enter in the Python Shell
view = GetActiveViewOrCreate('RenderView')
text = Text(Text=r"Plot of $\alpha^2$")
Show(text)