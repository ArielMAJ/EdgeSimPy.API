import edge_sim_py as esp
from edge_sim_py.component_manager import ComponentManager
from loguru import logger
from mesa import Agent


class ServiceManagementAgent(ComponentManager, Agent):
    _instances = []
    """List of all `ServiceManagementAgent` instances created."""

    _object_count = 0
    """Counter to assign unique IDs to each `ServiceManagementAgent` instance."""

    def __init__(self, service: esp.Service):
        self.service: esp.Service = service

        self.__class__._instances.append(self)
        self.__class__._object_count += 1

        self.id: int = self.service.id
        """Unique identifier for the service."""

    def step(self) -> None:
        if self._service_is_already_hosted_or_deploying():
            logger.info(f"[Agent {self.id}] No actions")
            return
        logger.info(f"[Agent {self.id}] Finding host for service {self.service.id}")

        servers: list[esp.EdgeServer] = esp.EdgeServer.all()
        if not self.service.users and not self.service.application.users:
            return self._place_self_in_the_first_available_server(servers)
        self._place_self_near_own_services_users(servers)

    def _place_self_in_the_first_available_server(
        self, servers: list[esp.EdgeServer]
    ) -> None:
        available_server: esp.EdgeServer = self._find_available_server(servers)
        self.service.provision(available_server)

    def _service_is_already_hosted_or_deploying(self):
        return self.service.server is not None or self.service.being_provisioned

    def _find_available_server(self, servers: list[esp.EdgeServer]) -> esp.EdgeServer:
        for server in servers:
            if server.has_capacity_to_host(self.service):
                return server
        return None

    @property
    def coordinates(self) -> tuple[int, int] | None:
        """2-tuple that represents the agent's geographical coordinates"""
        if not self.service.server:
            return None
        return self.service.server.coordinates

    def _place_self_near_own_services_users(self, servers: list[esp.EdgeServer]):
        self.migration_solicitation(incoming_service=self.service, servers=servers)

    def _euclidian_distance(
        self, coord1: tuple[int, int] | None, coord2: tuple[int, int] | None
    ) -> float:
        if coord1 is None or coord2 is None:
            return float("inf")
        return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5

    def _average_user_distance(self, server: esp.EdgeServer | None) -> float:
        if not server:
            return float("inf")
        distances = [
            self._euclidian_distance(user.coordinates, server.coordinates)
            for user in set(self.service.users + self.service.application.users)
        ]
        distances = list(filter(lambda value: value != float("inf"), distances))
        if not distances:
            return float("inf")
        return sum(distances) / len(distances)

    def migration_solicitation(
        self, incoming_service, servers: list[esp.EdgeServer], depth=0
    ):
        servers.sort(key=self._average_user_distance)

        current_distance_to_users = self._average_user_distance(self.service.server)
        for server in servers:
            if server == self.service.server:
                continue
            if self._average_user_distance(server) > current_distance_to_users:
                break
            if not server.has_capacity_to_host(self.service) and depth <= 2:
                for service in server.services:
                    if service != self.service and service != incoming_service:
                        service.agent.migration_solicitation(
                            incoming_service=self.service,
                            servers=servers,
                            depth=depth + 1,
                        )
            if server.has_capacity_to_host(self.service):
                logger.info(
                    f"[Agent {self.id}] Directing service to Server {server.id}"
                )
                self.service.provision(server)
                return
