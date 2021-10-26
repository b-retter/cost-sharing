import numpy as np

# Define classes

class Service():
    def __init__(self,name,cost,owner) -> None:
        self.name = name
        self.cost = cost
        self.owner = owner
        self.clients = []
        self.total_claim = 0

        owner.register_as_owner(self)

    def print_clients(self):
        for client in self.clients:
            print(client.name)

    def update_clients(self,client):
        if client not in self.clients:
            self.clients.append(client)

        self.total_claim = sum([client.service_fractions[self] for client in self.clients])
        for client in self.clients:
            client.service_costs[self] = self.cost/self.total_claim * client.service_fractions[self]



class Person():
    def __init__(self,name) -> None:
        self.name = name
        self.outgoings = {}
        self.services = []
        self.service_fractions = {}
        self.service_costs = {}

    def register_as_owner(self,service):
        self.outgoings[service.name] = service.cost

    def add_outgoing(self,outgoings):
        self.outgoings.update({outgoing.name:outgoing.cost for outgoing in outgoings})
    
    def add_service(self,service,service_fraction):
        """Add name and fraction of service
        
        Parameters:
        service_fraction: float
            fraction of service used.
        """
        if service not in self.services:
            self.services.append(service)
        
        self.service_fractions[service] = service_fraction
        service.update_clients(self)

    def update_service_cost(self,service,cost):
        self.service_costs[service] = cost


    def print_services(self):
        for service in self.services:
            print(f"{service.name} : £{self.service_costs[service]:.2f}")
        print(f"Total (expected) outgoings: £{self.expected_outgoings:.2f}")
        print(f"Total (actual) outgoings: £{self.actual_outgoings:.2f}")

        outgoings_diff = self.expected_outgoings-self.actual_outgoings
        print(f"Expected - Actual: {str(np.sign(outgoings_diff))[0] if outgoings_diff < 0 else ''}£{np.abs(outgoings_diff):.2f}")

    @property
    def expected_outgoings(self):
        return sum([cost for cost in self.service_costs.values()])

    @property
    def actual_outgoings(self):
        return sum(self.outgoings.values())

def register_services(person,services_and_fractions):
    for service,fraction in services_and_fractions.items():
        person.add_service(service,fraction)

def people_overview(people):
    for person in people.values():
        print(person.name)
        person.print_services()
        print('\n')

people = ["Brendan", "Megan","Bethan","Tom","Celia","Matt"]
people = {name: Person(name) for name in people}

services = {
    "netflix": Service("netflix",13.99-5,people["Bethan"]),
    "crunchyroll": Service("crunchyroll",6.50,people["Brendan"]),
    "sky sports": Service("sky sports",5.00,people["Celia"]),
    "spotify": Service("spotify",16.99,people["Tom"])
}
        

# Add Megan services
service_and_fractions = {service:1 for service in services.values()}
register_services(people["Megan"],service_and_fractions)

# Add Brendan services
service_and_fractions = {
    services["netflix"]:1,
    services["sky sports"]:1,
    services["crunchyroll"]:1
}
register_services(people["Brendan"],service_and_fractions)

# Add Bethan Services
service_and_fractions = {
    services["netflix"]:1,
    services["sky sports"]:1,
    services["spotify"]:1
}
register_services(people["Bethan"],service_and_fractions)

# Add Tom services
service_and_fractions = {
    services["netflix"]:1,
    services["sky sports"]:1,
    services["crunchyroll"]:0.5,
    services["spotify"]: 1
}
register_services(people["Tom"],service_and_fractions)

# Add Celia services
service_and_fractions = {
}
register_services(people["Celia"],service_and_fractions)

# # Add Matt services
# service_and_fractions = {
#     services["netflix"]:2
# }
# register_services(people["Matt"],service_and_fractions)
people_overview(people)