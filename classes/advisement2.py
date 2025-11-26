from collections.abc import MutableMapping

class TransformedDict(MutableMapping):
    """A dictionary that applies an arbitrary key-altering
       function before accessing the keys"""

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.store[self._keytransform(key)]

    def __setitem__(self, key, value):
        self.store[self._keytransform(key)] = value

    def __delitem__(self, key):
        del self.store[self._keytransform(key)]

    def __iter__(self):
        return iter(self.store)
    
    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return str(self.store)

    def _keytransform(self, key):
        return key

class Advisement(TransformedDict):
    def __init__(self, commandset, max_features=None, objectclasses=None):
        super().__init__()
        self.store["commandset"] = commandset
        self.store["max_features"] = max_features
        self.store["objectclasses"] = objectclasses
    def _keytransform(self, key):
        return key.lower()

class ObjectClass(TransformedDict):
    def __init__(self, name, objectclass_recommendations=None):
        super().__init__()
        self.store["name"] = name
        if objectclass_recommendations != None:
            self.store["objectclass_recommendations"] = objectclass_recommendations

class ObjectClassRecommendations(TransformedDict):
    def __init__(self, max_features):
        super().__init__()
        self.store["max_features"] = max_features



# import yaml

# class Advisement(yaml.YAMLObject):
#     yaml_tag = u'!Advisement'
#     def __init__(self, commandset, maxfeature=None, objectclasses=None, command=None):
#         self.usedCommandSet = commandset
#         self.maximumFeaturePerTile = maxfeature
#         self.availableObjectclasses = objectclasses
    
#     def to_oneline_command(self):
#         cmmnd = f"citydb-3dtiler {self.usedCommandSet['command']} --db-host {self.usedCommandSet['db_host']} --db-port {self.usedCommandSet['db_port']} --db-name {self.usedCommandSet['db_name']} --db-schema {self.usedCommandSet['db_schema']} --db-username {self.usedCommandSet['db_username']} --db-password SOMETHING --consider-thematic-features {self.usedCommandSet['consider_thematic_features']} --output {self.usedCommandSet['output']}"
#         return cmmnd
#     def to_yaml(self):
#         dict4yaml = {"usedCommand": self.to_oneline_command(), "maximumFeaturePerTile": self.maximumFeaturePerTile, "availableObjectclasses": str(self.availableObjectclasses)}
#         return dict4yaml

# class ObjectClass(dict):
#     # yaml_tag = u'!ObjectClass'
#     def __init__(self, name, recommended_max_features=None):
#         self.name = name
#         self.recommended_max_features = recommended_max_features
#     def __repr__(self):
#         dct = dict(name=self.name, recommended_max_features=self.recommended_max_features)
#         return str(dct)
#     # def to_yaml(self):
#     #     dict4yaml = {"name": self.name, "maximumFeaturePerTile": self.maximumFeaturePerTile}
#     #     return dict4yaml

# class ObjectClasses(dict):
#     # yaml_tag = u'!ObjectClasses'
#     def __init__(self, *objectclasses):
#         self.objectclasses = []
#         for oc in objectclasses:
#             self.objectclasses.append(oc)
#     def __repr__(self):
#         arr = []
#         for oc in self.objectclasses:
#             arr.append(oc)
#         return str(arr)
#     def append(self, objectclass):
#         self.objectclasses.append(objectclass)
#     # def to_yaml(self):
#     #     oc_arr = []
#     #     for oc in self.objectclasses:
#     #         oc_arr.append(oc)
#     #     return oc_arr

