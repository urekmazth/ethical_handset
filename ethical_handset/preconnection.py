from enum import Enum, auto
import re
import subprocess

from rich import print as rich_print

valid_mac_pattern = r'(\w\w:){5}\w\w'


class InterfaceMode(Enum):
    STAGED = "STAGED",
    MONITOR = "MONITOR",


def get_mac_address(interface: str):
    output = subprocess.check_output(["ifconfig", interface])
    result = re.search(valid_mac_pattern, str(output))

    if result:
        return result.group(0)

    raise rich_print(
        f"[red bold][-] Failed to read MAC address for interface {interface}[/]")


def update_mac_address(interface: str, new_mac: str):
    # verify if mac address is valid
    is_valid_mac = re.fullmatch(valid_mac_pattern, new_mac)
    current_mac = get_mac_address(interface)

    if is_valid_mac and current_mac:
        # Update mac address
        subprocess.call(["ifconfig", interface, "down"])
        subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
        subprocess.call(["ifconfig", interface, "up"])

        current_mac = get_mac_address(interface)

        if current_mac == new_mac:
            return True


def update_interface_mode(mode: InterfaceMode, interface: str):
    print(mode, interface)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["iwconfig", interface, "mode", mode.name])
    subprocess.call(["ifconfig", interface, "up"])

    return True
