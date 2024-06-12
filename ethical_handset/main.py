import typer
from rich import print as rich_print

from validations import verify_os
from preconnection import (
    update_mac_address, update_interface_mode, InterfaceMode,)

app = typer.Typer()

preconnection_app = typer.Typer(help="Preconnection attacks")

app.add_typer(preconnection_app, name="preconnection")

os_is_valid = verify_os()


@preconnection_app.command(name="update-ether",
                           help="Change MAC address for interface")
def change_mac_address(
    interface: str = typer.Option(..., "--interface", "-i",
                                  help="Network Interface name"),
        new_mac: str = typer.Option(..., "--ether", help="New MAC address")):
    """Updates MAC address"""

    rich_print(
        f"[green bold][+] Updating MAC address for interface {interface} [/]")

    interface = interface.strip()
    new_mac = new_mac.strip()

    if os_is_valid:
        success = update_mac_address(interface=interface, new_mac=new_mac)

        if success:
            rich_print(
                f"[blue bold][+] MAC address for {interface} updated to {new_mac}[/]")
        else:
            rich_print(
                "[red bold][-] Failed to update MAC address[/]")
    else:
        rich_print(
            "[red bold][-] Your operating system is not supported for this operation[/]")


@preconnection_app.command(name="update-mode",
                           help="Change Interface mode")
def change_interface_mode(
    interface: str = typer.Option(..., "--interface", "--ether", "-i",
                                  help="Network interface name"),
        mode: str = typer.Option(
            InterfaceMode.STAGED.name,
            "--mode", "-m",
            help="New interface mode. Staged or Monitor"),):

    if os_is_valid:
        try:
            success = update_interface_mode(
                mode=InterfaceMode[mode.upper()], interface=interface)

            if success:
                rich_print(
                    f"[blue bold][+] {interface} mode changed to {mode}")
            else:
                rich_print(
                    "[red bold][-] Failed to change interface mode")

        except KeyError:
            rich_print(
                f"[red bold][-] Unknown mode {mode}[/]")
    else:
        rich_print(
            "[red bold][-] Your operating system is not supported for this operation[/]")


if __name__ == '__main__':
    app()
