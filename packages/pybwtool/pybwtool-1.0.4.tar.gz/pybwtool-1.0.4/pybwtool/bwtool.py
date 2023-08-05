import subprocess
import os
from typing import Tuple
from .utils import is_loosely_bed, bed_has_header
from typing import List
import pandas as pd
from io import StringIO
import numpy as np


def bwtool_to_df(*args: List) -> pd.DataFrame:
    """Return DataFRame from bwtool with the given args."""
    df = pd.read_csv(StringIO(subprocess.run([
        "bwtool", *[str(arg) for arg in args], "/dev/stdout"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode("utf-8")), header=None, sep="\t")
    bed = df[df.columns[:3]]
    bed.columns = ["chrom", "chromStart", "chromEnd"]
    return bed, df[df.columns[-1]].str.split(",", expand=True).replace("NA", np.nan).astype(float)


def bwtool_to_file(*args: List, target: str = None):
    """Return DataFRame from bwtool with the given args."""
    subprocess.run([
        "bwtool", *[str(arg) for arg in args], "> {}".format(target)
    ])


def extract(bed_path: str, bigwig_path: str, target: str = None):
    """Return DataFrame with extracted data from given big wig files for regions specified in given.

    Parameters
    ----------------------------------------
    bed_path: str,
        the bed file from which to extract the regions.
    bigwig_path: str,
        the bigwig file from which to extract the data for the regions
    nan_threshold:float=0.95,
        Maximum percentage of nan to allow in a row to keep it,
        otherwise the row is dropped.
    target: str = None,
        Path where to write the extraction, optionally.
        It can be useful when extracting files that cannot
        be hold in RAM, expecially when handling multiprocessing.

    Raises
    -----------------------------------------
    ValueError:
        When one of the given file path does not exist.
    ValueError:
        When the file is not recognized as a bed file.
    ValueError:
        When the file contains an header.

    Returns
    ------------------------------------------
    Dataframe with extracted data.
    """

    for file_path in (bed_path, bigwig_path):
        if not os.path.exists(file_path):
            raise ValueError("Given file at path {file_path} does not exist.".format(
                file_path=file_path
            ))

    if not is_loosely_bed(bed_path):
        raise ValueError("Given bed candidate file at path {bed_path} is not a bed.".format(
            bed_path=bed_path
        ))

    if bed_has_header(bed_path):
        raise ValueError("Given bed file at path {bed_path} has a header: bwtools does not support bed files with headers".format(
            bed_path=bed_path
        ))
    if target is not None:
        bwtool_to_file("extract", "bed", bed_path, bigwig_path, target=target)
    return bwtool_to_df("extract", "bed", bed_path, bigwig_path,)