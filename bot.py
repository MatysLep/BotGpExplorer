import re
from playwright.sync_api import Playwright, sync_playwright, expect


def convertir_en_secondes(texte: str) -> int:
    nombres = [int(num) for num in re.findall(r'\d+', texte)]

    # minutes et secondes
    minutes = nombres[0] if len(nombres) > 0 else 0
    secondes = nombres[1] if len(nombres) > 1 else 0

    return (minutes * 60 + secondes) * 1000


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://gp-explorer.fr/billetterie/revente/")
    html_content = page.content()
    page.goto("https://widget.weezevent.com/ticket/gp-explorer-bourse-aux-billets?locale=fr-FR")
    page.wait_for_timeout(5000)

    if page.query_selector("#wz-button-continue") is not None:
        page.query_selector("#wz-button-continue").click()

    page.wait_for_selector(".queue-rank-number")

    while True :
        num_attente = page.query_selector(".queue-rank-number")
        if num_attente is None :
            print("🎉élément a disparu🎉")
            break
        else:
            print(f"⏰plus que {num_attente.inner_text()} places ⏰")
            page.wait_for_selector(".queue-waiting-time-count-down")
            time_wait = convertir_en_secondes(page.query_selector(".queue-waiting-time-count-down").inner_text())
            print(f"temps à attendre : {time_wait} ")
            page.wait_for_timeout(time_wait)

    message_description = page.query_selector(".wz-message-description")
    if message_description is not None and message_description.inner_text() == "Aucun billet disponible pour le moment, veuillez essayer plus tard." :
        print("plus de billet disponible pour le moment...😢")
    else :
        print(f"Des billets sont en lignes")
        # AJOUT DE LA SUITE DU CODE
            ## REGARDER SI LES PLACES SONT CELLES DU DIMANCHE
                ### APPUYER 4x SUR LE BOUTONS AJOUTER DES PLACES
                    #### CLIQUER SUR LE BOUTON "CONTINUER" POUR LE PAIEMENT
                        ##### AUTO REMPLIR LES INFORMATIONS DE MA CB
    page.wait_for_timeout(99999999)



playwright = sync_playwright().start()
run(playwright)