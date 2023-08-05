"""A SocialiteProvider Service Provider."""
from masonite.provider import ServiceProvider
from browserlog.commands.InstallCommand import InstallCommand


class BrowserlogProvider(ServiceProvider):
    """Provides Services To The Service Container."""

    wsgi = False

    def register(self):
        """Register objects into the Service Container."""
        self.app.bind('InstallCommand', InstallCommand())

