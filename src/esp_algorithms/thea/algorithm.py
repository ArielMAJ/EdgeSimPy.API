import edge_sim_py as esp
from loguru import logger

from src.esp_algorithms.thea.related_methods import (
    find_minimum_and_maximum,
    get_application_delay_score,
    get_application_privacy_score,
    get_host_candidates,
    get_norm,
)


def thea(parameters: dict = {}):
    """Heuristic algorithm that provisions composite applications on federated edge
    infrastructures taking into account the delay and privacy requirements of
    applications, the trust degree between application users and infrastructure
    providers, and the power consumption of edge servers.

    Args:
        parameters (dict, optional): Algorithm parameters. Defaults to {}.
    """

    logger.info(f"[STEP {parameters['current_step']}]")

    apps_metadata = []
    for app in esp.Application.all():
        app_attrs = {
            "object": app,
            "number_of_services": len(app.services),
            "delay_sla": app.users[0].delay_slas[str(app.id)],
            "delay_score": get_application_delay_score(app=app),
            "privacy_score": get_application_privacy_score(app=app),
        }
        apps_metadata.append(app_attrs)

    min_and_max = find_minimum_and_maximum(metadata=apps_metadata)
    apps_metadata = sorted(
        apps_metadata,
        key=lambda app: (
            get_norm(
                metadata=app,
                attr_name="delay_score",
                min=min_and_max["minimum"],
                max=min_and_max["maximum"],
            )
            + get_norm(  # noqa
                metadata=app,
                attr_name="privacy_score",
                min=min_and_max["minimum"],
                max=min_and_max["maximum"],
            )
        ),
        reverse=True,
    )

    for app_metadata in apps_metadata:
        app = app_metadata["object"]
        user = app.users[0]

        for service in app.services:
            edge_servers = get_host_candidates(user=user, service=service)

            min_and_max = find_minimum_and_maximum(metadata=edge_servers)

            edge_servers = sorted(
                edge_servers,
                key=lambda s: (
                    s["sla_violations"],
                    get_norm(  # noqa
                        metadata=s,
                        attr_name="affected_services_cost",
                        min=min_and_max["minimum"],
                        max=min_and_max["maximum"],
                    )
                    + get_norm(  # noqa
                        metadata=s,
                        attr_name="power_consumption",
                        min=min_and_max["minimum"],
                        max=min_and_max["maximum"],
                    )
                    + get_norm(  # noqa
                        metadata=s,
                        attr_name="delay_cost",
                        min=min_and_max["minimum"],
                        max=min_and_max["maximum"],
                    ),
                ),
            )

            for edge_server_metadata in edge_servers:
                edge_server = edge_server_metadata["object"]
                if edge_server.has_capacity_to_host(service=service):
                    if service.server != edge_server:
                        service.provision(target_server=edge_server)
                        break
