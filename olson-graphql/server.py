import datetime
import json
import os

import graphene
import uvicorn

from starlette.applications import Starlette
from starlette.config import Config
from starlette.graphql import GraphQLApp


class Database:
    def __init__(self, path):
        self.path = path
        self.films = self._load('films')
        self.people = self._load('people')
        self.planets = self._load('planets')
        self.species = self._load('species')

        self.starships = self._load('starships')
        self.vehicles = self._load('vehicles')

        transports = self._load('transport')

        for pk in self.starships:
            self.starships[pk].update(transports[pk])

        for pk in self.vehicles:
            self.vehicles[pk].update(transports[pk])

    def _load(self, name):
        with open(os.path.join(self.path, f'{name}.json')) as fp:
            data = json.load(fp)
        return {item['pk']: item['fields'] for item in data}


def resolve_datetime(name):
    def parse_datetime(self, info):
        value = getattr(self, name, None)
        if not value:
            return None
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
    return parse_datetime


def resolve_date(name):
    def parse_date(self, info):
        value = getattr(self, name, None)
        if not value:
            return None
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()
    return parse_date


class Planet(graphene.ObjectType):
    name = graphene.String(description='The name of this planet.')
    diameter = graphene.String(
        description='The diameter of this planet in kilometers.')
    rotation_period = graphene.String(
        description=(
            'The number of standard hours it takes for this planet to '
            'complete a single rotation on its axis.'))
    orbital_period = graphene.String(
        description=(
            'The number of standard days it takes for this planet to complete '
            'a single orbit of its local star.'))
    gravity = graphene.String(
        description=(
            'A number denoting the gravity of this planet. Where 1 is '
            'normal.'))
    population = graphene.String(
        description=(
            'The average population of sentient beings inhabiting this '
            'planet.'))
    climate = graphene.String(
        description='The climate of this planet. Comma-seperated if diverse.')
    terrain = graphene.String(
        description='The terrain of this planet. Comma-seperated if diverse.')
    surface_water = graphene.String(
        description=(
            'The percentage of the planet surface that is naturally occuring '
            'water or bodies of water.'))
    edited = graphene.DateTime(
        resolver=resolve_datetime('edited'),
        description='The datetime that this resource was created.')
    created = graphene.DateTime(
        resolver=resolve_datetime('created'),
        description='The datetime that this resource was edited.')


class Person(graphene.ObjectType):
    name = graphene.String(description='The name of this person.')
    height = graphene.String(
        description='The height of this person in meters.')
    mass = graphene.String(description='The mass of this person in kilograms.')
    hair_color = graphene.String(description='The hair color of this person.')
    skin_color = graphene.String(description='The skin color of this person.')
    eye_color = graphene.String(description='The eye color of this person.')
    birth_year = graphene.String(
        description=(
            'The birth year of this person. BBY (Before the Battle of Yavin) '
            'or ABY (After the Battle of Yavin).'))
    gender = graphene.String(
        description='The gender of this person (if known).')
    homeworld = graphene.Field(
        Planet, description='The planet that this person was born on.')
    edited = graphene.DateTime(
        resolver=resolve_datetime('edited'),
        description='The datetime that this resource was created.')
    created = graphene.DateTime(
        resolver=resolve_datetime('created'),
        description='The datetime that this resource was edited.')

    def resolve_homeworld(self, info):
        database = info.context['request'].app.database
        return Planet(**database.planets[self.homeworld])


class Species(graphene.ObjectType):
    name = graphene.String(description='The name of this species.')
    classification = graphene.String(
        description='The classification of this species.')
    designation = graphene.String(
        description='The designation of this species.')
    average_height = graphene.String(
        description='The average height of this person in centimeters.')
    average_lifespan = graphene.String(
        description='The average lifespan of this species in years.')
    hair_colors = graphene.String(
        description=(
            'A comma-seperated string of common hair colors for this species, '
            'none if this species does not typically have hair.'))
    skin_colors = graphene.String(
        description=(
            'A comma-seperated string of common skin colors for this species, '
            'none if this species does not typically have skin.'))
    eye_colors = graphene.String(
        description=(
            'A comma-seperated string of common eye colors for this species, '
            'none if this species does not typically have eyes.'))
    homeworld = graphene.Field(
        Planet, description='The planet that this species originates from.')
    language = graphene.String(
        description='The language commonly spoken by this species.')
    people = graphene.List(
        Person, description=(
            'An list of People that are a part of this species.'))
    edited = graphene.DateTime(
        resolver=resolve_datetime('edited'),
        description='The datetime that this resource was created.')
    created = graphene.DateTime(
        resolver=resolve_datetime('created'),
        description='The datetime that this resource was edited.')

    def resolve_homeworld(self, info):
        database = info.context['request'].app.database
        return Planet(**database.planets[self.homeworld])

    def resolve_people(self, info):
        people = info.context['request'].app.database.people
        return [Person(**people[pk]) for pk in self.people]


class Transport(graphene.ObjectType):
    name = graphene.String(description='The name of this transport.')
    model = graphene.String(
        description='The model or official name of this transport.')
    manufacturer = graphene.String(
        description=(
            'The manufacturer of this transport. Comma seperated if more than '
            'one.'))
    cost_in_credits = graphene.String(
        description='The cost of this transport new, in galactic credits.')
    length = graphene.String(
        description='The length of this transport in meters.')
    crew = graphene.String(
        description=(
            'The number of personnel needed to run or pilot this transport.'))
    passengers = graphene.String(
        description='The number of non-essential people this can transport.')
    max_atmosphering_speed = graphene.String(
        description=(
            'The maximum speed of this transport in atmosphere. n/a if this '
            'transport is incapable of atmosphering flight.'))
    cargo_capacity = graphene.String(
        description='The maximum number of kilograms that this can transport.')
    consumables = graphene.String(
        description=(
            'The maximum length of time that this transport can provide '
            'consumables for its entire crew without having to resupply.'))
    pilots = graphene.List(
        Person, description=(
            'An array of People that this transport has been piloted by.'))
    edited = graphene.DateTime(
        resolver=resolve_datetime('edited'),
        description='The datetime that this resource was created.')
    created = graphene.DateTime(
        resolver=resolve_datetime('created'),
        description='The datetime that this resource was edited.')

    def resolve_pilots(self, info):
        people = info.context['request'].app.database.people
        return [Person(**people[pk]) for pk in self.pilots]


class Starship(Transport):
    starship_class = graphene.String(description='The class of this starship.')
    hyperdrive_rating = graphene.String(
        description='The class of this starships hyperdrive.')
    MGLT = graphene.String(
        description=(
            'The Maximum number of Megalights this starship can travel in a '
            'standard hour. A Megalight is a standard unit of distance and '
            'has never been defined before within the Star Wars universe. '
            'This figure is only really useful for measuring the difference '
            'in speed of starships. We can assume it is similar to AU, the '
            'distance between our Sun (Sol) and Earth.'))


class Vehicle(Transport):
    vehicle_class = graphene.String(
        description='The class of this vehicle, such as Wheeled.')


class Film(graphene.ObjectType):
    title = graphene.String(description='The title of this film.')
    episode_id = graphene.Int(description='The episode number of this film.')
    opening_crawl = graphene.String(
        description='The opening crawl text at the beginning of this film.')
    director = graphene.String(description='The director of this film.')
    producer = graphene.String(description='The producer(s) of this film.')
    release_date = graphene.Date(
        resolver=resolve_date('release_date'),
        description='The release date at original creator country.')
    characters = graphene.List(
        Person, description='The people resources featured within this film.')
    planets = graphene.List(
        Planet, description='The planet resources featured within this film.')
    starships = graphene.List(
        Starship, description=(
            'The starship resources featured within this film.'))
    vehicles = graphene.List(
        Vehicle, description=(
            'The vehicle resources featured within this film.'))
    species = graphene.List(
        Species, description=(
            'The species resources featured within this film.'))
    edited = graphene.DateTime(
        resolver=resolve_datetime('edited'),
        description='The datetime that this resource was created.')
    created = graphene.DateTime(
        resolver=resolve_datetime('created'),
        description='The datetime that this resource was edited.')

    def resolve_characters(self, info):
        people = info.context['request'].app.database.people
        return [Person(**people[pk]) for pk in self.characters]

    def resolve_planets(self, info):
        planets = info.context['request'].app.database.planets
        return [Planet(**planets[pk]) for pk in self.planets]

    def resolve_starships(self, info):
        starships = info.context['request'].app.database.starships
        return [Starship(**starships[pk]) for pk in self.starships]

    def resolve_vehicles(self, info):
        vehicles = info.context['request'].app.database.vehicles
        return [Vehicle(**vehicles[pk]) for pk in self.vehicles]

    def resolve_species(self, info):
        species = info.context['request'].app.database.species
        return [Species(**species[pk]) for pk in self.species]


class Query(graphene.ObjectType):
    film = graphene.Field(Film, episode_id=graphene.Int(required=True))
    planet = graphene.Field(Planet, name=graphene.String(required=True))
    person = graphene.Field(Person, name=graphene.String(required=True))
    species = graphene.Field(Species, name=graphene.String(required=True))
    starship = graphene.Field(Starship, name=graphene.String(required=True))
    vehicle = graphene.Field(Vehicle, name=graphene.String(required=True))

    def resolve_film(self, info, episode_id):
        request = info.context['request']
        for film in request.app.database.films.values():
            if film['episode_id'] == episode_id:
                return Film(**film)
        return None

    def resolve_planet(self, info, name):
        request = info.context['request']
        for planet in request.app.database.planets.values():
            if planet['name'] == name:
                return Planet(**planet)
        return None

    def resolve_person(self, info, name):
        request = info.context['request']
        for person in request.app.database.people.values():
            if person['name'] == name:
                return Person(**person)
        return None

    def resolve_species(self, info, name):
        request = info.context['request']
        for species in request.app.database.species.values():
            if species['name'] == name:
                return Species(**species)
        return None

    def resolve_starship(self, info, name):
        request = info.context['request']
        for starship in request.app.database.starships.values():
            if starship['name'] == name:
                return Starship(**starship)
        return None

    def resolve_vehicle(self, info, name):
        request = info.context['request']
        for vehicle in request.app.database.vehicles.values():
            if vehicle['name'] == name:
                return Vehicle(**vehicle)
        return None


config = Config()
DEBUG = config('DEBUG', cast=bool, default=False)


app = Starlette()
app.debug = DEBUG

app.database = Database(os.path.join(os.path.dirname(__file__), 'data'))
app.add_route('/', GraphQLApp(schema=graphene.Schema(query=Query)))


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000, log_level='info')
