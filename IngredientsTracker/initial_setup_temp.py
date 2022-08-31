from .models import IngredientCategory, IngredientIcon, AppFeatureList, UserFeatureList, UnitsOfMeasurement
from Users.models import UserAuth
from django.conf import settings
import os, tempfile
from django.contrib.auth import get_user_model


def run_all_intializations():
    create_default_item_categories()
    create_default_app_features_list()
    create_test_user()
    set_test_user_features()
    create_uom()
    print("Done")


def create_default_item_categories():
    category_list = ['Condiments', 'Meats', 'Dairy', 'Veggies', 'Fruit']

    for category in category_list:
        new_categories = IngredientCategory.objects.create(
            name=category
        )
        new_categories.save()


def create_default_app_features_list():
    feature_list = {'cost_tracking': 'This feature enables things like cost history trends and how many meals'
                                     'something went into',
                    'quantity_tracking': 'Enables the ability to track exact quantities of items bought. This can be '
                                         'down to how many carrots are in the bag you bought. This feature is aimed '
                                         'at the people who want to know every little detail about what they have.'}

    for feature, desc in feature_list.items():
        new_entry = AppFeatureList.objects.create(
            feature_name=feature,
            description=desc
        )
        new_entry.save()


def create_test_user():
    User = get_user_model()
    user = User.objects.create_user(email='manley@me.com', password='foobar')
    user.is_superuser = False
    user.is_staff = False
    user.first_name = 'Test'
    user.last_name = 'User'
    user.save()

    user.user_id = user.id
    user.save()


def set_test_user_features():
    test_user = UserAuth.objects.get(email='manley@me.com')
    all_features = AppFeatureList.objects.all()

    for feature in all_features:
        new_entry = UserFeatureList.objects.create(
            user_id=test_user.user_id,
            feature=feature,
            enabled=False
        )
        new_entry.save()


def create_uom():
    metric_liquid_list = ['Liter', 'Millilitres', 'Each']
    imperial_liquid_list = ['Gallon', 'Quart', 'Pint', 'Ounce', 'Cup', 'tbsp', 'tsp', 'Each']

    for imperial_unit in imperial_liquid_list:
        new_entry = UnitsOfMeasurement.objects.create(
            name=imperial_unit,
            system='I'
        )
        new_entry.save()

    for metric_unit in metric_liquid_list:
        new_entry = UnitsOfMeasurement.objects.create(
            name=metric_unit,
            system='M'
        )
        new_entry.save()


def create_default_item_icons():
    media_folder = settings.MEDIA_ROOT
    default_icons_folder = media_folder + 'ingredient_icons_uploaded/'
    list_of_image_names = os.listdir(default_icons_folder)

    temp_path = '/Users/manleygage/Documents/PersonalProjects/Django/Images/Icons/'
    default_image = temp_path + 'default_icon.svg'

    if default_image:
        # create a named temporary file within the project base , here in media

        # lf = tempfile.NamedTemporaryFile(dir=default_icons_folder)
        # f = open(default_image, 'rb')
        # lf.write(f.read())
        # doc object with file FileField.

        # doc.file.save(file_name, File(lf), save=True)
        # lf.close()

        new_entry = IngredientIcon.objects.create(
            name='default_image',
            icon_image='default_icon.svg'
        )
        new_entry.save()

        # lf.close()
