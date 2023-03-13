"""I18n Utilities."""
import os
import json
import locale


class I18nManager:
    """Manage the translation database, this is a read only object."""

    def __init__(self, file_path: str, language: str = None):
        """Manage the translation database.

        Args:
            file_path (str): The path of the translation database
            language (str): The locale string ej. es-MX, en-US etc.

        Raises:
            FileNotFoundError: If the translation database
                cannot be found you will get this error.
        """
        if not language:
            locale.setlocale(locale.LC_ALL, "")
            language = locale.getlocale(locale.LC_MESSAGES)[0].split("_")[0]

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exists.")

        # Load translations database
        with open(file_path, 'r') as translations:
            self.__translations = json.load(translations)[language]

    def __getitem__(self, key: str):
        """Override the getitem python monad.

        Args:
            key (str): The key of the string item

        Returns:
            str: The indexed string
        """
        return self.__translations[key]
        # No overengenieer

    def __setitem__(self, __key: str, __value):
        # READONLY !!!
        """Override the setitem python monad.

        Args:
            __key (str): The item key
            __value (any): The new value

        Raises:
            AttributeError: This exception raises when you try to edit the
                database
        """
        raise AttributeError("Translations database class is readonly")

    # def __getattribute__(self, __name: str):
    #     """Override Python get attribute monad.

    #     Args:
    #         __name (str): The name of the attribute.

    #     Returns:
    #         Any: The translation string assciated to the key.
    #     """
    #     # The translations dictionary keys will be accesible via
    #     # Namespace operator "."
    #     print(__name)
    #     return self.__translations[__name]

    # def __setattr__(self, __name: str, __value):
    #     """Override the set attribute Python monad.

    #     Args:
    #         __name (str): The name of the string value.
    #         __value (Any): The Translation string associated to the string
    #             in the database.

    #     Raises:
    #         AttributeError: The database is in ReadOnly mode!.
    #     """
    #     # ReadOnly !
    #     raise AttributeError("The translation database is a readonly object")

    def __len__(self):
        """Override the the Python lenght operator.

        Returns:
            int: Is the number of elements in the translation database
        """
        return len(self.__translations.keys())


def initalize_i18n_manager(forced_locale: str = None):
    """Init I18n module.

    Args:
        forced_locale (str, optional): Forces to the module to load an
            specific language. Defaults to None.

    Returns:
        I18nManager: Wrapper for the I18n translation database
    """
    if not os.path.exists("./src/config.json"):
        with open('./src/config.json', 'w+') as f:
            default_content = ("{\n\t\"i18n_database_path\""
                               ":\"./src/i18n/strings.json\"\n}")
            f.write(default_content)
    with open('./src/config.json', 'r') as f:
        config = json.load(f)

    string_manager = I18nManager(config["i18n_database_path"], forced_locale)
    return string_manager

LOCALES = initalize_i18n_manager()
