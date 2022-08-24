from django.db import models


# Ended up not using this for now as it dampens the user experience.
class Store(models.Model):
    id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=200)
    description = models.TextField(null=True)

    class Meta:
        ordering = ['id']
        db_table = 'stores'
        managed = True


class IngredientItem(models.Model):
    id = models.AutoField(primary_key=True)
    barcode = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    default_quantity = models.FloatField(null=True)
    # store_id = models.ForeignKey(Store, related_name='store', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_item'
        managed = True


class IngredientInventory(models.Model):
    id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(IngredientItem, related_name='ingredient_item', on_delete=models.CASCADE)
    quantity = models.FloatField()
    expiration_date = models.DateField()

    class Meta:
        ordering = ['id']
        db_table = 'ingredient_inventory'
        managed = True



