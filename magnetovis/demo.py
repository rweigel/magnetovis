def demo(name):

    import os
    import magnetovis as mvs

    mvs.ClearPipeline()
    base = os.path.dirname(os.path.abspath(mvs.__file__))
    file = os.path.join(base, "Sources", name + "_demo.py")
    return open(file, encoding="utf-8").read()
