def read(path):
    try:
        f = open(path, "r")
        lines = f.readlines()
        return lines[0].replace("\n", "")

    except:
        print("Operation failed.")
    finally:
        f.close()
