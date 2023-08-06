""" Hosts the base class for Views. """
from django.http import HttpResponse
from django.views import View


class BaseTestView(View):
    """ Base View class for tests """

    # pylint: disable=no-self-use, unused-argument
    def get(self, request):
        """
        Test Get Method
        """
        return HttpResponse("ok!")


empty_view = BaseTestView.as_view()  # pylint: disable=invalid-name
