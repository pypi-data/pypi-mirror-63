"""Support for handling datapane script projects"""

import dataclasses as dc
import re
import sys
from pathlib import Path

import dacite
import jsonschema
import yaml

from dp_common import JDict, log

# app paths
sys_dir = Path(sys.executable if getattr(sys, "frozen", False) else __file__).parent
res_dir = sys_dir / "resources"
DATAPANE_YAML = Path("datapane.yaml")


def get_res_path(res_name: str) -> Path:
    return res_dir / res_name


re_check_name = re.compile("^[a-z0-9-_]+$")


def valid_script_name(x: str):
    if re_check_name.match(x) is None:
        raise AssertionError(f"'{x}' is not a valid service name, must be [a-z0-9-_]")


def default_title() -> str:
    return "Default Title"


@dc.dataclass
class DatapaneCfg:
    """Wrapper around the datapane config file"""

    config: JDict
    name: str
    docker_image: str = None
    title: str = dc.field(default_factory=default_title)

    def __post_init__(self):
        valid_script_name(self.name)

        log.debug("testing")

        # validate config
        config_schema = get_res_path("function_config_def.schema.json").read_text()
        jsonschema.validate(self.config, config_schema)

    @classmethod
    def create(cls) -> "DatapaneCfg":
        with DATAPANE_YAML.open("r") as f:
            config = yaml.safe_load(f)
        return dacite.from_dict(cls, data=config)
