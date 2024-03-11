import subprocess
import re

def get_ip_address(interface):
    try:
        # ifconfig 명령 실행
        output = subprocess.check_output(["ifconfig", interface]).decode('utf-8')
        # IP 주소를 찾기 위한 정규 표현식
        ip_pattern = r"inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        # 결과에서 IP 주소 찾기
        match = re.search(ip_pattern, output)
        if match:
            ip_address = match.group(1)
            return ip_address
        else:
            return None
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None

# wlo1 인터페이스의 IP 주소 가져오기
ip_address = get_ip_address("wlo1")
if ip_address:
    print(f"wlo1 interface IP address: {ip_address}")
else:
    print("Failed to get wlo1 interface IP address")
