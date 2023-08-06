from datacoco_core.config import config
from datacoco_secretsmanager import SecretsManager


class ConfigWrapper:
    """
    Wrapper file for config management for mssql_runner.
    """

    @staticmethod
    def sm_conf(project_name="maximilian", team_name="data"):
        """
        Simple config wrapper for using secrets manager.
        """
        c = SecretsManager().get_config(project_name, team_name)
        return c

    @staticmethod
    def extend_parser(parser):
        parser.add_argument(
            "--config",
            default="core",
            help="""
                whether to use secret_manager or
                datacoco_core to retrieve secrets
                """,
            choices=["secret_manager", "core"],
        )

        return parser

    @staticmethod
    def process_config(args):
        if args.config == "secret_manager":
            conf = ConfigWrapper.sm_conf()
        elif args.config == "core":
            conf = config()

        db_name = conf[args.database]["db_name"]
        host = conf[args.database]["server"]
        user = conf[args.database]["user"]
        password = conf[args.database]["password"]
        port = conf[args.database].get("port", 1433)

        return db_name, host, user, password, port
