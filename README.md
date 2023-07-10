# SPOSÓB URUCHOMIENIA APLIKACJI

1. Przejdż do katalogu głównego projketu
2. Aktywuj wirtualne środowisko poleceniem:
    #### Na systemie Windows:
    ``` venv\Scripts\activate ```
    
    #### Na systemach Linux/Mac:
    ``` source venv/bin/activate ```

3. Następnie zainstaluj potrzebne zależności: ``` pip install -r requirements.txt ```
4. Kolejny krok to wykonanie migracji: 
   * ```  python manage.py makemigrations ``` 
   * ``` python manage.py migrate```
5. Końcowy poleceniem będzie ``` python manage.py runserver ```, które uruchomi projekt
6. Ścieżki do prouszania się po projekcie opisane są w pliku urls.py aplikacji "api"
7. W projekcie istnieją konta klienta i sprzedawcy:
   ```
   Konto klienta:
   - login: klient
   - hasło: klient
   
   Konto sprzedawcy:
   - login: sprzedawca
   - hasło: sprzedawca
   ```