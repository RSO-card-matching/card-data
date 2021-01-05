import graphene
from starlette.graphql import GraphQLApp

from . import database


class Card(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    series = graphene.String()
    manufacturer = graphene.String()
    serial_num = graphene.String()

class Query(graphene.ObjectType):
    card = graphene.Field(Card, cid = graphene.Int())
    @staticmethod
    def resolve_card(root, info, cid):
        db = database.SessionLocal()
        card_model = database.get_card_by_id(db, cid)
        db.close()
        return card_model



def make_app():
    return GraphQLApp(schema=graphene.Schema(query=Query))