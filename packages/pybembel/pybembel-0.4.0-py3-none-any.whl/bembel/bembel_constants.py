default_framework_conf = """
{
    "properties": {
        "pelix.log.level": "INFO"
    },
    "bundles": [
        "pelix.ipopo.core",
        "pelix.services.configadmin",
        "pelix.shell.core",
        "pelix.shell.ipopo",
        "pelix.shell.configadmin",
        "pelix.shell.remote",
        "pelix.http.basic"
    ]
}
"""

empty_extra_bundles_conf = """
{
    "bundles": [

    ]
}
"""
