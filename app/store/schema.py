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

class ProductMutation(relay.ClientIDMutation):
    class Input:
        # The input arguments for this mutation
        Product_name = graphene.String(required=True)
        price=graphene.Int()
        id = graphene.ID()
    product=graphene.Field(ProductType)
    @classmethod
    def mutate_and_get_payload(cls , root , info , Product_name ,price,id):
        product=Products.objects.get(pk=id)
        product.product_name=Product_name
        product.price=5000
        product.save()

        return ProductMutation(product=product)

class ProductMutationCreate(relay.ClientIDMutation):
    class Input:
        product_name=graphene.String(required=True)
        price=graphene.Int(required=True)
        description=graphene.String()
        stock=graphene.Int()
        category_name=graphene.String(required=True)
    product=graphene.Field(ProductType)
    @classmethod
    def mutate_and_get_payload(cls , root , info ,**kwargs):
        cat_name=kwargs["category_name"]
        cat=None
        if Category.objects.filter(category_name=cat_name).exists():
            cat=Category.objects.get(category_name__exact=cat_name)
        else:
            cat=Category.objects.create(category_name=cat_name)
        kwargs.pop("category_name")
        print(cat)
        kwargs["category"]=cat
        product=Products.objects.create(**kwargs)

        return ProductMutationCreate(product=product)

class Mutation(graphene.ObjectType):
    update_product = ProductMutation.Field()
    create_product=ProductMutationCreate.Field()

class Query(ObjectType):
    product=relay.Node.Field(ProductType)
    all_products=DjangoFilterConnectionField(ProductType)
    category = relay.Node.Field(CategoryType)
    all_categories = relay.ConnectionField(CategoryConnection)


    def resolve_all_categories(root, info, **kwargs):
        return Category.objects.all()

schema = graphene.Schema(query=Query ,  mutation=Mutation)