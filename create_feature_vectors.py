from products.models import Product, FeatureVector
from PIL import Image
from torchvision import transforms
from torchvision.models import vgg16


def extract_features_from_image(image):
    preprocess = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    image = preprocess(image)
    image = image.unsqueeze(0)
    model = vgg16(pretrained=True).features
    model.eval()
    feature_vector = model(image).detach().numpy()
    return feature_vector


def create_feature_vectors():
    products = Product.objects.all()
    for product in products:
        if not hasattr(product, "feature_vector"):
            if product.product_image:
                image = Image.open(product.product_image.path).convert("RGB")
                feature_vector = extract_features_from_image(image)
                feature_vector_str = ",".join(map(str, feature_vector.flatten()))
                feature_vector_obj, created = FeatureVector.objects.get_or_create(
                    product=product
                )
                feature_vector_obj.feature_vector = feature_vector_str
                feature_vector_obj.save()


create_feature_vectors()
