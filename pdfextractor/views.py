from django.shortcuts import render
from data_extraction.forms import FileUploadForm
from data_extraction import dataextractor


def homepage(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            input_file = request.FILES['input_file']
            print("Results : ", dataextractor.execute("Invoice", input_file))
    else:
        form = FileUploadForm()
    return render(request, 'index.html', {'form': form})