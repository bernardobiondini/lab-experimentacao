
import graphene
from flask import Flask
from flask_graphql import GraphQLView
import json

app = Flask(__name__)

# Carregar dados do arquivo JSON
with open('data.json', 'r') as f:
    users_data = json.load(f)

class User(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    city = graphene.String()

class Query(graphene.ObjectType):
    all_users = graphene.List(User)
    user = graphene.Field(User, id=graphene.Int())
    users_by_city = graphene.List(User, city=graphene.String())

    def resolve_all_users(root, info):
        return users_data

    def resolve_user(root, info, id):
        return next((user for user in users_data if user['id'] == id), None)

    def resolve_users_by_city(root, info, city):
        return [user for user in users_data if user['city'] == city]

schema = graphene.Schema(query=Query)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run(port=5001)


