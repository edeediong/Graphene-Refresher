import graphene
import json
from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    created_at = graphene.DateTime()


class Query(graphene.ObjectType):
    users = graphene.List(User, limit=graphene.Int())
    hello = graphene.String()
    is_admin = graphene.Boolean()


    def resolve_hello(self, info):
        return "world"

    def resolve_is_admin(self, info):
        return True

    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="fred", created_at=datetime.now()),
            User(id="2", username="ann", created_at=datetime.now()),
        ][:limit]

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)

    class Arguments:
        username = graphene.String()


    def mutate(self, info, username):
        user = User(id="3", username=username, created_at=datetime.now())
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# Check Admin/ Naming conventions
# schema = graphene.Schema(query=Query)
# result = schema.execute(
#     '''
#     {
#         isAdmin
#     }
#     '''
# )
# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))

# Remove camel case
# schema = graphene.Schema(query=Query, auto_camelcase=False)
# result = schema.execute(
#     '''
#     {
#         isAdmin
#     }
#     '''
# )
# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))

# schema = graphene.Schema(query=Query, auto_camelcase=False)
# result = schema.execute(
#     '''
#     {
#         is_admin
#     }
#     '''
# )
# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))

# Query of users
# schema = graphene.Schema(query=Query)
# result = schema.execute(
#     '''
#     {
#         users {
#             id
#             username
#             createdAt
#         }
#     }
#     '''
# )
# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))

# Default with a Limit
# schema = graphene.Schema(query=Query)
# result = schema.execute(
#     '''
#     {
#         users(limit: 1) {
#             id
#             username
#             createdAt
#         }
#     }
#     '''
# )
# # print(result.data['hello'])
# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))

# Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
    '''
    mutation {
        createUser(username: "Edeediong") {
            user {
                id
                username
                createdAt
            }
        }
    }
    '''
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))
