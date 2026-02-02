import json
import random

# Ordbok som kobler fagnavn til filnavn
SUBJECT_FILES = {
    "INFO100": "info100.json",
    "INFO132 / DATA110": "info132_data110.json",
    "INFO132 Begrepsbank": "info132_begreper.json",
    "INFO104": "info104.json"
}

def load_notes(filename):
    
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"\n--- FEIL ---")
        print(f"Filen '{filename}' ble ikke funnet.")
        print("Sørg for at filen er i samme mappe som skriptet.")
        print("--- /FEIL ---")
        return None
    except json.JSONDecodeError:
        print(f"\n--- FEIL ---")
        print(f"Filen '{filename}' er ikke en gyldig JSON-fil.")
        print("--- /FEIL ---")
        return None

def ask_question(q):

    
    print("\nSpørsmål:", q["question"])

    options = [(opt, opt == q["answer"]) for opt in q["options"]]
    random.shuffle(options)

    for i, (opt, _) in enumerate(options, 1):
        print(f"{i}. {opt}")

    # Finn riktig svartekst på forhånd (for fasit)
    correct_answer_text = ""
    for opt, is_correct in options:
        if is_correct:
            correct_answer_text = opt
            break
            
    try:
        choice_input = input(f"Velg alternativ (1-{len(options)}): ")
        choice_index = int(choice_input) - 1
        
        if 0 <= choice_index < len(options):
            if options[choice_index][1]:
                print("✅ Riktig!")
                return 1
            else:
                print(f"❌ Feil. Fasit: {correct_answer_text}")
                return 0
        else:
            print(f"❌ Ugyldig valg. Fasit: {correct_answer_text}")
            return 0
            
    except ValueError:
        print(f"❌ Ugyldig input. Fasit: {correct_answer_text}")
        return 0
    except Exception as e:
        print(f"En feil oppstod: {e}")
        print(f"Fasit er: {correct_answer_text}")
        return 0

def run_exam(notes, category, num_questions=10):
    """Kjører en quiz for en valgt kategori."""
    
    pool = [q for q in notes[category] if "answer" in q and "options" in q]
    
    if not pool:
        print(f"Fant ingen gyldige spørsmål for kategorien '{category}'.")
        return

    random.shuffle(pool)
    
    num_to_ask = min(num_questions, len(pool))
    questions = pool[:num_to_ask]

    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n--- {category} | Spørsmål {i}/{len(questions)} ---")
        score += ask_question(q)

    print("\n" + "="*20)
    print("=== Oppsummering ===")
    print(f"Kategori: {category}")
    print(f"Score: {score}/{len(questions)} ({(score/len(questions)):.0%})")
    print("="*20 + "\n")

def run_category_menu(subject_name, notes):
    categories = list(notes.keys())
    
    while True:
        print(f"\nDu har valgt: {subject_name}")
        print("Velg kategori:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print("0. Tilbake til fagvalg")

        try:
            choice_str = input(f"Skriv nummer (0-{len(categories)}): ")
            choice = int(choice_str)

            if choice == 0:
                print("Går tilbake til fagvalg...")
                break # Går ut av denne løkken, tilbake til main()
                
            if 1 <= choice <= len(categories):
                category = categories[choice - 1]
                run_exam(notes, category) # Starter quizen
            else:
                print(f"Ugyldig valg. Skriv et tall mellom 0 og {len(categories)}.")
        
        except ValueError:
            print("Ugyldig input. Skriv et tall.")
        except KeyboardInterrupt:
            print("\nAvslutter... Ha det bra!")
            exit() # Avslutter hele programmet

def main():
    
    print("Velkommen til Eksamens-Quizen!")
    
    subject_names = list(SUBJECT_FILES.keys())

    while True:
        print("\nHvilket fag vil du øve på?")
        for i, name in enumerate(subject_names, 1):
            print(f"{i}. {name}")
        print("0. Avslutt programmet")

        try:
            choice_str = input(f"Skriv nummer (0-{len(subject_names)}): ")
            choice = int(choice_str)

            if choice == 0:
                print("Lykke til på eksamen! Ha det bra.")
                break # Avslutter hovedløkken og programmet
            
            if 1 <= choice <= len(subject_names):
                subject_name = subject_names[choice - 1]
                filename = SUBJECT_FILES[subject_name]
                
                # Last inn data for det valgte faget
                notes_data = load_notes(filename)
                
                # Hvis filen ble lastet inn (ikke None), start kategorimenyen
                if notes_data:
                    run_category_menu(subject_name, notes_data)
            
            else:
                print(f"Ugyldig valg. Skriv et tall mellom 0 og {len(subject_names)}.")

        except ValueError:
            print("Ugyldig input. Skriv et tall.")
        except KeyboardInterrupt:
            print("\nAvslutter... Ha det bra!")
            break

if __name__ == "__main__":
    main()
