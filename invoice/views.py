import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from dal import autocomplete

from utils.filehandler import handle_file_upload

from .forms import *
from .models import *



class ProductAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        # if not self.request.user.is_authenticated:
        #     return Product.objects.none()

        qs = Product.objects.all()

        if self.q:
            qs = qs.filter(product_name__istartswith=self.q)

        return qs


def getTotalIncome():
    allInvoice = Invoice.objects.all()
    totalIncome = 0
    for curr in allInvoice:
        totalIncome += curr.total
    return totalIncome


def base(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()
    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
    }

    return render(request, "invoice/base/base.html", context)


def download_all(request):
    # Download all invoice to excel file
    # Download all product to excel file
    # Download all customer to excel file

    allInvoiceDetails = InvoiceDetail.objects.all()
    invoiceAndProduct = {
        "invoice_id": [],
        "invoice_date": [],
        "invoice_customer": [],
        "invoice_contact": [],
        "invoice_email": [],
        "invoice_comments": [],
        "product_name": [],
        "product_price": [],
        "product_unit": [],
        "product_amount": [],
        "invoice_total": [],

    }
    for curr in allInvoiceDetails:
        invoice = Invoice.objects.get(id=curr.invoice_id)
        product = Product.objects.get(id=curr.product_id)
        invoiceAndProduct["invoice_id"].append(invoice.id)
        invoiceAndProduct["invoice_date"].append(invoice.date)
        invoiceAndProduct["invoice_customer"].append(invoice.customer)
        invoiceAndProduct["invoice_contact"].append(invoice.contact)
        invoiceAndProduct["invoice_email"].append(invoice.email)
        invoiceAndProduct["invoice_comments"].append(invoice.comments)
        invoiceAndProduct["product_name"].append(product.product_name)
        invoiceAndProduct["product_price"].append(product.product_price)
        invoiceAndProduct["product_unit"].append(product.product_unit)
        invoiceAndProduct["product_amount"].append(curr.amount)
        invoiceAndProduct["invoice_total"].append(invoice.total)

    df = pd.DataFrame(invoiceAndProduct)
    df.to_excel("static/excel/allInvoices.xlsx", index=False)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="allInvoices.xlsx"'
    with open("../static/excel/allInvoices.xlsx", "rb") as f:
        response.write(f.read())
    return response


def delete_all_invoice(request):
    # Delete all invoice
    Invoice.objects.all().delete()
    return redirect("view_invoice")


def upload_product_from_excel(request):
    # Upload excel file to static folder "excel"
    # add all product to database
    # save product to database
    # redirect to view_product
    excelForm = excelUploadForm(request.POST or None, request.FILES or None)
    print("Reached HERE!")
    if request.method == "POST":
        print("Reached HERE2222!")

        handle_file_upload(request.FILES["excel_file"])
        excel_file = "../static/excel/masterfile.xlsx"
        df = pd.read_excel(excel_file)
        Product.objects.all().delete()
        for index, row in df.iterrows():
            product = Product(
                product_name=row["product_name"],
                product_price=row["product_price"],
                product_unit=row["product_unit"],
            )
            print(product)
            product.save()
        return redirect("view_product")
    return render(request, "invoice/upload_products.html", {"excelForm": excelForm})

    # Product view


def create_product(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()
    products = Product.objects.all()
    products = [p.product_name for p in products]

    product_formset = ProductDetailFormSet()
    product_detail_form = ProductDetailForm()

    if request.method == "POST":
        product_formset = ProductDetailFormSet(request.POST)
        if product_formset.is_valid():
            print('product_formset is valid')
            for form in product_formset:
                form.save()
            return redirect("create_product")
        else:
            print(product_formset.errors)

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product_formset": product_formset,
    }

    return render(request, "invoice/create_product.html", context)


def view_product(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = Product.objects.filter(product_is_delete=False)
    print(product)
    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": product,
    }

    return render(request, "invoice/view_product.html", context)


# def find_customer(request):


# Customer view
def create_customer(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = CustomerForm(
        initial={
            'state': 'CA'
        }
    )

    if request.method == "POST":
        customer = CustomerForm(request.POST)
        if customer.is_valid():
            customer.save()
            return redirect("create_customer")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": customer,
    }

    return render(request, "invoice/create_customer.html", context)


def view_customer(request):
    """View all existing customers with the option to edit or delete"""
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = Customer.objects.all()

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": customer,
    }

    return render(request, "invoice/view_customer.html", context)


def update_invoice(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    invoice = Invoice.objects.get(id=pk)
    customer = Customer.objects.get(id=invoice.customer_id)
    products = Product.objects.filter(invoice_id=pk)

    invoice_form = InvoiceForm(instance=invoice)
    customer_form = CustomerForm(instance=customer)

    ProductFormSet = modelformset_factory(
        Product, ProductForm,
        fields=[
            'id',
            'product_name',
            'product_unit',
            'product_qty',
            'product_price',
            'product_total',
            'product_vendor',
            'product_material',

        ],
        widgets={
            'id': forms.NumberInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_id',
                'type': 'number',
                'hidden': 'True',
            }),
            'product_name': forms.TextInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_name',
                'placeholder': 'Enter name of the product',
            }),
            'product_unit': forms.TextInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_unit',
            }),
            'product_qty': forms.NumberInput(attrs={
                'class': 'form-control product-input qty-product',
                'id': 'product_qty',
                'type': 'number',
                'oninput': 'calculateProductTotal()'
            }),
            'product_price': forms.NumberInput(attrs={
                'class': 'form-control product-input price-product',
                'id': 'product_price',
                'type': 'number',
                'oninput': 'calculateProductTotal()'
            }),
            'product_total': forms.NumberInput(attrs={
                'class': 'form-control product-input total-product',
                'id': 'product_total',
                'type': 'number',
                'readonly': 'True',
                # 'onchange': 'calculateSubTotal()'
            }),
            'product_vendor': forms.TextInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_vendor',
            }),
            'product_material': forms.Select(attrs={
                'class': 'form-control product-input',
                'id': 'product_material',
            }),
        },
        extra=0)

    product_formset = ProductFormSet(
        queryset=Product.objects.filter(invoice_id=pk),
        prefix='product_formset',
    )

    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        customer_form = CustomerForm(request.POST)
        product_formset = ProductFormSet(request.POST, prefix='product_formset')

        if customer_form.is_valid():
            customer.first_name = customer_form.cleaned_data.get("first_name"),
            customer.last_name = customer_form.cleaned_data.get("last_name"),
            customer.phone = customer_form.cleaned_data.get("phone"),
            customer.alt_phone = customer_form.cleaned_data.get("alt_phone"),
            customer.company = customer_form.cleaned_data.get("company"),
            customer.email = customer_form.cleaned_data.get("email"),
            customer.address = customer_form.cleaned_data.get("address"),
            customer.city = customer_form.cleaned_data.get("city"),
            customer.state = customer_form.cleaned_data.get("state"),
            customer.zip = customer_form.cleaned_data.get("zip"),
            print('customer form is valid')

        if invoice_form.is_valid():
            invoice.payment_type = invoice_form.cleaned_data.get("payment_type"),
            invoice.payment_status = invoice_form.cleaned_data.get("payment_status"),
            invoice.subtotal = invoice_form.cleaned_data.get("subtotal"),
            invoice.tax = invoice_form.cleaned_data.get("tax"),
            invoice.total = invoice_form.cleaned_data.get("total"),
            invoice.deposit = invoice_form.cleaned_data.get("deposit"),
            invoice.balance = invoice_form.cleaned_data.get("balance"),
            invoice.invoice_notes = invoice_form.cleaned_data.get("invoice_notes"),
            print('invoice form is valid')

        if product_formset.is_valid():
            for i, product in enumerate(product_formset):
                products[i].product_name = product.cleaned_data.get("product_name"),
                products[i].product_unit = product.cleaned_data.get("product_unit"),
                products[i].product_qty = product.cleaned_data.get("product_qty"),
                products[i].product_price = product.cleaned_data.get("product_price"),
                products[i].product_total = product.cleaned_data.get("product_total"),
                products[i].product_vendor = product.cleaned_data.get("product_vendor"),
                products[i].product_material = product.cleaned_data.get("product_material"),
                print('product is valid')
        else:
            print('product formset is NOT valid')
            for form in product_formset:
                if form.is_valid():
                    pass
                else:
                    print(form.errors)

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice_form": invoice_form,
        "product_formset": product_formset,
        "customer_form": customer_form,
        "dummy_invoice_num": invoice.id,
    }

    return render(request, "invoice/create_invoice.html", context)


def find_invoice_number():
    invoices = Invoice.objects.all()
    ids = [i.id for i in invoices]
    latest = max(ids)
    return latest + 1


# Invoice view
def create_invoice(request):
    date = datetime.date.today()
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    products = Product.objects.all()
    products = [p.product_name for p in products]

    try:
        invoice_num = find_invoice_number()
    except:
        invoice_num = 1

    invoice_form = InvoiceForm(initial={'invoice_date_created': datetime.datetime.now()})
    product_detail_formset = ProductDetailFormSet(prefix='product_detail_formset')
    product_formset = ProductFormSet(prefix='product_formset')
    customer_form = CustomerForm(initial={'state': 'CA'})

    contractor_form = ContractorForm(initial={'state': 'CA'})

    if request.method == "POST":
        invoice_form = InvoiceForm(request.POST)
        customer_form = CustomerForm(request.POST)
        product_formset = ProductFormSet(request.POST, prefix='product_formset')
        product_detail_formset = ProductDetailFormSet(request.POST, prefix='product_detail_formset')

        if customer_form.is_valid():
            customer = Customer.objects.create(
                first_name=customer_form.cleaned_data.get("first_name"),
                last_name=customer_form.cleaned_data.get("last_name"),
                phone=customer_form.cleaned_data.get("phone"),
                alt_phone=customer_form.cleaned_data.get("alt_phone"),
                company=customer_form.cleaned_data.get("company"),
                email=customer_form.cleaned_data.get("email"),
                address=customer_form.cleaned_data.get("address"),
                city=customer_form.cleaned_data.get("city"),
                state=customer_form.cleaned_data.get("state"),
                zip=customer_form.cleaned_data.get("zip"),
            )
        else:
            print('customer form is NOT valid')
            print(customer_form.errors)

        if invoice_form.is_valid():
            invoice = Invoice.objects.create(
                payment_type=invoice_form.cleaned_data.get("payment_type"),
                payment_status=invoice_form.cleaned_data.get("payment_status"),
                subtotal=invoice_form.cleaned_data.get("subtotal"),
                tax=invoice_form.cleaned_data.get("tax"),
                total=invoice_form.cleaned_data.get("total"),
                deposit=invoice_form.cleaned_data.get("deposit"),
                balance=invoice_form.cleaned_data.get("balance"),
                invoice_notes=invoice_form.cleaned_data.get("invoice_notes"),
                customer_id=customer.id,
            )
            invoice_num = invoice.id

        else:
            print('invoice form is NOT valid')
            print(invoice_form.errors)

        if product_detail_formset.is_valid():
            for product in product_detail_formset:
                product = Product.objects.create(
                    product_name=product.cleaned_data.get("product_name"),
                    product_unit=product.cleaned_data.get("product_unit"),
                    product_qty=product.cleaned_data.get("product_qty"),
                    product_price=product.cleaned_data.get("product_price"),
                    product_total=product.cleaned_data.get("product_total"),
                    product_vendor=product.cleaned_data.get("product_vendor"),
                    product_material=product.cleaned_data.get("product_material"),
                    invoice_id=invoice.id
                )
        else:
            print('product formset is NOT valid')
            for form in product_detail_formset:
                if form.is_valid():
                    pass
                else:
                    print(form.errors)

        return redirect(f'/update_invoice/{invoice.id}')

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice_form": invoice_form,
        "product_detail_formset": product_detail_formset,
        "product_formset": product_formset,
        "customer_form": customer_form,
        "contractor_form": contractor_form,

        "date": date,
        "dummy_invoice_num": invoice_num,
        # "products" : products,
    }

    return render(request, "invoice/create_invoice.html", context)


def view_invoice(request):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    invoice = Invoice.objects.all()

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice": invoice,
    }

    return render(request, "invoice/view_invoice.html", context)


# Detail view of invoices
# def view_invoice_detail(request, pk):
#     total_product = Product.objects.count()
#     total_customer = Customer.objects.count()
#     total_invoice = Invoice.objects.count()
#     total_income = getTotalIncome()
#
#     invoice = Invoice.objects.get(id=pk)
#     customer = Customer.objects.get(id=invoice.customer_id)
#     products = Product.objects.filter(invoice_id=pk)
#
#     context = {
#         "total_product": total_product,
#         "total_customer": total_customer,
#         "total_invoice": total_invoice,
#         "total_income": total_income,
#         'invoice': invoice,
#     }
#
#     return render(request, "invoice/view_invoice_detail.html", context)

def view_invoice_detail(request, pk):
    """
    View invoice products
    """
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    products = Product.objects.filter(invoice_id=pk)

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        'products': products,
    }

    return render(request, "invoice/view_invoice_detail.html", context)


# Delete invoice
def delete_invoice(request, pk):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    if request.method == "POST":
        invoice_detail.delete()
        invoice.delete()
        return redirect("view_invoice")

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/delete_invoice.html", context)


# Edit customer
def edit_customer(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        customer = CustomerForm(request.POST, instance=customer)
        if customer.is_valid():
            customer.save()
            return redirect("view_customer")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": form,
    }

    return render(request, "invoice/create_customer.html", context)


# Delete customer
def delete_customer(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    customer = Customer.objects.get(id=pk)

    if request.method == "POST":
        customer.delete()
        return redirect("view_customer")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "customer": customer,
    }

    return render(request, "invoice/delete_customer.html", context)


# Edit product
def edit_product(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)

    if request.method == "POST":
        customer = CustomerForm(request.POST, instance=product)

        product.save()
        return redirect("view_product")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": form,
    }

    return render(request, "invoice/templates/trash/create_product3.html", context)


# Delete product
def delete_product(request, pk):
    total_product = Product.objects.count()
    total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    total_income = getTotalIncome()

    product = Product.objects.get(id=pk)

    if request.method == "POST":
        product.product_is_delete = True
        product.save()
        return redirect("view_product")

    context = {
        "total_product": total_product,
        "total_customer": total_customer,
        "total_invoice": total_invoice,
        "total_income": total_income,
        "product": product,
    }

    return render(request, "invoice/delete_product.html", context)
