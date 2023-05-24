from datetime import date

from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.contrib.admin.widgets import AutocompleteSelect
from django.contrib import admin

from dal import autocomplete


from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_unit',
            'product_vendor',
            'product_material',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_name',
            }),
            'product_unit': forms.TextInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_unit',
            }),
            'product_vendor': forms.TextInput(attrs={
                'class': 'form-control product-input',
                'id': 'product_vendor',
            }),
            'product_material': forms.Select(attrs={
                'class': 'form-control product-input',
                'id': 'product_material',
            }),
        }


class ProductDetailForm(forms.ModelForm):
    # products = Product.objects.all()
    # product_names = [p.product_name for p in products]

    # product = forms.ModelChoiceField(
    #     queryset=Product.objects.all(),
    #     widget=forms.Select(attrs={
    #         'class'      : 'form-control product-input',
    #         'id'         : 'product_name',
    #         'placeholder': 'Enter name of the product',
    #         }))

    # product = forms.CharField()

    # product = forms.ModelChoiceField(
    #     queryset=Product.objects.all(),
    #     to_field_name='product_name',
    #     widget=TypeaheadInput()
    # )

    # find_product = forms.CharField(
    #     widget=TypeaheadInput()
    #     )

    # product = forms.ModelChoiceField(
    #     queryset=Product.objects.all(),
    #     widget=autocomplete.ModelSelect2(
    #         url='product-autocomplete',
    #         attrs={
    #             'tags': 'true',
    #             'data-minimum-input-length': 2,
    #             'class': 'form-control',
    #             'id' : 'product',
    #         },
    #     ))

    class Meta:
        model = ProductDetail
        fields = [
            'product_qty',
            'product_price',
            'product_total',
            'product',

        ]
        widgets = {
            'product': autocomplete.ModelSelect2(
                url='product-autocomplete',
                attrs={
                    'tags': 'true',
                    'data-minimum-input-length': 2,
                    'allowClear': 'true',
                    'class': 'form-control',
                    'role': 'textbox',
                    'aria-readonly': 'true',
                    'data-placeholder': 'Autocomplete'
                }
            ),
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
            }),
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'phone',
            'alt_phone',
            'company',
            'email',
            'address',
            'city',
            'state',
            'zip',
            'customer_notes',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'Customer First Name',
            }),
            'last_name'     : forms.TextInput(attrs={
                'class'      : 'form-control',
                'id'         : 'last_name',
                'placeholder': 'Customer Last Name',
                }),
            # 'last_name': TypeaheadInput(
            #     options={
            #         'hint': True,
            #         'highlight': True,
            #         'minLength': 1,
            #     },
            #     datasets={
            #         'name': 'lastNames',
            #         'source': 'substringMatcher(lastNames)',
            #     },
            #     attrs={
            #         'class': 'form-control',
            #         'id': 'last_name',
            #         'placeholder': 'Customer Last Name',
            #     }
            # ),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phone',
            }),
            'alt_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'alt_phone',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'company',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'city',
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'state',
            }),
            'zip': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'zip',
            }),
            'customer_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'customer_notes',
                'placeholder': 'Enter customer notes',
                'rows': '3'
            }),
        }


class ContractorForm(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = [
            'contractor_first_name',
            'contractor_last_name',
            'contractor_phone',
            'contractor_company',
            'contractor_email',
            'contractor_address',
            'contractor_city',
            'contractor_state',
            'contractor_zip',
            'contractor_notes',
        ]
        widgets = {
            'contractor_first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_first_name',
                'placeholder': 'Contractor First Name',
            }),
            'contractor_last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_last_name',
                'placeholder': 'Contractor Last Name',
            }),

            'contractor_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_phone',
            }),
            # 'alt_phone': forms.TextInput(attrs={
            #     'class': 'form-control',
            #     'id': 'alt_phone',
            # }),
            'contractor_company': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_company',
            }),
            'contractor_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'contractor_email',
            }),
            'contractor_address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_address',
            }),
            'contractor_city': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_city',
            }),
            'contractor_state': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_state',
            }),
            'contractor_zip': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'contractor_zip',
            }),
            'contractor_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'contractor_notes',
                'placeholder': 'Enter contractor notes',
                'rows': '2'
            }),
        }


class InvoiceForm(forms.ModelForm):
    # initial_date = forms.DateField(
    #     widget=forms.widgets.DateInput(
    #         attrs={'placeholder': date.today(), 'type': 'text',
    #                'onfocus': "(this.type='date')",
    #                'id':'date_created'}
    #     )
    # )

    class Meta:
        model = Invoice
        fields = [
            'payment_type',
            'payment_status',
            'subtotal',
            'tax',
            'total',
            'deposit',
            'balance',
            'invoice_notes',
            'customer',
        ]
        exclude = ['customer']
        widgets = {
            'payment_type': forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_type',
                'placeholder': 'Check',
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'payment_status',
                'placeholder': 'PAID',
            }),
            'subtotal': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'subtotal',
                'placeholder': '0.00',
                'type': 'number',
                'readonly': 'True',
            }),
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'tax',
                'type': 'number',
                'readonly': 'True'
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'total',
                'placeholder': '0.00',
                'type': 'number',
                'readonly': 'True',
            }),
            'deposit': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'deposit',
                'default': '0.00',
                'type': 'number',
                'oninput': 'calculateBalance()',
                'step': 'any'
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'form-control',
                'id': 'balance',
                'placeholder': '0.00',
                'type': 'number',
                'readonly': 'True'
            }),
            'invoice_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'invoice_notes',
                'placeholder': 'Enter notes',
                'rows': '3'
            }),
        }


class InvoiceDetailForm(forms.ModelForm):
    class Meta:
        model = InvoiceDetail
        fields = [
            'product',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),
            # 'amount': forms.NumberInput(attrs={
            #     'class': 'form-control',
            #     'id': 'invoice_detail_amount',
            #     'placeholder': '0',
            #     'type': 'number',
            # }),
            # 'price': forms.NumberInput(attrs={
            #     'class': 'form-control',
            #     'id': 'invoice_detail_price',
            #     'type': 'number',
            # }),
        }


class excelUploadForm(forms.Form):
    file = forms.FileField()


# class BaseInvoiceFormset(BaseInlineFormSet):
#     def add_fields(self, form, index):
#         super(BaseInvoiceFormset, self).add_fields(form, index)
#
#         # save the formset in the 'nested' property
#         form.nested = ProductFormSet(
#             instance=form.instance,
#             data=form.data if form.is_bound else None,
#             files=form.files if form.is_bound else None,
#             prefix= f'product-{form.prefix}-{ProductFormSet.get_default_prefix()}',
#         )
#


ProductFormSet = formset_factory(ProductForm, extra=1)
ProductDetailFormSet = formset_factory(ProductDetailForm, extra=1)
# ProductDetailFormSet = inlineformset_factory(Product, ProductDetail, form=ProductDetailForm, extra=1)
