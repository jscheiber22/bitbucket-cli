def read(path):
    try:
        f = open(path, "r")
        lines = f.readlines()
        return lines[0].replace("\n", "")
        f.close()
    except:
        try:
            f = open(path + ".txt", "r")
            lines = f.readlines()
            return lines[0].replace("\n", "")
            f.close()
        except:
            print("Read operation failed.")
