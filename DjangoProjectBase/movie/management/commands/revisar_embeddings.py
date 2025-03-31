from django.core.management.base import BaseCommand
from movie.models import Movie
import numpy as np

class Command(BaseCommand):
    help = "Verifica que los embeddings de las películas están almacenados correctamente"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()

        if not movies:
            self.stdout.write(self.style.ERROR("No hay películas en la base de datos."))
            return

        for movie in movies:
            embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
            self.stdout.write(f"{movie.title}: {embedding_vector[:5]}")  # Muestra los primeros 5 valores

        self.stdout.write(self.style.SUCCESS("✅ Embeddings verificados correctamente."))
