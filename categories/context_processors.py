from .models import Category


def sidebar_data(request):
    # Your logic to fetch sidebar data, such as categories, tags, or any other dynamic content
    # You can fetch the data from your models or any other data source
    sidebar_data = {
        "categories": Category.objects.all(),  # Assuming you have a Category model
        # Add any other data you need for your sidebar
    }
    return {"sidebar_data": sidebar_data}
