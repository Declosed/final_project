from django.apps import AppConfig

class PortalConfig(AppConfig):
    # Set the default database primary key type for all models in this app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # The complete module path name of the Django application
    name = 'portal'
    
    # Custom display name for the Django administration control panel
    verbose_name = 'LASOP School Portal Management Core'

    def ready(self):
        """
        Executes once when Django boots up. 
        Import your signals inside this hook to prevent circular import errors.
        """
        import portal.signals  
