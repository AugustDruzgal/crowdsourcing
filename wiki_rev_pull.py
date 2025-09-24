import requests
import pandas as pd

events = [
    {"EventName": "Death of Pope Benedict XVI", "WikipediaArticleTitle": "Death and funeral of Pope Benedict XVI"},
    {"EventName": "2023 Turkey–Syria Earthquake", "WikipediaArticleTitle": "2023 Turkey–Syria earthquake"},
    {"EventName": "Silicon Valley Bank Collapse", "WikipediaArticleTitle": "Collapse of Silicon Valley Bank"},
    {"EventName": "OceanGate Titan Submersible Implosion", "WikipediaArticleTitle": "Titan submersible implosion"},
    {"EventName": "2023 Lahaina (Maui) Wildfires", "WikipediaArticleTitle": "2023 Hawaii wildfires"},
    {"EventName": "2023 Hamas attack on Israel", "WikipediaArticleTitle": "2023 Hamas-led attack on Israel"},
    {"EventName": "Death of Matthew Perry", "WikipediaArticleTitle": "Matthew Perry"},
    {"EventName": "OpenAI CEO Sam Altman Ousted", "WikipediaArticleTitle": "Sam Altman"},
    {"EventName": "Francis Scott Key Bridge Collapse", "WikipediaArticleTitle": "Francis Scott Key Bridge collapse"},
    {"EventName": "2024 Taiwan Earthquake", "WikipediaArticleTitle": "2024 Hualien earthquake"},
    {"EventName": "Artemis I Launch", "WikipediaArticleTitle": "Artemis 1"},
    {"EventName": "Super Bowl LVII Result", "WikipediaArticleTitle": "Super Bowl LVII"},
    {"EventName": "Everything Everywhere All at Once Wins Best Picture", "WikipediaArticleTitle": "Everything Everywhere All at Once"},
    {"EventName": "Apple Vision Pro Announced", "WikipediaArticleTitle": "Apple Vision Pro"},
    {"EventName": "India's Chandrayaan-3 Moon Landing", "WikipediaArticleTitle": "Chandrayaan-3"},
    {"EventName": "Spain wins FIFA Women's World Cup Final", "WikipediaArticleTitle": "2023 FIFA Women's World Cup final"},
    {"EventName": "Super Bowl LVIII Result", "WikipediaArticleTitle": "Super Bowl LVIII"},
    {"EventName": "Oppenheimer Wins Best Picture", "WikipediaArticleTitle": "Oppenheimer (film)"},
    {"EventName": "2024 North American Solar Eclipse", "WikipediaArticleTitle": "Solar eclipse of April 8, 2024"},
    {"EventName": "GPT-4o Announced by OpenAI", "WikipediaArticleTitle": "GPT-4o"}
]


headers = {
    'User-Agent': 'WikipediaLagAnalysis/1.0 (contact@example.com)'
}

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"
all_revisions_data = []


for event in events:
    event_name = event["EventName"]
    article_title = event["WikipediaArticleTitle"]
    

    PARAMS = {
        "action": "query",
        "prop": "revisions",
        "titles": article_title,
        "rvlimit": "max",
        "rvprop": "timestamp|user|comment|ids", 
        "rvdiffto": "prev",
        "format": "json",
        "rvdir": "newer", 
        "rvstart": "2022-01-01T00:00:00Z",
        "rvend": "2025-12-31T23:59:59Z"
    }

    try:
        response = S.get(url=URL, params=PARAMS, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        pages = data.get("query", {}).get("pages", {})
        page_id = list(pages.keys())[0]

        if "revisions" in pages[page_id]:
            for rev in pages[page_id]["revisions"]:
                diff_content = rev.get('diff', {}).get('*', '')
                
                all_revisions_data.append({
                    "Event": event_name,
                    "Timestamp (UTC)": rev.get("timestamp"),
                    "User": rev.get("user"),
                    "Edit_Summary": rev.get("comment"),
                    "Diff_Content": diff_content
                })
        else:
            print(f"No revisions found for '{article_title}' in the date range.")

    except requests.exceptions.RequestException as e:
        print(f"ERROR fetching data for '{article_title}': {e}")

df_revisions = pd.DataFrame(all_revisions_data)

if not df_revisions.empty:
    print(df_revisions.head())
    df_revisions.to_csv("wikipedia_revisions_with_diffs.csv", index=False)
else:
    print("\n ERROR: No data was collected")