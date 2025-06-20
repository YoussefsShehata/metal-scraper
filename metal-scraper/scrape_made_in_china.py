import csv
import re
import os
import tempfile
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

def scrape_made_in_china(search_term):
    base_url = (
        "https://www.made-in-china.com/productdirectory.do?"
        "subaction=hunt&style=b&mode=and&code=0&comProvince=nolimit&order=0"
        "&isOpenCorrection=1&org=top&keyword=&file=&searchType=0&word="
    )
    encoded_search = search_term.replace(' ', '+')
    max_pages = 5

    options = uc.ChromeOptions()
    options.add_argument("--headless")
    driver = uc.Chrome(options=options)

    all_results = []

    for page in range(1, max_pages + 1):
        search_url = f"{base_url}{encoded_search}&page={page}"
        print(f"\n🔍 Searching Page {page}: {search_url}\n")
        driver.get(search_url)

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".prod-content"))
            )
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            items = soup.select(".prod-content")

            for item in items:
                title_tag = item.select_one(".product-name a")
                price_tag = item.select_one(".price-info .price")
                moq_tag = item.select_one(".product-property .info:nth-of-type(2)")
                supplier_tag = item.select_one(".compnay-name")

                if not title_tag or not price_tag:
                    continue

                raw_price = price_tag.get_text(strip=True)
                if not re.search(r"\d", raw_price):
                    continue

                moq = moq_tag.get_text(strip=True) if moq_tag else ""

                all_results.append({
                    "title": title_tag.get("title", title_tag.text.strip()),
                    "supplier": supplier_tag.get_text(strip=True) if supplier_tag else "",
                    "raw_price": raw_price,
                    "moq": moq,
                    "link": title_tag["href"] if title_tag.has_attr("href") else "",
                })

        except Exception as e:
            print(f"⚠️ Skipping page {page} due to error:\n{e}")

    driver.quit()

    df = pd.DataFrame(all_results)
    out_path = os.path.join(tempfile.gettempdir(), "results.csv")
    df.to_csv(out_path, index=False)
    print(f"\n✅ {len(df)} results saved to {out_path}")
    # -------------------------------------------

    if not df.empty:
        print(df.to_string(index=False))
    else:
        print("No data found.")

    return df  # ✅ Return the DataFrame


#if __name__ == "__main__":
   #scrape_made_in_china("stainless steel TP316L seamless pipe")
