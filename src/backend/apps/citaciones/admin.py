from django.contrib import admin

# Citacion is a transient class (not a Django Model), so it cannot be registered in Admin.
# The Citacion class is used only for encapsulating citation data for email notifications.
# See models.py for the class definition.
