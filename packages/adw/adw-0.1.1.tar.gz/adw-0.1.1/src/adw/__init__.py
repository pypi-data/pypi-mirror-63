from functools import update_wrapper
from pathlib import Path
import appdirs


__version__ = "0.1.1"


class Directories:
    """
    Base namespace object to hold all site directory paths.

    """

    def __init__(self, adw, name="site"):
        self._appdirs = adw
        self._name = name

    def __iter__(self):
        for name, obj in self.__dict__.items():
            if not name.startswith("_") and name.endswith("_dir"):
                yield name, obj

    def assert_directories(self):
        """
        Create all directory Paths if they do no already exist.

        """
        for name, obj in self:
            dirpath = getattr(self, name)
            dirpath.mkdir(parents=True, exist_ok=True)

    def to_string(self):
        """
        Visualize all default application directories.

        """
        info = []
        for name, obj in self:
            dir_type = name.split('_')[0]
            info.append(f"{self._name} {dir_type} dir:  {obj}")
        return '\n'.join(info)


class Site(Directories):
    """
    Namespace object to hold all site directory paths.

    """

    def __init__(self, adw):
        super().__init__(adw, 'site')
        self.data_dir = Path(self._appdirs.site_data_dir)
        self.config_dir = Path(self._appdirs.site_config_dir)


class User(Directories):
    """
    Namespace object to hold all user directory paths.

    """

    def __init__(self, adw):
        super().__init__(adw, "user")
        self.data_dir = Path(self._appdirs.user_data_dir)
        self.cache_dir = Path(self._appdirs.user_cache_dir)
        self.log_dir = Path(self._appdirs.user_log_dir)
        self.config_dir = Path(self._appdirs.user_config_dir)
        self.state_dir = Path(self._appdirs.user_state_dir)


class AppDirs:
    """
    Convenience wrapper object to the appdirs library.

    """

    def __init__(self, appname, version=None, appauthor=None):
        self._appdirs = _appdirs = appdirs.AppDirs(
            appname, appauthor=appauthor, version=version
        )
        self.user = User(_appdirs)
        self.site = Site(_appdirs)
