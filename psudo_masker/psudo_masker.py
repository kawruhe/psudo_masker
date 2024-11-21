from faker import Faker
import hashlib


class SeededFaker(Faker):
    """
    A subclass of Faker that automatically seeds each method with a hash of the input value.
    """
    def __init__(self, locale=None):
        super().__init__(locale)

    def _seed_and_call(self, method_name, value, *args, **kwargs):
        """
        Middleware to seed the generator with a hash of the input value before calling the method.
        """
        if not isinstance(value, str):
            raise ValueError("The value to seed must be a string.")
        hash_val = int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)
        self.seed_instance(hash_val)  # Seed the Faker instance
        method = super().__getattr__(method_name)
        return method(*args, **kwargs)

    def __getattr__(self, name):
        """
        Dynamically intercept method calls, apply seeding, and forward the call.
        """
        return lambda value, *args, **kwargs: self._seed_and_call(name, value, *args, **kwargs)


class PsudoMasker:
    """
    Wrapper around SeededFaker to provide two default locales: Austrian and Greek.
    """
    def __init__(self, locale_austria="de_AT", locale_greece="en_US"):
        self.faker_austria = SeededFaker(locale_austria)
        self.faker_greece = SeededFaker(locale_greece)

    def setup(self, locale_austria=None, locale_greece=None):
        """
        Setup method to modify defaults for Austrian and Greek locales.
        """
        if locale_austria:
            self.faker_austria = SeededFaker(locale_austria)
        if locale_greece:
            self.faker_greece = SeededFaker(locale_greece)

    def get_faker(self, value):
        """
        Determine which Faker instance to use based on a hash of the input value.
        """
        hash_val = int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16)
        return self.faker_austria if hash_val % 2 == 0 else self.faker_greece

    def __getattr__(self, name):
        """
        Proxy method calls to the appropriate SeededFaker instance.
        """
        def wrapped_method(value, *args, **kwargs):
            faker_instance = self.get_faker(value)
            return getattr(faker_instance, name)(value, *args, **kwargs)
        return wrapped_method
