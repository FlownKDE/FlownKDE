# Color palette for text.
TX_RED = "\033[91m"    # Red text.
TX_GREEN = "\033[92m"  # Green text.
TX_YELLOW = "\033[93m" # Yellow text.
TX_BLUE = "\033[94m" # Blue text.
TX_MAGENTA = "\033[95m" # Magenta text.
TX_CYAN = "\033[96m" # Cyan text.
TX_WHITE = "\033[97m" # White text.
TX_GRAY = "\033[90m" # Gray text.
TX_BLACK = "\033[30m" # Black text.


# Color palette for background.
BG_RED = "\033[101m"   # Red background.
BG_GREEN = "\033[102m" # Green background.
BG_YELLOW = "\033[103m"# Yellow background.
BG_BLUE = "\033[104m" # Blue background.
BG_MAGENTA = "\033[105m" # Magenta background.
BG_CYAN = "\033[106m" # Cyan background.
BG_WHITE = "\033[107m" # White background.
BG_GRAY = "\033[100m" # Gray background.
BG_BLACK = "\033[40m" # Black background.


# Text formatting options.
BOLD = "\033[1m"       # Bold text.
UNDERLINE = "\033[4m"  # Underlined text.
ITALIC = "\033[3m"     # Italicized text.
BLINK = "\033[5m"      # Blinking text.


# Reset all text formatting.
END = "\033[0m"

class console:
    def clear():
        subprocess.run(["clear"])

    def info(message, end="\n", flush=False):
        print(f"{TX_BLUE}INFO 🢝 {END + message}", end=end, flush=flush)

    def error(message, end="\n", flush=False):
        print(f"{TX_RED}ERROR 🢝 {END + message}", end=end, flush=flush)

    def alert(message, end="\n", flush=False):
        print(f"{TX_RED}ALERT! 🢝 {message + END}", end=end, flush=flush)

    def success(message, end="\n", flush=False):
        print(f"{TX_GREEN}SUCCESS! 🢝 {message + END}", end=end, flush=flush)

try:
    import subprocess
    import os
    import time
except ModuleNotFoundError:
    console.error("The necessary python modules were not found")


def create_flown_shortcut():
    try:
        with open("start-flown", "w") as file: 
            file.write("""Xephyr :2 -resizeable -fullscreen &
sudo -g root DISPLAY=:2 startplasma-x11 > /dev/null 2>&1 &
echo "Flown to start correctly, to close flown, run "kill-flown" in your terminal""")
        subprocess.run(["sudo", "mv", "start-flown", "/usr/local/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/start-flown"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except Exception as a:
        console.error(f"""An unknown error has occurred
More details {a}""")
        
    try:
        with open("kill-flown", "w") as file: 
            file.write("""pkill Xephyr
        echo "Closure of Flown..." """)
        subprocess.run(["sudo", "mv", "kill-flown", "/usr/local/bin"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/kill-flown"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    except Exception as a:
        console.error(f"""An unknown error has occurred
More details {a}""")
        
def check_file_presence(file):
    if os.path.isfile(file):
        return True
    else:
        return False

def check_root_access():
    if os.getuid() !=0:
        return True
    else:
        return False

def give_root_auth(content):
    console.error(f"This script requires superuser (root) privileges.\n", end="")
    if input(f"Please type {BOLD + f'{content}' + END} to rerun the script with elevated permissions: ") == content:
        return True
    else:
        return False

class installation:
    def update_pkgs():
        console.info("Linux update in progress...", end=" ", flush=True)
        subprocess.run(["sudo", "apt", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.run(["sudo", "apt", "upgrade", "-y"], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print("Done !")

    def install_pkgs(pkgs):
        for to_install in pkgs:
            console.info(f"Installation of {to_install}...", end=" ", flush=True)
            subprocess.run(["sudo", "apt", "install", "-y", to_install], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            print("Done !")

def main():
    installation.update_pkgs()
    installation.install_pkgs(["xserver-xephyr", "plasma-desktop"])

    create_flown_shortcut()
    if check_file_presence("/usr/local/bin/start-flown"):
        if check_file_presence("/usr/local/bin/kill-flown"):
            console.info("Shortcut created!\n")
    else:
        console.alert("A problem occurred while creating the Flown launch shortcut.\n")

if __name__ == "__main__":  
    try:
        if check_root_access():
            if not give_root_auth("sudo python3 install.py"):
                console.error("The script has stopped due to insufficient privileges.")
                exit()
        console.clear()


        # Info screen!         
        print(f"""{TX_BLUE + "Flown KDE" + END}  🢝 1.0
Create your own ChromeOS Desktop.
""")
        input(f"Press {BG_WHITE + TX_BLACK + ' Enter ↲ ' + END} key to start the installation !\n")
        # Info screen!

        console.clear()
        main()

        console.success("""The installation of Flown is complete!
You can launch Flown you can type in the terminal 'start-flown' and to close it 'kill-flown'""")

    except Exception as a:
        console.error(f"""An error occurred while executing the program
More details: {a}""")
        input("Press enter to exit")