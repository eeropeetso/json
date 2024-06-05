import json
import tkinter as tk
from tkinter import filedialog
import datetime
from functools import reduce
from Person import Person


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def calculate_age(birth_date):
    today = datetime.date.today()
    birth_date = datetime.datetime.strptime(birth_date, "%Y-%m-%d").date()

    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age


def analyze_data(people):
    total_people = len(people)

    name_lengths = list(map(lambda person: (person.name, len(person.name)), people))
    longest_name, longest_name_length = reduce(lambda a, b: a if a[1] > b[1] else b, name_lengths)

    # Corrected calculation for actors
    total_actors = len(list(filter(lambda person: 'näitleja' in person.profession.lower(), people)))

    born_in_1997 = len(list(filter(lambda person: person.birth_date.startswith('1997'), people)))

    professions = list(map(lambda person: person.profession, people))
    unique_professions = len(set(professions))

    names_with_more_than_two_parts = len(list(filter(lambda person: len(person.name.split()) > 2, people)))

    same_birth_death_date_except_year = len(list(filter(lambda person: person.birth_date[5:] == person.death_date[5:], people)))

    living_people = list(filter(lambda person: person.death_date == '0000-00-00', people))
    living_people.sort(key=lambda person: datetime.datetime.strptime(person.birth_date, "%Y-%m-%d"))

    oldest_living_person = living_people[0]
    oldest_living_person_age_years = calculate_age(oldest_living_person.birth_date)

    dead_people = total_people - len(living_people)

    oldest_dead_person = max(filter(lambda person: person.death_date != '0000-00-00', people), key=lambda x: int(x.death_date[:4]) - int(x.birth_date[:4]))
    oldest_dead_person_age = int(oldest_dead_person.death_date[:4]) - int(oldest_dead_person.birth_date[:4])

    # Format birth and death dates to "d.m.Y" format
    birth_date_format = datetime.datetime.strptime(oldest_living_person.birth_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    death_date_format = datetime.datetime.strptime(oldest_dead_person.birth_date, "%Y-%m-%d").strftime("%d.%m.%Y")

    # Concatenate all analysis results into a single list
    results = [
        f"1. Isikute arv kokku: {total_people}",
        f"2. Kõige pikem nimi ja tähemärkide arv: {longest_name}, {longest_name_length}",
        f"3. Kõige vanem elav inimene: {oldest_living_person.name}, {oldest_living_person_age_years}, {birth_date_format}",
        f"4. Kõige vanem surnud inimene: {oldest_dead_person.name}, {oldest_dead_person_age}, {birth_date_format} - {death_date_format}",
        f"5. Näitlejate koguarv: {total_actors}",
        f"6. Sündinud 1997 aastal: {born_in_1997}",
        f"7. Kui palju on erinevaid elukutseid: {unique_professions}",
        f"8. Nimi sisaldab rohkem kui kaks nime: {names_with_more_than_two_parts}",
        f"9. Sünniaeg ja surmaaega on sama v.a. aasta: {same_birth_death_date_except_year}",
        f"10. Elavaid ja surnud isikud: Elavaid - {len(living_people)}, Surnud - {dead_people}"
    ]

    # Return the concatenated list of analysis results
    return results


def open_file_and_analyze(root, text_results, result_frame):
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        try:
            data = read_json_file(file_path)
            people = [Person(person['nimi'], person['amet'], person['sundinud'], person['surnud']) for person in data]
            analysis_result = analyze_data(people)
            update_text(text_results, analysis_result)
            result_frame.pack(pady=10)
        except Exception as e:
            pass


def update_text(text_results, analysis_result):
    text_results.delete(1.0, tk.END)
    text_to_display = "\n".join(analysis_result)
    text_results.insert(tk.END, text_to_display)


def main():
    root = tk.Tk()
    root.title("JSON Analysis")

    result_frame = tk.Frame(root)

    text_results = tk.Text(result_frame, height=20, width=80)
    text_results.grid(row=0, column=0)

    btn_open_file = tk.Button(root, text="Open JSON File",
                              command=lambda: open_file_and_analyze(root, text_results, result_frame))
    btn_open_file.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()
