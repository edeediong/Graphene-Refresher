
import graphene
import json
import uuid
from datetime import datetime

class Post(graphene.ObjectType):
    title = graphene.String()
    content = graphene.String()


class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    created_at = graphene.DateTime(default_value=datetime.now())
    avatar_url = graphene.String()

    def resolve_avatar_url(self, info):
        return f'https://cloudinary.com/{self.username}/{self.id}'


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
            User(username="fred"),
            User(username="ann")
        ][:limit]

class CreateUser(graphene.Mutation):
    user = graphene.Field(User)


    class Arguments:
        username = graphene.String()


    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        title = graphene.String()
        content = graphene.String()


    def mutate(self, info, title, content):
        if info.context.get('is_anonymous'):
            raise Exception('Not Authenticated')
        post = Post(title=title, content=content)
        return CreatePost(post=post)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    create_post = CreatePost.Field()

# Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
    '''
    mutation($username: String) {
        createUser(username: $username) {
            user {
                id
                username
                createdAt
            }
        }
    }
    ''',
    variable_values={'username': "Eddie"}
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))

# Query
schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
    '''
    query getUserQuery ($limit: Int) {
        users(limit: $limit) {
            id
            username
            createdAt
        }
    }
    ''',
    variable_values={'limit': 4}
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))

# Post Mutation
schema = graphene.Schema(query=Query, mutation=Mutation)
result = schema.execute(
    '''
    mutation {
        createPost(
            title: "Study Time",
            content: "Django + React + GraphQL") {
            post {
                title
                content
            }
        }
    }
    ''',
    context = {'is_anonymous': True}
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))

# Query for Users
schema = graphene.Schema(query=Query)
result = schema.execute(
    '''
    {
        users {
            id
            username
            createdAt
            avatarUrl
        }
    }
    '''
)
dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent=2))