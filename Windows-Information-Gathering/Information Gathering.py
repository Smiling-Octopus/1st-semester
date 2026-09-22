import json
import os
import platform
import socket
import uuid
import urllib.error
import urllib.request

# psutil은 선택 의존 라이브러리입니다. 설치되어 있으면 NIC 및 시스템 정보를 더 자세히 가져옵니다.
try:
    import psutil
except ImportError:
    psutil = None

# 결과를 저장할 기본 파일 경로
log_file = "system_info.txt"


def get_os_info():
    """OS 및 시스템 정보를 포괄적으로 수집합니다.

    platform.uname()와 추가 플랫폼/파이썬 정보, CPU 및 메모리 상태를 포함합니다.
    psutil이 설치되어 있으면 부팅 시간과 물리/논리 CPU 개수 등 추가 정보도 수집합니다.
    """
    uname = platform.uname()
    info = {
        "system": uname.system,
        "node": uname.node,
        "release": uname.release,
        "version": uname.version,
        "machine": uname.machine,
        "processor": uname.processor,
        "platform": platform.platform(),
        "architecture": platform.architecture(),
        "python_version": platform.python_version(),
        "python_build": platform.python_build(),
        "python_compiler": platform.python_compiler(),
        "os_name": os.name,
    }

    # psutil이 있는 경우 더 많은 시스템 정보를 추가
    if psutil:
        try:
            info["cpu_count_logical"] = psutil.cpu_count(logical=True)
            info["cpu_count_physical"] = psutil.cpu_count(logical=False)
            info["boot_time"] = psutil.boot_time()
            info["memory_total_bytes"] = psutil.virtual_memory().total
            info["memory_available_bytes"] = psutil.virtual_memory().available
            info["swap_total_bytes"] = psutil.swap_memory().total
            info["swap_used_bytes"] = psutil.swap_memory().used
        except Exception:
            pass

    return info


def get_network_info():
    """모든 네트워크 인터페이스 및 주소 정보를 수집합니다.

    가능한 경우 psutil을 사용해 NIC 이름, MAC, IPv4, IPv6, 상태 정보를 모두 수집합니다.
    psutil이 없는 경우에는 기본 호스트 정보와 IP만 수집합니다.
    """
    info = {
        "hostname": None,
        "interfaces": [],
        "public_ip": None,
    }

    # 호스트 이름 수집
    try:
        info["hostname"] = socket.gethostname()
    except Exception:
        info["hostname"] = None

    if psutil:
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()
            for interface_name, addresses in addrs.items():
                iface = {
                    "name": interface_name,
                    "is_up": stats.get(interface_name).isup if stats.get(interface_name) else None,
                    "speed_mbps": stats.get(interface_name).speed if stats.get(interface_name) else None,
                    "mtu": stats.get(interface_name).mtu if stats.get(interface_name) else None,
                    "addresses": [],
                }
                for address in addresses:
                    iface["addresses"].append(
                        {
                            "family": str(address.family),
                            "address": address.address,
                            "netmask": address.netmask,
                            "broadcast": address.broadcast,
                            "ptp": address.ptp,
                        }
                    )
                info["interfaces"].append(iface)
        except Exception:
            info["interfaces"] = []
    else:
        # psutil 없을 때는 최소한의 네트워크 정보만 수집
        try:
            hostname = info.get("hostname") or socket.gethostname()
            info["interfaces"].append(
                {
                    "name": "default",
                    "address": socket.gethostbyname(hostname),
                    "mac_address": ":".join(
                        f"{(uuid.getnode() >> ele) & 0xff:02x}" for ele in range(40, -1, -8)
                    ),
                }
            )
        except Exception:
            pass

    # 공개 IP 수집
    try:
        info["public_ip"] = urllib.request.urlopen("https://api.ipify.org").read().decode("utf-8")
    except Exception:
        info["public_ip"] = None

    return info


def get_location_info():
    """외부 지리 위치 API에서 위치 관련 전체 정보를 가져옵니다.

    ipinfo.io 요청 결과 중 가능한 모든 필드를 수집합니다.
    """
    location = {
        "ip": None,
        "hostname": None,
        "city": None,
        "region": None,
        "country": None,
        "loc": None,
        "latitude": None,
        "longitude": None,
        "postal": None,
        "timezone": None,
        "org": None,
        "readme": None,
        "asn": None,
    }

    try:
        with urllib.request.urlopen("https://ipinfo.io/json") as response:
            data = json.loads(response.read().decode("utf-8"))
            for key in location.keys():
                location[key] = data.get(key)

            loc = data.get("loc")
            if loc:
                try:
                    lat, lon = loc.split(",")
                    location["latitude"] = lat
                    location["longitude"] = lon
                except ValueError:
                    pass
    except urllib.error.URLError:
        pass
    except Exception:
        pass

    return location


def write_report(filename, data):
    """수집된 데이터를 JSON 파일로 저장합니다."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # 수집 단계: OS/시스템, 네트워크 인터페이스, 위치 정보를 모두 취합합니다.
    report = {
        "os_info": get_os_info(),
        "network_info": get_network_info(),
        "location_info": get_location_info(),
    }

    # 결과를 파일로 출력하고 완료 메시지를 표시합니다.
    write_report(log_file, report)
    print(f"System info written to {log_file}")
