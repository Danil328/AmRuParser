
class Car:
    def __init__(self, brand: str, model: str, generation: str, color: str, images: list):
        self.brand = brand
        self.model = model
        self.generation = generation
        self.color = color
        self.images = images

    def get_brand(self):
        return self.brand

    def model(self):
        return self.model

    def generation(self):
        return self.generation

    def get_object(self):
        return {"brand": self.brand, "model": self.model, "generation": self.generation, "color": self.color, "images": self.images}
