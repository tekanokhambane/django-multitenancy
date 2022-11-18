from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required  # type: ignore
def team_home(request):

    return render(request, 'multitenancy/admin/teamUser/index.html',
                  {
                      'nbar': 'admin',
                      'title': 'Dashboard!',

                  }
                  )
