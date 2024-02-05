import pygame
import os
import subprocess

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
szerokosc = 800
wysokosc = 700
okno = pygame.display.set_mode((szerokosc, wysokosc))
pygame.display.set_caption("Recoil Jump made by @werbel")

# Kolory
bialy = (255, 255, 255)
szary = (169, 169, 169)
czarny = (0, 0, 0)
czerwony = (255, 0, 0)

# Ścieżki do plików
sciezka_do_obrazu_tla = os.path.join("things", "graphics", "tlo.png")
sciezka_do_obrazu_przycisku = os.path.join("things", "graphics", "przycisk.png")
sciezka_do_folderu_poziomy = os.path.join("things", "poziomy")

# Sprawdzenie istnienia pliku z obrazem tła
if os.path.isfile(sciezka_do_obrazu_tla):
    tlo = pygame.image.load(sciezka_do_obrazu_tla)
    tlo = pygame.transform.scale(tlo, (szerokosc, wysokosc))
else:
    tlo = pygame.Surface((szerokosc, wysokosc))
    tlo.fill(bialy)

# Sprawdzenie istnienia pliku z obrazem przycisku
if os.path.isfile(sciezka_do_obrazu_przycisku):
    obraz_przycisku = pygame.image.load(sciezka_do_obrazu_przycisku)
    obraz_przycisku = pygame.transform.scale(obraz_przycisku, (200, 50))
else:
    obraz_przycisku = pygame.Surface((200, 50))
    obraz_przycisku.fill(szary)

# Funkcje pomocnicze
def rysuj_przycisk(przycisk):
    okno.blit(przycisk['obraz'], przycisk['rect'])
    okno.blit(przycisk['tekst'], przycisk['tekst_pozycja'])

# Funkcja główna
def main():
    # Napis nad przyciskami
    # Ścieżka do pliku czcionki
    sciezka_do_czcionki = os.path.join("things", "graphics", "BULLETCAMPUS.ttf")
    czcionka_napisu = pygame.font.Font(sciezka_do_czcionki, 68)

    napis_recoil_jump = czcionka_napisu.render("RECOIL JUMP", True, czarny)
    pozycja_napisu = (szerokosc // 2 - napis_recoil_jump.get_width() // 2, 20)  # Zmieniono wysokość napisu

    # Przyciski
    przyciski = []
    poziomy = ['easy', 'medium', 'hard']  # Dodane poziomy
    for i, poziom in enumerate(poziomy):
        sciezka_do_pliku = os.path.join(sciezka_do_folderu_poziomy, f"{poziom}.py")
        przycisk = {
            'rect': pygame.Rect(szerokosc // 2 - 100, wysokosc // 2 - 25 + i * 150, 200, 50),
            'tekst': None,
            'tekst_pozycja': (0, 0),
            'poziom': poziom.capitalize(),  # Zmieniono na dużą literę
            'obraz': obraz_przycisku.copy(),
            'plik': sciezka_do_pliku
        }
        przycisk['tekst'] = pygame.font.Font(None, 36).render(przycisk['poziom'], True, czarny)
        przycisk['tekst_pozycja'] = (przycisk['rect'].centerx - przycisk['tekst'].get_width() // 2,
                                     przycisk['rect'].centery - przycisk['tekst'].get_height() // 2)
        przyciski.append(przycisk)

    for przycisk in przyciski:
        przycisk['tekst_pozycja'] = (przycisk['rect'].centerx - przycisk['tekst'].get_width() // 2,
                                     przycisk['rect'].centery - przycisk['tekst'].get_height() // 2)

    # Pętla gry
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for przycisk in przyciski:
                    if przycisk['rect'].collidepoint(event.pos):
                        subprocess.Popen(["python", przycisk['plik']])

        okno.blit(tlo, (0, 0))  # Rysowanie tła
        okno.blit(napis_recoil_jump, pozycja_napisu)

        for przycisk in przyciski:
            rysuj_przycisk(przycisk)

        pygame.display.flip()

# Uruchomienie gry
if __name__ == "__main__":
    main()
