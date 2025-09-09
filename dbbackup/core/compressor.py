"""
Handle compression of backup files (gzip by default).
"""
import gzip
import shutil 
import logging
from pathlib import Path

class Compressor:
    """
    Compressor class to compress files before storage.
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        
    def compress_file(self, file_path: str, method: str ="gzip"):
        """
        Compress a given file and return the path to the compressed file.

        Args:
            file_path (str): Path to the file to compress.
            method (str): Compression method ('gzip' supported).

        Returns:
            str: Path to the compressed file.
        """
        path = Path(file_path)
        
        if not path.is_file():
            self.logger.error(f"Cannot compress non-existent file: {file_path}")
            return file_path    # Return original if not exist
        
        if method.lower() == "gzip":
            compressed_path = path.with_suffix(path.suffix + ".gz")
            try:
                with open(path, "rb") as f_in, gzip.open(compressed_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
                self.logger.info(f"File compressed: {compressed_path}")
                return str(compressed_path)
            except Exception as e:
                self.logger.error(f"Compression failed for {file_path}: {e}")
                return str(path)
        else:
            self.logger.warning(f"Unsupported compression method '{method}', skipping compression.")
            return str(path)                  