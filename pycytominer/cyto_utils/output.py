"""
Utility function to compress output data
"""

import os
import warnings
import pandas as pd

compress_options = ["gzip", None]


def output(
    df,
    output_filename,
    sep=",",
    float_format=None,
    compression_options={"method": "gzip", "mtime": 1},
):
    """Given an output file and compression options, write file to disk

    Parameters
    ----------
    df :  pandas.core.frame.DataFrame
        a pandas dataframe that will be written to file
    output_filename : str
        location of file to write
    sep : str
        file delimiter
    float_format : str, default None
        Decimal precision to use in writing output file as input to
        pd.DataFrame.to_csv(float_format=float_format). For example, use "%.3g" for 3
        decimal precision.
    compression_options : str or dict, default {"method": "gzip", "mtime": 1}
        Contains compression options as input to
        pd.DataFrame.to_csv(compression=compression_options). pandas version >= 1.2.

    Returns
    -------
    None
        Writes to file

    Examples
    --------
    import pandas as pd
    from pycytominer.cyto_utils import output

    data_df = pd.concat(
        [
            pd.DataFrame(
                {
                    "Metadata_Plate": "X",
                    "Metadata_Well": "a",
                    "Cells_x": [0.1, 0.3, 0.8],
                    "Nuclei_y": [0.5, 0.3, 0.1],
                }
            ),
            pd.DataFrame(
                {
                    "Metadata_Plate": "X",
                    "Metadata_Well": "b",
                    "Cells_x": [0.4, 0.2, -0.5],
                    "Nuclei_y": [-0.8, 1.2, -0.5],
                }
            ),
        ]
    ).reset_index(drop=True)

    output_file = "test.csv.gz"
    output(
        df=data_df,
        output_filename=output_file,
        sep=",",
        compression_options={"method": "gzip", "mtime": 1},
        float_format=None,
    )
    """
    # Make sure the compression method is supported
    compression_options = set_compression_method(compression=compression_options)

    df.to_csv(
        path_or_buf=output_filename,
        sep=sep,
        index=False,
        float_format=float_format,
        compression=compression_options,
    )


def set_compression_method(compression):
    """Set the compression options

    Parameters
    ----------
    compression : str or dict
        Contains compression options as input to
        pd.DataFrame.to_csv(compression=compression_options). pandas version >= 1.2.

    Returns
    -------
    compression, dict
        A formated dictionary expected by output()
    """

    if compression is None:
        compression = {"method": None}

    if isinstance(compression, str):
        compression = {"method": compression}

    check_compression_method(compression["method"])
    return compression


def check_compression_method(compression):
    """Ensure compression options are set properly

    Parameters
    ----------
    compression : str
        The category of compression options available

    Returns
    -------
    None
        Asserts available options
    """
    assert (
        compression in compress_options
    ), "{} is not supported, select one of {}".format(compression, compress_options)
