from injector import Module, singleton
from app.teams.service import TeamsService
from app.teams.repository import TeamsRepository


class TeamsModule(Module):
    def configure(self, binder):
        binder.bind(TeamsRepository, scope=singleton)
        print("TeamsRepository initialized")
        binder.bind(TeamsService, scope=singleton)
        print("TeamsService initialized")
        print("TeamsModule initialized")
