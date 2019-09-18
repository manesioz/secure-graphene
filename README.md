# secure-graphene

An extension of [Graphene](https://github.com/graphql-python/graphene) which allows you to secure your GraphQL API against malicious queries. 

Features included: 
- Limit Query Depth


Other features (limiting query complexity, etc) are under development. 


### Prerequisites 

- [graphql-core](https://github.com/graphql-python/graphql-core) 


### Installation 

- Will be available on pip soon 


### Detailed Example 

Given the following schema: 

    import graphene
    
    class Episode(graphene.Enum):
        NEWHOPE = 4
        EMPIRE = 5
        JEDI = 6
    
    
    class Character(graphene.Interface):
        id = graphene.ID()
        name = graphene.String()
        friends = graphene.List(lambda: Character)
        appears_in = graphene.List(Episode)
    
        def resolve_friends(self, info):
            # The character friends is a list of strings
            return [get_character(f) for f in self.friends]
    
    
    class Human(graphene.ObjectType):
        class Meta:
            interfaces = (Character,)
    
        home_planet = graphene.String()
    
    
    class Droid(graphene.ObjectType):
        class Meta:
            interfaces = (Character,)
    
        primary_function = graphene.String()
    
    
    class Query(graphene.ObjectType):
        hero = graphene.Field(Character, episode=Episode())
        human = graphene.Field(Human, id=graphene.String())
        droid = graphene.Field(Droid, id=graphene.String())
    
        def resolve_hero(self, info, episode=None):
            return get_hero(episode)
    
        def resolve_human(self, info, id):
            return get_human(id)
    
        def resolve_droid(self, info, id):
            return get_droid(id)
            
And the resolver functions and data: 

    human_data = {}
    droid_data = {}
    
    luke = Human(
        id="1000",
        name="Luke Skywalker",
        friends=["1002", "1003", "2000", "2001"],
        appears_in=[4, 5, 6],
        home_planet="Tatooine",
    )
    
    vader = Human(
        id="1001",
        name="Darth Vader",
        friends=["1004"],
        appears_in=[4, 5, 6],
        home_planet="Tatooine",
    )
    
    han = Human(
        id="1002",
        name="Han Solo",
        friends=["1000", "1003", "2001"],
        appears_in=[4, 5, 6],
        home_planet=None,
    )
    
    leia = Human(
        id="1003",
        name="Leia Organa",
        friends=["1000", "1002", "2000", "2001"],
        appears_in=[4, 5, 6],
        home_planet="Alderaan",
    )
    
    tarkin = Human(
        id="1004",
        name="Wilhuff Tarkin",
        friends=["1001"],
        appears_in=[4],
        home_planet=None,
    )
    
    human_data = {
        "1000": luke,
        "1001": vader,
        "1002": han,
        "1003": leia,
        "1004": tarkin,
    }
    
    c3po = Droid(
        id="2000",
        name="C-3PO",
        friends=["1000", "1002", "1003", "2001"],
        appears_in=[4, 5, 6],
        primary_function="Protocol",
    )
    
    r2d2 = Droid(
        id="2001",
        name="R2-D2",
        friends=["1000", "1002", "1003"],
        appears_in=[4, 5, 6],
        primary_function="Astromech",
    )
    
    droid_data = {"2000": c3po, "2001": r2d2}
    
    
    def get_character(id):
        return human_data.get(id) or droid_data.get(id)
    
    
    def get_friends(character):
        return map(get_character, character.friends)
    
    
    def get_hero(episode):
        if episode == 5:
            return human_data["1000"]
        return droid_data["2001"]
    
    
    def get_human(id):
        return human_data.get(id)
    
    
    def get_droid(id):
        return droid_data.get(id)

Let's run this query

    query_string = """
                query HeroNameAndFriendsQuery {
                  hero {
                    id
                    name
                    friends {
                      name
                    }
                  }
                }
            """

By doing the following: 

    backend = DepthAnalysisBackend(max_depth=2) 
    schema = graphene.Schema(query=Query)
    result = schema.execute(query_string, backend=backend)
    result.errors

Which returns the following: 

    [Exception('Query is too deep - your depth is 3 and the max depth is 2')]
    
    
