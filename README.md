# Event Manager
Popis aplikace: <br>Webová aplikace s názvem EventManager je psaná v programovacím jazyce Python (verzi 3.12) a postavena na webovém frameworku Django.
<br><br>
Cílem tohoto projektu je vytvoření platformy pro správu a evidenci různých událostí v podobě webové aplikace. Aplikace je vhodná pro všechny organizátory akcí, chtějící mít jejich správu řešenou na jednom místě a také účastníky těchto akcí, kteří se mohou přehledně a pohodlně na jednotlivé akce hlásit a také o nich diskutovat.<br>
Pro zajištění efektivního využití jsou implementovány tři úrovně oprávnění, které umožňují různé možnosti správy a přístupu k událostem. 
<br><br>
<strong>Nepřihlášený uživatel:</strong> <br>
Nepřihlášeným uživatelům je umožněn pouze náhled veřejně dostupných událostí, včetně zobrazení jejich detailů a čtení komentářů. Uživatelé se mohou registrovat nebo přihlásit ke svému existujícímu účtu. 
<br><br>
<strong>Účastník:</strong><br>
Uživatel s tímto oprávněním může spravovat svůj uživatelský účet (změna jména, emailu, hesla) a přihlašovat se na jednotlivé akce. Dále může přidávat komentáře a také je později mazat. 
<br>
-[ucastnik (Kints123)]
<br><br>
<strong>Pořadatel:</strong><br>
Pořadatelé mají stejná oprávnění jako účastníci a navíc mohou vytvářet nové události. V jejich sekci "Moje akce" jsou události rozděleny na dvě části: jako účastník a jako pořadatel. Pořadatelé mohou své události upravovat a mazat, ale nově vytvořené události jsou nejprve odeslány ke schválení a nejsou tak na webu viditelné okamžitě. Navíc mohou účastníků rozesílat emailové zprávy a to buďto jednotlivě a nebo hromadně.
<br>
-[poradatel (Letad123)]
<br><br>
<strong>Administrátor:</strong><br>
Administrátor má všechna oprávnění pořadatele a účastníka a navíc má právo schvalovat nové události. Administrátor může upravovat a mazat všechny události, spravovat komentáře, a navíc má plnou kontrolu nad typy událostí, které nejsou přístupné jiným uživatelům.
<br>
-[administrator (Rotar123)]
<br><br>


ER diagram modelů:
![diagram](media/img/ERDiagram.png)

Ukázka práce s Backlogem:
![backlog](media/img/Backlog.png)
![backlog_detail](media/img/Backlog_detail.png)

- K aplikaci se můžete dostat jednoduše pomocí git clone https://github.com/Komet-ka/Final_project.git
- Následné spuštění zařídí příkaz: python .\manage.py runserver
- Pro zajištění korektních migrací byl využíván příkaz: python .\manage.py makemigrations viewer
- API poskytující seznam všech plánovaných událostí je dostupné zde: 127.0.0.1:8000/list_events/

<br><br>

Checklist základních bodů ke splnění:
- [x] zprovoznit git
- [x] vytvořit aplikaci
- [x] dostat se do admin rozhraní
- [x] vytvořit modely a udělat migrace
- [x] vytvořit hlavní HTML stránku
- [x] názvy přepsat do češtiny
- [x] upravit záhlaví
- [x] doplnit vyhledávací pole
- [x] upravit event formulář
- [x] prohodit logování a my account uživatele
- [x] zvětšit description area
- [x] event type, ať se zobrazují názvy místo čísel
- [x] kalendář - výběr data
- [x] schovat create date
- [x] vstupné - odkázat na description
- [x] zkusit tam dát barvy a třeba i obrázky
- [x] event types - dát do levého panelu pod sebe
- [x] doplnit validátory k polím
- [x] oprávnění
- [x] doplnit styly
- [x] zakomponovat JS


