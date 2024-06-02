import os, logging
from typing import List
from scripts.setup_logging import setup_logging

def find_missing_files(files: List[str]):
    """
    checks if some of the model responses are missing in the out folder,
    uses a format "q[query-id-numder]_[model-name]" with the delimiter "_"

    Parameters:
    -----------
        files: List[str]
            a list of file names where it must find missing files
    Returns:
    --------
        missing_files: str
            a list of missing files
    """

    delimiter = "_"

    # parse the file names into a dictionary
    res = {}
    for file in files:
        try:
            tmp = file.split(delimiter)
            query_id = int(tmp[0][1:])
            model_name = tmp[1]
            if model_name in res.keys():
                res[model_name].append(query_id)
            else:
                res[model_name] = [query_id]
        except Exception:
            logging.exception(f"During checking output files an exception has been raised.\nFile's name = {file}")
    
    # sort each list of query ids
    for query_ids in res.values():
        query_ids.sort()

    # initialize counters for each model name
    counters = {}
    for model_name in res.keys():
        if not model_name in counters.values():
            counters[model_name] = 0

    # find missing files
    missing_files = []
    for model_name, query_ids in res.items():
        for query_id in query_ids:
            if query_id - 1 != counters[model_name]:
                for missing_id in range(counters[model_name] + 1, query_id):
                    missing_files.append("q" + str(missing_id) + "_" + model_name)
            counters[model_name] = query_id

    return missing_files

def load_files_from(dir_path: str) -> List[str]:
    """
    loads file names by a given path

    Parameters:
    -----------
        dir_path: str
            a path to the directory where it must load file names
    
    Returns:
    --------
        file_names: List[str]
            a list with loaded file names
    """

    # load all existing files to a list
    entries = os.listdir(dir_path)
    file_names = [entry for entry in entries if os.path.isfile(os.path.join(dir_path, entry))]

    return file_names

def run_checking():
    setup_logging()
    file_names = load_files_from("out/")
    logging.info(file_names)
    missing_files = find_missing_files(file_names)
    res = "The following files are missing: \n"
    for file in missing_files:
        res += file + "\n"
    logging.info(res)

if __name__ == "__main__":
    run_checking()

    


