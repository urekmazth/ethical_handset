import re
import subprocess

valid_mac_pattern = r'(\w\w:){5}\w\w'


def get_mac_address(interface: str):
    output = subprocess.check_output(["ifconfig", interface])
    result = re.search(valid_mac_pattern, output)

    if result:
        return result.group(0)

    raise Exception(
        f"[-] Failed to read MAC address for interface {interface}")


def update_mac_address(interface: str, new_mac: str):
    # verify if mac address is valid
    is_valid_mac = re.fullmatch(valid_mac_pattern, new_mac)

    if is_valid_mac:
        # Update mac address
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])

        current_mac = get_mac_address(interface)

        if current_mac == new_mac:
            return True
