from .models import *
from superfarmer.settings import MEDIA_ROOT, MEDIA_URL
from collections import OrderedDict

def get_user(request):
    try:
        user = Users.objects.get(email_address=request.user.email)
        return user
    except:
        return None


def get_product(product_name=None):
    try:
        product = Product.objects.get(product_name=product_name)
        return product
    except:
        return None


def get_seller(request):
    try:
        seller = Seller.objects.get(pk=get_user(request).user_id)
        return seller
    except:
        print("seller id not found.")
        return None


def get_product_measuring_unit(measuring_unit=None):
    try:
        product_measuring_unit = MeasuringUnit.objects.get(measuring_unit=measuring_unit)
        return product_measuring_unit
    except:
        return None


def get_product_category(category=None):
    try:
        if type(category) == int:
            product_category = ProductCategory.objects.get(category_id=category)
        else:
            product_category = ProductCategory.objects.get(category_name=category)
        return product_category
    except:
        return None


def handle_uploaded_file(f):
    filepath = "{}/{}".format(MEDIA_ROOT, f.name.replace("/","_"))
    try:
        with open(filepath, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return "{}{}".format(MEDIA_URL, f)
    except:
        return "error"


def get_inventory_item_address(item_id=None):
    address = None
    try:
        address = InventoryItemAddress.objects.get(item_id=item_id)
    except:
        print("{} has no separate address assigned. Defaulting to seller's address.".format(item_id))

    return address


def sanitize_user_address(userProfile=None):
    sanitized = OrderedDict()
    sanitized["about_seller"] = userProfile.get("about_me")
    sanitized["address"] = userProfile.get("address")
    sanitized["city"] = userProfile.get("city")
    sanitized["state"] = userProfile.get("state")
    sanitized["country"] = userProfile.get("country")
    sanitized["postal_code"] = userProfile.get("postal_code")
    sanitized["latitude"] = userProfile.get("latitude")
    sanitized["longitude"] = userProfile.get("longitude")
    sanitized["latitude"] = userProfile.get("latitude")

    sanitized["phone_primary"] = "Unavailable"

    if userProfile.get("phone_verified") == True:
        sanitized["phone_primary"] = userProfile.get("phone_primary")

    sanitized["email_verified"] = "Unavailable"
    if userProfile.get("email_verified") == True:
        sanitized["email_verified"] = userProfile.get("email_verified")

    return sanitized


def sanitize_inventory_item(instance):
    sanitized = OrderedDict()
    sanitized["inventory_item_id"] = instance.get("inventory_item_id")
    sanitized["listing_title"] = instance.get("listing_title")
    sanitized["item_price"] = instance.get("item_price")
    sanitized["inventory_product_quantity"] = instance.get("inventory_product_quantity")
    sanitized["inventory_item_create_datetime"] = instance.get("inventory_item_create_datetime")
    sanitized["inventory_item_update_datetime"] = instance.get("inventory_item_update_datetime")
    sanitized["inventory_available_from_datetime"] = instance.get("inventory_available_from_datetime")
    sanitized["item_picture"] = instance.get("item_picture")
    sanitized["inventory_item_status"] = instance.get("inventory_item_status").get("status")
    sanitized["product_name"] = instance.get("product").get("product_name")
    sanitized["product_category"] = instance.get("product").get("product_category").get("category_name")
    sanitized["seller_name"] = instance.get("seller").get("seller").get("name")
    sanitized["measuring_unit"] = instance.get("product_measuring_unit").get("measuring_unit")

    address = OrderedDict()

    address.update(address=instance.get("address").get("address"))
    address.update(city=instance.get("address").get("city"))
    address.update(state=instance.get("address").get("state"))
    address.update(country=instance.get("address").get("country"))
    address.update(latitude=instance.get("address").get("latitude"))
    address.update(longitude=instance.get("address").get("longitude"))
    address.update(phone_primary=instance.get("address").get("phone_primary"))
    address.update(phone_verified=instance.get("address").get("phone_verified"))
    address.update(email_verified=instance.get("address").get("email_verified"))

    sanitized["address"] = address
    return sanitized