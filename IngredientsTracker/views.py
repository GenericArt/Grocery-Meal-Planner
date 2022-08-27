from django.shortcuts import render, redirect, Http404
from django.http import JsonResponse
import json
from .forms import BarcodeScanner, LoginForm
from .models import IngredientItem, IngredientInventory, IngredientCategory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


@login_required(login_url='/loginpage')
def index(request):
    context = {'form': BarcodeScanner()}
    return render(request, "IngredientsTracker/add_inventory.html", context)


def login_page(request):
    context = {'login_form': LoginForm}
    msg = request.session['msg']

    if msg:
        context['msg'] = msg
    else:
        context['msg'] = ''

    return render(request, 'IngredientsTracker/login_page.html', context)


def validate_user_login(request):
    if request.method == 'POST':
        user_email = request.POST.get('user_email', '')
        user_password = request.POST.get('user_password', '')

        user = authenticate(request, email=user_email, password=user_password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            request.session['msg'] = 'Oops! Wrong credentials!'
            return redirect('login_page')


def log_user_out(request):
    logout(request)
    return redirect('/loginpage')


@csrf_exempt
def check_scanned_barcode(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        print(post_data)

        scanned_barcode = str(post_data['barcode']).strip()
        item_info = {}

        # check if barcode exists
        check_barcode_exist = IngredientItem.objects.filter(barcode=scanned_barcode).values()
        if check_barcode_exist:
            exists = True

            # todo Take in only Barcode and check for a default Quantity. Then always provide a pop confirmation
            '''A better idea may be to not use a Django Form and then just use Javascript to check if the
            barcode exists and get the default quantity. Then ask user if this is right and then submit to db'''

        else:
            exists = False

        context = {
            'msg': 'This was posted: {}'.format(scanned_barcode),
            'exists': exists,
            'item_info': item_info,
            'categories': list(IngredientCategory.objects.all().values_list('name', flat=True))
        }

        return JsonResponse(context, status=200)


@csrf_exempt
def add_new_ingredient(request):
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))

        barcode_nbr = str(post_data['barcode']).strip()
        barcode_name = str(post_data['name']).strip()
        barcode_qty = int(str(post_data['quantity']).strip())
        barcode_desc = str(post_data['description']).strip()
        barcode_expire = str(post_data['expire_date']).strip()
        barcode_category = str(post_data['category']).strip()

        # Check if needed information exists before adding to the database
        if not barcode_nbr or not barcode_name or not barcode_expire or not barcode_category:
            return JsonResponse({'server_msg': 'Missing either the barcode number, expiry date, category or name'},
                                status=422)
        else:
            category_instance = IngredientCategory.objects.get(name=barcode_category)
            new_item_entry = IngredientItem.objects.create(
                barcode=barcode_nbr,
                name=barcode_name,
                default_quantity=barcode_qty,
                description=barcode_desc,
                category=category_instance,
            )
            new_item_entry.save()
            new_item_entry.ingredient_id = new_item_entry.id
            new_item_entry.save()

            new_inventory = IngredientInventory.objects.create(
                ingredient_id=new_item_entry,
                quantity=barcode_qty,
                expiration_date=barcode_expire,
            )
            new_inventory.save()

            return JsonResponse({'server_msg': 'Added new item successfully'}, status=200)

    return JsonResponse({'server_msg': 'This should have been a POST request but was not'}, status=401)


