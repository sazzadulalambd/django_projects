from django.shortcuts import render,redirect
from .forms import AssetForm

# Create your views here.
def asset_index(request):
    return render(request, "asset/index.html")


def create_asset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('viewAsset')
            return redirect('asset_index')
    else:
        form = AssetForm()
    return render(request, 'asset/create_asset.html', {'form': form})

