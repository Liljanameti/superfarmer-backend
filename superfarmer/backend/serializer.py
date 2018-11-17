from .models import *
from rest_framework import serializers

from rest_framework.serializers import ModelSerializer
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin

class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = '__all__'


class UserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = '__all__'


class UsersSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('user_status', 'registration_status')


class UserProfileSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["address","city", "state", "country", "phone_primary" ]


# List of categories the web portal is supporting.
class ProductCategorySerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


# a product has an id, and it belongs to a category.
class ProductSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        #fields = ('product_name', 'product_default_image', 'product_category')
        fields = '__all__'

        expandable_fields = dict(
            product_category=dict(
                serializer=ProductCategorySerializer,
                id_source='product_category.pk'
            ),
        )


# each product has a measuring unit, a base measuring unit and a multiplier.
# measuring unit = multiplier * base measuring unit
class ProductMeasuringUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMeasuringUnit

        exclude = ('measuring_unit_id',)


# list of sellers, with the list of products they sell.
class SellerSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'

        expandable_fields = dict(
            seller=dict(
            serializer=UsersSerializer,
            id_source='seller.pk'),
        )


# list of buyers, with the list of products they buy.
class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'


# inventory item has a status: draft, active, suspended, unavailable.
class InventoryItemStatusSerializer(SerializerExtensionsMixin, serializers.ModelSerializer):
    class Meta:
        model = InventoryItemStatus
        fields = '__all__'


# a list of all advertised products.
class InventoryItemSerializer(SerializerExtensionsMixin, ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

        expandable_fields = dict(
            product=dict(
                serializer = ProductSerializer,
                id_source='product.pk'
            ),
            inventory_item_status=dict(
                serializer = InventoryItemStatusSerializer,
                id_source='inventory_item_status.pk'
            ),
            seller=dict(
                serializer = SellerSerializer,
                id_source='seller.pk'
            ),
            product_measuring_unit=dict(
                serializer=ProductMeasuringUnitSerializer,
                id_source='product_measuring_unit.pk'
            ),

        )

    def to_representation(self, instance):
        data = super(InventoryItemSerializer, self).to_representation(instance)
        print(data)
        return data


# each inventory item can have its own address. Default is sellers address.
class InventoryItemAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItemAddress
        fields = '__all__'



# transporters have an id, their transportation capacity, and what they're willing to transport.
class TransporterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporter
        fields = '__all__'


class RegistrationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationStatus
        fields = '__all__'
