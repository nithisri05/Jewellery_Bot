from transformers import CLIPModel, CLIPProcessor

class CLIPSingleton:
    _model = None
    _processor = None

    @classmethod
    def load(cls):
        if cls._model is None:
            cls._model = CLIPModel.from_pretrained(
                "openai/clip-vit-base-patch32"
            )
            cls._processor = CLIPProcessor.from_pretrained(
                "openai/clip-vit-base-patch32"
            )
            cls._model.eval()

        return cls._model, cls._processor
