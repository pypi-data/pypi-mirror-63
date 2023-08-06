import os
import copy
import yaml

from django.conf import settings

from drf_app_generators.compliers.model import ModelMeta


class AppOptions(object):

    models: [str] = [] # a list of model names
    api_doc: bool = False
    nested: bool = False
    force: bool = False

    def __init__(self, models=[], api_doc=False, nested=False, force=False):
        self.models = models
        self.api_doc = api_doc
        self.nested = nested
        self.force = force

    def to_json(self) -> dict:
        return self.__dict__


class AppConfig(object):
    """
    This contains all configuration to generate/update a Django app.
    """
    name: str = None
    name_capitalized: str = None
    options: AppOptions = AppOptions()
    models_meta: [ModelMeta] = []
    force: bool = False # force to override.

    # Summary required libraries and modules from model meta.
    factory_required_libs: [str] = []
    factory_required_modules: [str] = []

    def __init__(self, name=None, options=None, init=True):
        self.name = name
        self.name_capitalized = self.name.capitalize()
        self.options = options
        self.init = init # Init app the first time.
        self.models_meta = []

        if self.init:
            # Build model meta for the first time.
            self._build_models_meta()

    def set_models_meta(self, models_meta: [object]):
        """
        Set a list of models meta to app.
        """
        self.models_meta = models_meta

        for model_meta in models_meta:
            # Summary required libraries & modules for factory.
            self.factory_required_libs = set().union(
                self.factory_required_libs,
                model_meta.factory_required_libs
            )
            self.factory_required_modules = set().union(
                self.factory_required_modules,
                model_meta.factory_required_modules
            )

    def _build_models_meta(self):
        """
        Create models meta from options.
        """
        model_names = []

        if self.options and self.options.models:
            model_names = self.options.models

        for model_name in model_names:
            # Build the model meta.
            model_meta = ModelMeta(model=None)
            model_meta.build_from_name(name=model_name)
            self.models_meta.append(model_meta)

    def to_json(self) -> dict:
        """
        Dump this class to JSON.
        """
        obj = copy.copy(self.__dict__)
        obj['options'] = self.options.to_json()
        obj['models_meta'] = []

        for model_meta in self.models_meta:
            model_obj = model_meta.to_json()
            obj['models_meta'].append(model_obj)

        return obj

    def write_to_yaml(self):
        """
        Write the JSON data to yaml.
        """
        base_dir = settings.BASE_DIR
        data = self.to_json()

        if base_dir:
            base_dir = os.path.join(base_dir, self.name, 'meta.yaml')
        else:
            base_dir = os.path.join(os.getcwd(), self.name, 'meta.yaml')

        with open(f'{base_dir}', 'w') as fp:
            fp.write(yaml.dump(data, indent=4))
