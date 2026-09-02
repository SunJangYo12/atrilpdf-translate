import os
import telnetlib
import time

HOST = "192.168.0.100"
PORT = 9090

tn = telnetlib.Telnet(HOST, PORT)

# Tunggu sampai muncul prompt
tn.read_until(b"Translate Server 1.0")



all = []
for folder, subfolders, files in os.walk("original"):
    for file in files:
        full = os.path.join(folder, file)

        all.append(full)

all.sort()

for full in all:
    outfile = full.replace("original", "translate")

    if os.path.exists(outfile):
        print("SKIP: "+outfile)
        continue

    print(full)
    outpath = os.path.dirname(outfile)

    os.makedirs(outpath, exist_ok=True)

    with open(full, "r", encoding="utf-8", errors="ignore") as fd: #errors="replace"
        data = fd.read()
        if data == "":
            data = "zz"

        tn.write(data.encode('utf-8'))

        for i in range(4):
            tn.write(b"\n")

        result = tn.read_until(b"============= zzzzzzText Output ================", timeout=30)
        result = result.decode("utf-8", errors="ignore")
        result = result.split("============= Text Output ================")
        result = result[1].split("============= zzzzzzText Output ================")

        with open(outfile, "w") as wd:
            wd.write(result[0])

        time.sleep(1)

#tn.close()
