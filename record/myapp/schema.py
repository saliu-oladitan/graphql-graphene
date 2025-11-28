import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from myapp.models import UserModel


# Define your GraphQL Type
class UserType(DjangoObjectType):
    class Meta:
        model = UserModel
        fields = ("id", "first_name", "last_name")  # Explicit fields for safety



# Query Class — Read
class Query(graphene.ObjectType):
    # These field definitions are what tell Graphene which resolver function to call.
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_users(self, info):
        """Return all users."""
        return UserModel.objects.all()

    def resolve_user(self, info, id):
        """Return a single user by ID with error handling."""
        try:
            return UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            raise GraphQLError("User not found.")



# Create Mutation — Create
class CreateUser(graphene.Mutation):
    # Define what fields this mutation returns
    user = graphene.Field(UserType)

    # Define what arguments it accepts
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    def mutate(self, info, first_name, last_name):
        # Create the user
        user = UserModel.objects.create(
            first_name=first_name.strip(),
            last_name=last_name.strip()
        )
        # Return an instance of this mutation with the user field populated
        return CreateUser(user=user)



# Update Mutation — Update
class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    user = graphene.Field(UserType)

    def mutate(self, info, id, first_name=None, last_name=None):
        try:
            user = UserModel.objects.get(pk=id)
        except UserModel.DoesNotExist:
            raise GraphQLError("User not found.")

        if first_name:
            user.first_name = first_name.strip()
        if last_name:
            user.last_name = last_name.strip()

        user.save()
        return UpdateUser(user=user)



# Delete Mutation — Delete
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    response = graphene.String()

    def mutate(self, info, id):
        try:
            user = UserModel.objects.get(pk=id)
            user.delete()
            return DeleteUser(response="Successfully deleted user.")
        except UserModel.DoesNotExist:
            raise GraphQLError("User not found.")



# Combine all Mutations
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


# Schema definition
schema = graphene.Schema(query=Query, mutation=Mutation)




















### CREATE
# mutation {
#   createUser(firstName: "Alice2", lastName: "Smith2") {
#     user {
#       id
#       firstName
#       lastName
#     }
#   }
# }



### GET BY ID
# {
#   user(id: 3) {
#     id
#     firstName
#     lastName
#   }
# }



### GET ALL
# query{
#   users{
#     id
#     firstName
#     lastName
#   }
# }




### UPDATE
# mutation {
#   updateUser(id: 6, lastName: "JohnsonEdited") {
#     user {
#       id
#       firstName
#       lastName
#     }
#   }
# }




### DELETE
# mutation {
#   deleteUser(id: 10) {
#     ok
#   }
# }





















# import graphene
# from graphene_django import DjangoObjectType
# from myapp.models import UserModel

# class UserType(DjangoObjectType):
#     class Meta:
#         model = UserModel

# class Query(graphene.ObjectType):
#     users = graphene.List(UserType)

#     def resolve_users(self, info):
#         return UserModel.objects.all()
# schema = graphene.Schema(query=Query)





# class CreateUser(graphene.Mutation):
#     # The fields that the mutation will return after it runs successfully.
#     # So when a new user is created, the mutation returns that user’s details.
#     id = graphene.Int()
#     first_name = graphene.String()
#     last_name = graphene.String()

#     class Arguments:
#         first_name = graphene.String()
#         last_name = graphene.String()

#     def mutate(self, info, first_name, last_name):
#         user = UserModel(first_name=first_name, last_name=last_name)
#         user.save()

#         # After saving, the mutation returns a new CreateUser instance with the user’s info.
#         return CreateUser(
#             id=user.id,
#             first_name=user.first_name,
#             last_name=user.last_name,
#         )
# # This line registers the CreateUser mutation inside the main GraphQL schema.
# # It tells Graphene: “Our API supports a mutation named create_user.”
# class Mutation(graphene.ObjectType):
#     create_user = CreateUser.Field()





# # This creates the main GraphQL schema object that defines what your API can read (queries) and change (mutations).
# schema = graphene.Schema(
#     query=Query,
#     mutation=Mutation
# )