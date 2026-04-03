## Classes
class Language:
    def __init__(self, file="res://data/foobar.json"):
        self.load_lang(file)
    
    @property
    def properties(self):
        """The metadata in the language file."""
        return self._file["properties"]
    @property
    def entries(self):
        """The entries in the language file."""
        return self._file["entries"]
    @property
    def name(self):
        """The name of the language."""
        return self.properties["name"]
    @property
    def base(self):
        """The language to use if an entry is not found."""
        return self.properties["base"]
    
    def load_lang(self,file):
        """Load a language file.
        
        Args:
            file: The filepath."""
        import classes.singleton as engine

        self._file = engine.loader.load(file)
        if self._file["properties"]["base"]:
            _base = Language(self._file["properties"]["base"])
            for i in _base.entries:
                if not i in self.entries:
                    self.entries[i] = _base.entries[i]
    
    def get(self, entry):
        """Get a localized entry from the language file.
        
        Args:
            entry: The name of the entry."""
        return self.entries.get(entry, entry)