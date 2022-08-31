from django.db import models
from .validators import validate_file_extension


class Store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['id']
        db_table = 'stores'
        managed = True


class IngredientCategory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_category'
        managed = True

# todo Meta tag images for searching when adding an icon to a new item
# todo Maybe add new Meta tags to icons for specific users when they use it?
class IngredientIcon(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    icon_image = models.FileField(upload_to="ingredient_icons_uploaded/", validators=[validate_file_extension])
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_icon'
        managed = True


class UnitsOfMeasurement(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    system = models.CharField(max_length=20)

    class Meta:
        ordering = ['id']
        db_table = 'units_of_measurement'
        managed = True


class IngredientItem(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    icon = models.ForeignKey(IngredientIcon, null=True, related_name='icon_data', on_delete=models.PROTECT)
    ingredient_id = models.IntegerField(null=True)
    barcode = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    category = models.ForeignKey(IngredientCategory, related_name='category_data', on_delete=models.PROTECT)
    default_quantity = models.FloatField(null=True)
    uom = models.ForeignKey(UnitsOfMeasurement, null=True, related_name='uom_data', on_delete=models.PROTECT)
    store = models.ForeignKey(Store, null=True, related_name='store_location', on_delete=models.PROTECT)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_item'
        managed = True


class IngredientCostLogging(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    cost = models.FloatField()
    currency = models.CharField(max_length=10)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_cost_logging'
        managed = True


class MealsMadeHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    meal_name = models.CharField(max_length=250)

    class Meta:
        ordering = ['id']
        db_table = 'meals_made_history'
        managed = True


class Student(models.Model):
    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    GRADUATE = 'GR'
    YEAR_IN_SCHOOL_CHOICES = [
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
        (GRADUATE, 'Graduate'),
    ]
    year_in_school = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default=FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {self.JUNIOR, self.SENIOR}


class IngredientInventory(models.Model):
    HUNDRED = 10
    NINETY = 9
    EIGHTY = 8
    SEVENTY = 7
    SIXTY = 6
    FIFTY = 5
    FORTY = 4
    THIRTY = 3
    TWENTY = 2
    TEN = 1
    AMOUNT_LEFT_CHOICES = [
        (HUNDRED, '%100'),
        (NINETY, '%90'),
        (EIGHTY, '%80'),
        (SEVENTY, '%70'),
        (SIXTY, '%60'),
        (FIFTY, '%50'),
        (FORTY, '%40'),
        (THIRTY, '%30'),
        (TWENTY, '%20'),
        (TEN, '%10'),
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    ingredient_id = models.ForeignKey(IngredientItem, related_name='ingredient_data', on_delete=models.PROTECT)
    amount_remaining = models.CharField(
        max_length=10,
        choices=AMOUNT_LEFT_CHOICES,
        default=HUNDRED
    )
    quantity = models.FloatField(null=True)
    cost = models.ForeignKey(IngredientCostLogging, related_name='ingredient_cost_data',
                             on_delete=models.PROTECT, null=True)
    store = models.ForeignKey(Store, null=True, related_name='store_data', on_delete=models.PROTECT)
    expiration_date = models.DateField()
    meals_used_in = models.ForeignKey(MealsMadeHistory, null=True, related_name='meals_used_in_data',
                                      on_delete=models.PROTECT)
    date_created = models.DateField(auto_now=True)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_inventory'
        managed = True


class AppFeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['id']
        db_table = 'app_feature_list'
        managed = True


class UserFeatureList(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=True)
    feature = models.ForeignKey(AppFeatureList, related_name='feature_data', on_delete=models.PROTECT)
    enabled = models.BooleanField(default=0)

    class Meta:
        ordering = ['id']
        db_table = 'user_feature_list'
        managed = True
