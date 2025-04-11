# flake8: noqa

import edge_sim_py as esp


def get_application_delay_score(app: object) -> float:
    """Calculates the application delay score considering the number application's SLA and the number of edge servers close enough
    to the application's user that could be used to host the application's services without violating the delay SLA.

    Args:
        app (object): Application whose delay score will be calculated.

    Returns:
        app_delay_score (float): Application's delay score.
    """

    delay_sla = app.users[0].delay_slas[str(app.id)]
    user_switch = app.users[0].base_station.network_switch

    edge_servers_that_dont_violate_delay_sla = 0
    for edge_server in esp.EdgeServer.all():
        topology = user_switch.model.topology
        path = find_shortest_path(
            origin_network_switch=user_switch,
            target_network_switch=edge_server.network_switch,
        )
        delay = topology.calculate_path_delay(path=path)
        if delay <= delay_sla:
            edge_servers_that_dont_violate_delay_sla += 1

    if edge_servers_that_dont_violate_delay_sla == 0:
        app_delay_score = 0
    else:
        app_delay_score = 1 / (
            (edge_servers_that_dont_violate_delay_sla * delay_sla) ** (1 / 2)
        )

    app_delay_score = app_delay_score * len(app.services)

    return app_delay_score


def find_shortest_path(
    origin_network_switch: object, target_network_switch: object
) -> int:
    import networkx as nx

    """Finds the shortest path (delay used as weight) between two network switches (origin and target).

    Args:
        origin_network_switch (object): Origin network switch.
        target_network_switch (object): Target network switch.

    Returns:
        path (list): Shortest path between the origin and target network switches.
    """
    topology = origin_network_switch.model.topology
    path = []

    if not hasattr(topology, "delay_shortest_paths"):
        topology.delay_shortest_paths = {}

    key = (origin_network_switch, target_network_switch)

    if key in topology.delay_shortest_paths.keys():
        path = topology.delay_shortest_paths[key]
    else:
        path = nx.shortest_path(
            G=topology,
            source=origin_network_switch,
            target=target_network_switch,
            weight="delay",
        )
        topology.delay_shortest_paths[key] = path

    return path


def normalize_cpu_and_memory(cpu, memory) -> float:
    """Normalizes the CPU and memory values.

    Args:
        cpu (float): CPU value.
        memory (float): Memory value.

    Returns:
        normalized_value (float): Normalized value.
    """
    normalized_value = (cpu * memory) ** (1 / 2)
    return normalized_value


def find_minimum_and_maximum(metadata: list):
    """Finds the minimum and maximum values of a list of dictionaries.

    Args:
        metadata (list): List of dictionaries that contains the analyzed metadata.

    Returns:
        min_and_max (dict): Dictionary that contains the minimum and maximum values of the attributes.
    """
    min_and_max = {
        "minimum": {},
        "maximum": {},
    }

    for metadata_item in metadata:
        for attr_name, attr_value in metadata_item.items():
            if attr_name != "object":
                if (
                    attr_name not in min_and_max["minimum"]
                    or attr_name in min_and_max["minimum"]
                    and attr_value < min_and_max["minimum"][attr_name]
                ):
                    min_and_max["minimum"][attr_name] = attr_value

                if (
                    attr_name not in min_and_max["maximum"]
                    or attr_name in min_and_max["maximum"]
                    and attr_value > min_and_max["maximum"][attr_name]
                ):
                    min_and_max["maximum"][attr_name] = attr_value

    return min_and_max


def min_max_norm(x, min, max):
    """Normalizes a given value (x) using the Min-Max Normalization method.

    Args:
        x (any): Value that must be normalized.
        min (any): Minimum value known.
        max (any): Maximum value known.

    Returns:
        (any): Normalized value.
    """
    if min == max:
        return 1
    return (x - min) / (max - min)


def get_norm(metadata: dict, attr_name: str, min: dict, max: dict) -> float:
    """Wrapper to normalize a value using the Min-Max Normalization method.

    Args:
        metadata (dict): Dictionary that contains the metadata of the object whose values are being normalized.
        attr_name (str): Name of the attribute that must be normalized.
        min (dict): Dictionary that contains the minimum values of the attributes.
        max (dict): Dictionary that contains the maximum values of the attributes.

    Returns:
        normalized_value (float): Normalized value.
    """
    normalized_value = min_max_norm(
        x=metadata[attr_name], min=min[attr_name], max=max[attr_name]
    )
    return normalized_value


def calculate_path_delay(
    origin_network_switch: object, target_network_switch: object
) -> int:
    """Gets the distance (in terms of delay) between two network switches (origin and target).

    Args:
        origin_network_switch (object): Origin network switch.
        target_network_switch (object): Target network switch.

    Returns:
        delay (int): Delay between the origin and target network switches.
    """
    topology = origin_network_switch.model.topology

    path = find_shortest_path(
        origin_network_switch=origin_network_switch,
        target_network_switch=target_network_switch,
    )

    delay = topology.calculate_path_delay(path=path)

    return delay


def sign(value: int):
    """Calculates the sign of a real number using the well-known "sign" function (https://wikipedia.org/wiki/Sign_function).

    Args:
        value (int): Value whose sign must be calculated.

    Returns:
        (int): Sign of the passed value.
    """
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def get_application_privacy_score(app: object):
    """Calculates the application privacy score considering the demand and privacy requirements of its services.

    Args:
        app (object): Application whose privacy score will be calculated.

    Returns:
        app_privacy_score (float): Application's privacy score.
    """
    app_privacy_score = 0

    for service in app.services:
        normalized_demand = normalize_cpu_and_memory(
            cpu=service.cpu_demand, memory=service.memory_demand
        )
        privacy_requirement = service.privacy_requirement
        service_privacy_score = normalized_demand * (1 + privacy_requirement)
        app_privacy_score += service_privacy_score

    return app_privacy_score


def get_host_candidates(user: object, service: object) -> list:
    """Get list of host candidates for hosting services of a given user.
    Args:
        user (object): User object.
    Returns:
        host_candidates (list): List of host candidates.
    """
    chain = list([service.application.users[0]] + service.application.services)
    prev_item = chain[chain.index(service) - 1]
    switch_of_previous_item_in_chain = (
        prev_item.base_station.network_switch
        if chain.index(service) - 1 == 0
        else prev_item.server.network_switch
    )
    app_delay = (
        user.delays[str(service.application.id)]
        if user.delays[str(service.application.id)] is not None
        else 0
    )

    host_candidates = []

    for edge_server in esp.EdgeServer.all():
        additional_delay = calculate_path_delay(
            origin_network_switch=switch_of_previous_item_in_chain,
            target_network_switch=edge_server.network_switch,
        )
        overall_delay = app_delay + additional_delay
        delay_cost = (
            additional_delay if service == service.application.services[-1] else 0
        )

        violates_privacy_sla = (
            1
            if user.providers_trust[str(edge_server.infrastructure_provider)]
            < service.privacy_requirement
            else 0
        )
        violates_delay_sla = (
            1 if overall_delay > user.delay_slas[str(service.application.id)] else 0
        )
        sla_violations = violates_delay_sla + violates_privacy_sla

        static_power_consumption = edge_server.power_model_parameters[
            "static_power_percentage"
        ]
        consumption_per_core = (
            edge_server.power_model_parameters["max_power_consumption"]
            / edge_server.cpu
        )
        power_consumption = consumption_per_core + static_power_consumption * (
            1 - sign(edge_server.cpu_demand)
        )

        affected_services = []
        for affected_service in esp.Service.all():
            affected_user = affected_service.application.users[0]
            trust_on_the_edge_server = affected_user.providers_trust[
                str(edge_server.infrastructure_provider)
            ]
            relies_on_the_edge_server = (
                trust_on_the_edge_server >= affected_service.privacy_requirement
            )

            if (
                affected_service.server is None
                and affected_service != service
                and relies_on_the_edge_server
            ):
                distance_to_affected_user = calculate_path_delay(
                    origin_network_switch=affected_user.base_station.network_switch,
                    target_network_switch=edge_server.network_switch,
                )
                distance_cost = 1 / max(1, distance_to_affected_user)
                affected_services.append(distance_cost)

        affected_services_cost = (
            sum(affected_services) if service == service.application.services[-1] else 0
        )

        host_candidates.append(
            {
                "object": edge_server,
                "sla_violations": sla_violations,
                "affected_services_cost": affected_services_cost,
                "power_consumption": power_consumption,
                "delay_cost": delay_cost,
            }
        )

    return host_candidates
