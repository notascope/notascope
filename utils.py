def slug_from_path(path):
    return ".".join(path.split("/")[-1].split(".")[:-1])
