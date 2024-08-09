from django.db import models


class User(models.Model):
    uname = models.CharField(max_length=50, unique=True, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.uname


class DocumentTypes(models.Model):
    DocumentType = models.CharField(max_length=255, unique=True)
    BuyerFirstName = models.CharField(max_length=255, null=True, blank=True)
    BuyerLastName = models.CharField(max_length=255, null=True, blank=True)
    BuyerAddress = models.CharField(max_length=255, null=True, blank=True)
    BuyerCity = models.CharField(max_length=255, null=True, blank=True)
    BuyerState = models.CharField(max_length=255, null=True, blank=True)
    BuyerZipcode = models.CharField(max_length=20, null=True, blank=True)
    SellerFirstName = models.CharField(max_length=255, null=True, blank=True)
    SellerLastName = models.CharField(max_length=255, null=True, blank=True)
    SellerAddress = models.CharField(max_length=255, null=True, blank=True)
    SellerCity = models.CharField(max_length=255, null=True, blank=True)
    SellerState = models.CharField(max_length=255, null=True, blank=True)
    SellerZipcode = models.CharField(max_length=20, null=True, blank=True)
    PropertyDetailsAddress = models.CharField(max_length=255, null=True, blank=True)
    PropertyDetailsLot = models.CharField(max_length=50, null=True, blank=True)
    PropertyDetailsBlock = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.DocumentType
