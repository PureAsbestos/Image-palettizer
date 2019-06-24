import os
import sys

# Based on https://learning-python.com/cgi/showcode.py?name=pyedit-products/unzipped/multiprocessing_exe_patch.py

# Problem only occurs on Windows when running in onefile mode
if sys.platform.startswith('win') and hasattr(sys, 'frozen'):

    # Module multiprocessing is organized differently in Python 3.4+
    try:
        # Python 3.4+
        import multiprocess.popen_spawn_win32 as forking
    except ImportError:
        # This program doesn't officially support Python < 3.6, but this is the import
        # to use for Python < 3.4
        import multiprocess.forking as forking


    # First define a modified version of Popen.  # ML: this is a no-op otherwise
    class _Popen(forking.Popen):
        def __init__(self, *args, **kwargs):
            # We have to set original _MEIPASS2 value from sys._MEIPASS
            # to get --onefile mode working.
            os.putenv('_MEIPASS2', sys._MEIPASS)

            try:
                super(_Popen, self).__init__(*args, **kwargs)
            finally:
                # On some platforms (e.g. AIX) 'os.unsetenv()' is not
                # available. In those cases we cannot delete the variable
                # but only set it to the empty string. The bootloader
                # can handle this case.
                if hasattr(os, 'unsetenv'):
                    os.unsetenv('_MEIPASS2')
                else:
                    os.putenv('_MEIPASS2', '')

    # Second override 'Popen' class with our modified version.
    # This happens in all contexts, whether __main__ or not.
    forking.Popen = _Popen
