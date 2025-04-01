import os
from django.core.management.base import BaseCommand
from movie.models import Movie
from django.conf import settings

class Command(BaseCommand):
    help = "Update movie images in the database from the media folder"

    def handle(self, *args, **kwargs):
        # 📥 Ruta de la carpeta de imágenes
        image_folder = os.path.join(settings.MEDIA_ROOT, 'movie/images')

        if not os.path.exists(image_folder):
            self.stderr.write(self.style.ERROR(f"Image folder '{image_folder}' not found."))
            return

        updated_count = 0
        files_in_folder = set(os.listdir(image_folder))  # Archivos en la carpeta

        # 📖 Recorrer todas las películas en la base de datos
        for movie in Movie.objects.all():
            sanitized_title = movie.title.replace(":", "").strip()  # Eliminar los ":"
            expected_filename = f"m_{sanitized_title}.png"  # Formato esperado

            if expected_filename in files_in_folder:
                image_path = f"movie/images/{expected_filename}"  # Ruta relativa a MEDIA_ROOT
                movie.image = image_path  # Suponiendo que `image` es el campo de imagen en `Movie`
                movie.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
            else:
                self.stderr.write(self.style.WARNING(f"Image not found for: {movie.title} (Expected: {expected_filename})"))

        # ✅ Resumen final
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movie images."))
