# %%
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import subprocess

# %%
contest = "abc278"
task = "d"
url = f"https://atcoder.jp/contests/{contest}/tasks/{contest}_{task}"


# %%
r = requests.get(url)

# %%
soup = BeautifulSoup(r.content, "html.parser")

# %%
tests = []
for i in range(1, 100):
    q = soup.find("h3", text=f"入力例 {i}")
    if not q:
        break
    while q.name != "pre":
        q = q.next_element
    
    a = soup.find("h3", text=f"出力例 {i}")
    if not a:
        break
    while a.name != "pre":
        a = a.next_element
    
    test = (q, a)
    tests.append(test)

    with open(f"{task}{i}.txt", "w") as f:
        f.write(q.text.replace("\r\n", "\n"))
    with open(f"{task}{i}_ans.txt", "w") as f:
        f.write(a.text.replace("\r\n", "\n"))

# %%
u = list(Path().glob(f"{task}.[c][cpp][py]"))
u += list(Path().glob(f"{task}.py"))
u = u[0]
print(u.name)

if u.suffix.lower() in [".c", ".cpp"]:
    print("### compiling...", end="")
    r = subprocess.run(["g++", "-o", u.stem, str(u)], shell=True, capture_output=True)
    if r.returncode == 0:
        print("done")
        if r.stdout.decode():
            print(r.stdout.decode())
    else:
        print("failed")
        print(r)

print("### runnning...")
for i in range(1, 100):
    q = Path(f"{task}{i}.txt")
    a = Path(f"{task}{i}_ans.txt")
    if not q.exists():
        break


    #print("-------------------")
    print("Sample:", i, "...", end="")
    with open(q, "r") as f:
        #print(f.read())
        pass
    if u.suffix.lower() == ".c":
        r = subprocess.run([str(u.stem), "<", str(q)], shell=True, capture_output=True)
    elif u.suffix.lower() == ".cpp":
        r = subprocess.run([str(u.stem), "<", str(q)], shell=True, capture_output=True)
    elif u.suffix.lower() == ".py":
        r = subprocess.run(["py", str(u), "<", str(q)], shell=True, capture_output=True)
    #print(r)
    ua = r.stdout.decode().replace("\r\n", "\n").strip()
    #print("Your answer:")
    #print(ua)

    with open(a, "r") as f:
        ans = f.read().strip()
        if ua == ans:
            print("ok")
        else:
            print("ng")
            #print(ans)

    

# %%



