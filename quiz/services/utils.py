from django.db.models import Model


def update_model(model: Model, pk: int, data: dict) -> Model:
    """
    Docstring для update_model

    :param model: Модель
    :param pk: id объекта
    :param data: Данные для обновления
    :return: Модель
    """
    model.objects.filter(id=pk).update(**data)
    return model.objects.get(id=pk)
