import json, re, os, datetime as dt, requests, urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin
urllib3.disable_warnings()
# Sirf official sites scrape hote hain. Aur sites jodni hon to yahan line add karo.
S=[("SSC","https://ssc.gov.in/"),("UPSC","https://upsc.gov.in/"),("BPSC","https://bpsc.bihar.gov.in/"),
("BPSSC","https://bpssc.bihar.gov.in/"),("CSBC Bihar","https://csbc.bihar.gov.in/"),("RRB Apply","https://rrbapply.gov.in/"),
("RRC","https://www.rrcb.gov.in/"),("IBPS","https://www.ibps.in/"),("SBI","https://sbi.co.in/web/careers"),
("RBI","https://opportunities.rbi.org.in/"),("NABARD","https://www.nabard.org/careers-notices1.aspx"),
("India Post","https://www.indiapost.gov.in/"),("Army","https://joinindianarmy.nic.in/"),("Navy","https://joinindiannavy.gov.in/"),
("Coast Guard","https://www.joinindiancoastguard.cdac.in/"),("NCS","https://www.ncs.gov.in/"),
("Apprenticeship India","https://www.apprenticeshipindia.gov.in/"),("NATS","https://www.nats.education.gov.in/"),
("Employment News","https://employmentnews.gov.in/")]
KW=re.compile(r"recruit|vacanc|notification|advertis|apply|examination|admit|walk-in|engagement|online application|result",re.I)
H={"User-Agent":"Mozilla/5.0 (personal job feed)"}
def get(u):
    for v in (True,False):
        try: return requests.get(u,headers=H,timeout=25,verify=v).text
        except Exception: pass
today=dt.date.today().isoformat()
old=json.load(open("jobs.json"))["jobs"] if os.path.exists("jobs.json") else []
oldmap={j["url"]:j for j in old}
jobs={};ok=set()
for name,url in S:
    h=get(url)
    if not h: print("FAIL",name); continue
    ok.add(name);n=0
    for a in BeautifulSoup(h,"html.parser").find_all("a",href=True):
        t=" ".join(a.get_text().split());u=urljoin(url,a["href"])
        if 15<len(t)<200 and KW.search(t) and u.startswith("http") and u not in jobs:
            jobs[u]={"title":t,"url":u,"source":name,"first_seen":oldmap.get(u,{}).get("first_seen",today)};n+=1
            if n>=25: break
    print(name,n)
for j in old:  # jo source fail hua uska purana data rakho (45 din tak)
    if j["source"] not in ok and j["url"] not in jobs and (dt.date.today()-dt.date.fromisoformat(j["first_seen"])).days<=45: jobs[j["url"]]=j
out=sorted(jobs.values(),key=lambda j:j["first_seen"],reverse=True)
json.dump({"updated":dt.datetime.utcnow().isoformat()+"Z","jobs":out},open("jobs.json","w"),ensure_ascii=False,indent=1)
