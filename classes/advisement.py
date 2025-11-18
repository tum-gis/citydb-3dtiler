import yaml

class Advisement(yaml.YAMLObject):
    yaml_tag = u'!Advisement'
    def __init__(self, commandset, maxfeature=None, objectclasses=None, command=None):
        self.usedCommandSet = commandset
        self.maximumFeaturePerTile = maxfeature
        self.availableObjectclasses = objectclasses
    
    def to_oneline_command(self):
        cmmnd = f"citydb-3dtiler {self.usedCommandSet['command']} --db-host {self.usedCommandSet['db_host']} --db-port {self.usedCommandSet['db_port']} --db-name {self.usedCommandSet['db_name']} --db-schema {self.usedCommandSet['db_schema']} --db-username {self.usedCommandSet['db_username']} --db-password SOMETHING --consider-thematic-features {self.usedCommandSet['consider_thematic_features']} --output {self.usedCommandSet['output']}"
        return cmmnd
    def to_yaml(self):
        dict4yaml = {"usedCommand": self.to_oneline_command(), "maximumFeaturePerTile": self.maximumFeaturePerTile, "availableObjectclasses": self.availableObjectclasses}
        return dict4yaml

# class ObjectClass:
#     yaml_tag = u'!ObjectClass'
#     def __init__(self, name, recommended_max_features=None):
#         self.name = name
#         self.recommended_max_features = recommended_max_features
#     def __repr__(self):
#         dct = dict(name=self.name, recommended_max_features=self.recommended_max_features)
#         return str(dct)
#     def to_yaml(self):
#         dict4yaml = {"name": self.name, "maximumFeaturePerTile": self.maximumFeaturePerTile}
#         return dict4yaml

# class ObjectClasses(yaml.YAMLObject):
#     yaml_tag = u'!ObjectClasses'
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
#     def to_yaml(self):
#         oc_arr = []
#         for oc in self.objectclasses:
#             oc_arr.append(oc)
#         return oc_arr

