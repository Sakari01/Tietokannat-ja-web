Keskeneräisessä sovelluksessa käyttäjä voi:
  - Luoda uuden käyttäjän, sekä kirjautua sisään ja ulos
  - Luoda uusia keskustelualueita, sekä keskustelupalstoja näille alueille
  - lähettää viestejä ja nähdä muiden lähettämät viestit, sekä niiden lähetysajankohdat

## ASENNUS

Kloonaa tämä repositorio.
```
git clone https://github.com/Sakari01/Tietokannat-ja-web
cd Tietokannat-ja-web
```
siirry juurikansioon. Luo kansioon .env-tiedosto ja määritä se näin:
```
DATABASE_URL=postgresql:///<new-db-name>
SECRET_KEY=<salainen-avain>
```
Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
python3 -m venv venv
source venv/bin/activate
pip install -r ./requirements.txt
```
Määritä vielä tietokannan skeema komennolla
```
psql < schema.sql
```
Nyt voit käynnistää sovelluksen komennolla
```
flask run
```

