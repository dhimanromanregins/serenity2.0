from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Audiobook, Download
from .forms import AudiobookForm, AudiobookCreateForm

@login_required
def download_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)
    # Track download in the database
    Download.objects.create(user=request.user, audiobook=audiobook)
    # Redirect to the audio file URL
    return redirect(audiobook.audio_file.url)

@login_required
def edit_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to edit

    if request.method == 'POST':
        form = AudiobookForm(request.POST, request.FILES, instance=audiobook)
        if form.is_valid():
            form.save()
            return redirect('book_detail', pk=audiobook.book.id)
    else:
        form = AudiobookForm(instance=audiobook)
    return render(request, 'audiobooks/edit_audiobook.html', {'form': form, 'audiobook': audiobook})

@login_required
def delete_audiobook(request, audiobook_id):
    audiobook = get_object_or_404(Audiobook, id=audiobook_id)
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to delete

    if request.method == 'POST':
        audiobook.delete()
        return redirect('book_detail', pk=audiobook.book.id)

    return render(request, 'audiobooks/delete_audiobook.html', {'audiobook': audiobook})


@login_required
def create_audiobook(request):
    if not request.user.is_superuser:
        return redirect('book_list')  # Only allow admins to create new audiobooks

    if request.method == 'POST':
        form = AudiobookCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list or another page as needed
    else:
        form = AudiobookCreateForm()

    return render(request, 'audiobooks/create_audiobook.html', {'form': form})