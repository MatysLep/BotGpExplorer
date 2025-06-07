import re
import time
import asyncio
from playwright.async_api import async_playwright
import requests

def send_discord_webhook(message: str) -> None:
    webhook_url = "https://discord.com/api/webhooks/1381010025698295869/7vNmzHLQzCsOd7gP8cllVuhWIRO_x2xpPqR9esGJvW790aGml0O09bBv9gaDiyQH2Bj7"
    data = {
        "content": message
    }

    response = requests.post(webhook_url, json=data)

    if response.status_code == 204:
        print("✅ Message envoyé avec succès.")
    else:
        print(f"❌ Échec de l'envoi : {response.status_code} - {response.text}")


def convertir_en_secondes(texte: str) -> int:
    nombres = [int(num) for num in re.findall(r'\d+', texte)]

    minutes = nombres[0] if len(nombres) > 0 else 0
    secondes = nombres[1] if len(nombres) > 1 else 0

    return (minutes * 60 + secondes) * 1000

async def run(playwright) -> bool:
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    await page.goto("https://gp-explorer.fr/billetterie/revente/")
    html_content = await page.content()
    await page.goto("https://widget.weezevent.com/ticket/gp-explorer-bourse-aux-billets?locale=fr-FR")
    await page.wait_for_timeout(5000)

    if await page.query_selector("#wz-button-continue") is not None:
        await (await page.query_selector("#wz-button-continue")).click()

    while True:
        num_attente = await page.query_selector(".queue-rank-number")
        if num_attente is None:
            print("🎉élément a disparu🎉")
            break
        else:
            text = await num_attente.inner_text()
            print(f"⏰plus que {text} places ⏰")
            await page.wait_for_selector(".queue-waiting-time-count-down")
            await page.wait_for_timeout(2000)
            time_element = await page.query_selector(".queue-waiting-time-count-down")
            time_text = await time_element.inner_text()
            time_wait = convertir_en_secondes(time_text)
            print(f"temps à attendre : {time_wait}")
            await page.wait_for_timeout(time_wait)

    message_description = await page.query_selector(".wz-message-description")
    if message_description is not None and await message_description.inner_text() == "Aucun billet disponible pour le moment, veuillez essayer plus tard.":
        print("plus de billet disponible pour le moment...😢")
        await context.close()
        await browser.close()
        return True
    else:
        print(f"Des billets sont en lignes")

        available_date = await page.query_selector_all(".neo-rate-group-title")

        # Si des dates sont disponibles
        if available_date is not None :

            # boucle sur chaque date
            for date in available_date:
                text = await date.inner_text()
                print(f"billet(s) disponible(s) pour {text}")
                # Si la date correspond à DIMANCHE
                if text.strip() == "DIMANCHE":
                    print("PLACE DISPONIBLE LE DIMANCHE !!!")
                    # Appui 4 fois sur le bouton "+" pour avoir 4 places
                    counter = await page.query_selector('button[aria-label^="Ajouter 1 billet"]')
                    if counter:
                        for _ in range(4):
                            await counter.click()
                            await page.wait_for_timeout(400)  # Petite pause pour être sûr que le compteur se met à jour
                    else:
                        print("Bouton pour ajouter des billets non trouvé.")
                    # Attend le bouton "Suite" pour cliquer dessus
                    await page.wait_for_selector(".wz-neo-button-2.wz-cta-next")
                    await page.click(".wz-neo-button-2.wz-cta-next")
                    send_discord_webhook("🚨🚨🚨HEYYYY ALERTE A MALIBU, Y'A DES PLACES POUR LE DIMANCHE !!! VA CHECK TON PANIER !!🚨🚨🚨")
                    await page.wait_for_timeout(99999999)
                    return False
        return True

async def main():
    restart = True
    while restart:
        try :
            async with async_playwright() as playwright:
                restart = await run(playwright)
        except Exception as e:
            print(e)
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())