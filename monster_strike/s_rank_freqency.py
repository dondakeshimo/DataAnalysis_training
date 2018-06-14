from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm


def login(session):
    r_token = session.get("https://gamewith.jp/user/login")
    soup_token = BeautifulSoup(r_token.text, "html.parser")
    mojolicious_csrf_token = soup_token.find(
                                 attrs={'name': 'mojolicious_csrf_token'})
    mojolicious_csrf_token = mojolicious_csrf_token.get('value')
    payload = {
            'username': 'XXX@yahoo.co.jp',
            'password': 'XXX'
    }
    payload['mojolicious_csrf_token'] = mojolicious_csrf_token
    r_login = session.post("https://gamewith.jp/user/login", data=payload)
    if r_login.status_code == 200:
        print("login success")
        return session
    else:
        print("login error")
        return session


def get_quests_urls(session):
    url = "https://xn--eckwa2aa3a9c8j8bve9d.gamewith.jp/article/show/3054"
    res = session.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    table_data = soup.find_all("table")
    quest_urls = []
    for table in table_data[1:-1]:
        a_data = table.find_all("a")
        for i, a in enumerate(a_data):
            if i % 2 == 0:
                continue
            else:
                quest_urls.append(a.get("href"))
    return session, quest_urls


def make_monster_list(session, quest_urls):
    monster = []
    for url in tqdm(quest_urls):
        res = session.get(url)
        soup = BeautifulSoup(res.text, "lxml")
        table_data = soup.find_all("table")
        for table in table_data:
            tr_tag = table.find_all("tr")
            th_tag = tr_tag[0].find("th")
            if not th_tag:
                break
            elif th_tag.string == "Sランク":
                for tr in tr_tag[1:]:
                    a_tag = tr.find_all("a")
                    if a_tag:
                        monster.append(a_tag[1].string)
                    else:
                        break
    return monster


def count_frequency(monster):
    monster_unique = set(monster)
    monster_count = {}
    for mon in monster_unique:
        monster_count[mon] = monster.count(mon)
    monster_df = pd.DataFrame(list(monster_count.items()))
    monster_df.columns = ["monster", "frequency"]
    monster_df = monster_df.sort_values(by=["frequency"], ascending=False)
    monster_df_upper = monster_df[monster_df["frequency"] > 3]
    monster_df_upper.to_csv("s_rank_freqency.csv", index=None)


def main():
    session = requests.Session()
    session = login(session)
    session, quest_urls = get_quests_urls(session)
    monster = make_monster_list(session, quest_urls)
    count_frequency(monster)


if __name__ == "__main__":
    main()
