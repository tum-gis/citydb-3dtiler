import yaml

class Advisement(yaml.YAMLObject):
    yaml_tag = u'!Advisement'
    def __init__(self, commandset, maxfeature, command=None):
        self.usedCommandSet = commandset
        self.maximumFeaturePerTile = maxfeature
    
    def to_oneline_command(self):
        return f"citydb-3dtiler {self.usedCommandSet['command']} --db-host {self.usedCommandSet['db_host']} --db-port {self.usedCommandSet['db_port']} --db-name {self.usedCommandSet['db_name']} --db-schema {self.usedCommandSet['db_schema']} --db-username {self.usedCommandSet['db_username']} --db-password SOMETHING --consider-thematic-features {self.usedCommandSet['consider_thematic_features']} --output {self.usedCommandSet['output']}"
    def to_yaml(self):
        dict4yaml = {"usedCommand": self.to_oneline_command(), "maximumFeaturePerTile": self.maximumFeaturePerTile}
        return dict4yaml