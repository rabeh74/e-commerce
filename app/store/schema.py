from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
# from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from store.models import Products , Variation
from category.models import Category
import graphene

class ProductType(DjangoObjectType):
    class Meta:
        model=Products
        fields="__all__"
        filter_fields = ['product_name', 'category' , "id"]
        interfaces = (relay.Node, )
    @classmethod
    def get_queryset(cls, queryset, info):
        if info.context.user.is_anonymous:
            return queryset
        return queryset.all()[:2]
class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        fields="__all__"
        filter_fields = {
        'category_name':['exact', 'icontains', 'istartswith']
        , 'description':['exact', 'icontains',] ,}
        interfaces = (relay.Node, )
class CategoryConnection(relay.Connection):
    class Meta:
        node = CategoryType

class Query(ObjectType):
    product=relay.Node.Field(ProductType)
    all_products=DjangoFilterConnectionField(ProductType)
    category = relay.Node.Field(CategoryType)
    all_categories = relay.ConnectionField(CategoryConnection)
    # def resolve_questions(root, info, **kwargs):
    #     return Question.objects.all()

    def resolve_all_categories(root, info, **kwargs):
        return Category.objects.all()

schema = graphene.Schema(query=Query)