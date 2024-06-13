def get_extractor(file_name):
    if "mid" in file_name.lower():
        from .midas_extractor import MidasExtractor
        return MidasExtractor()
    elif "bgo" in file_name.lower():
        from .bigo_extractor import BigoExtractor
        return BigoExtractor()
    else:
        return None