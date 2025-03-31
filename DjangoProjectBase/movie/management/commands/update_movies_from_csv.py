import os
import csv
from django.core.management.base import BaseCommand
from movie.models import Movie  # Asegúrate de importar el modelo correcto

class Command(BaseCommand):
    help = "Update movie descriptions in the database from a CSV file"

    def handle(self, *args, **kwargs):
        # 📥 Ruta del archivo CSV con las descripciones actualizadas
        csv_file = os.path.join(os.path.dirname(__file__), 'updated_movie_descriptions.csv')
  # Cambia el nombre si es necesario

        # ✅ Verifica si el archivo existe
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"CSV file '{csv_file}' not found."))
            return

        updated_count = 0

        # 📖 Abrimos el CSV y leemos cada fila
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                title = row.get('Title')
                new_description = row.get('Updated Description')

                if not title or not new_description:
                    self.stderr.write(self.style.WARNING(f"Skipping row with missing data: {row}"))
                    continue

                try:
                    # 🔍 Buscar la película por título
                    movie = Movie.objects.get(title=title)

                    # 📝 Actualizar la descripción
                    movie.description = new_description
                    movie.save()
                    updated_count += 1

                    self.stdout.write(self.style.SUCCESS(f"Updated: {title}"))

                except Movie.DoesNotExist:
                    self.stderr.write(self.style.WARNING(f"Movie not found: {title}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Failed to update {title}: {str(e)}"))

        # ✅ Al finalizar, muestra cuántas películas se actualizaron
        self.stdout.write(self.style.SUCCESS(f"Finished updating {updated_count} movies from CSV."))
