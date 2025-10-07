# GymPap-NameCollector
a project to scrape names from the GymPap website


> [!NOTE]
> To run the project first install the requirements via `pip install -r requirements.txt` and run `python -m GymPapNameCollector` afterwards.

> [!NOTE]
> The code may take some time to finish scraping *every article* published... I've already encountered 10+ minutes. Time will increase as more articles get published...

> [!WARNING]
> This project is *(and probably will stay)* in **Alpha**. This means that the name filter over at [.not_a_name.txt](/GymPapNameCollector/.not_a_name.txt) wont be complete and results should be checked.
> <br>*The filter is not guaranteed to work 100% of the time. There seems to be a hidden bug but for example "Buchhandlung" (which is blacklisted) still shows up in a name...*
