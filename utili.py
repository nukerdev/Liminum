import os, asyncio, threading
from rgbprint import gradient_scroll, Color
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor()

async def async_grab_process(guild, grab_function):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(executor, grab_function, guild)

def init():
    os.system("title Liminum (W3bh00k Gr4bb3r) - Made by nukerdev")

def print_to_console(message: str, type: str):
    gradient_scroll(
        f"[{type.upper()}] {message}",
        start_color=Color.purple,
        end_color=Color.medium_purple
    )

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_in_thread(message: str, type: str):
    thread = threading.Thread(target=print_to_console, args=(message, type))
    thread.start()
    return thread

printToConsole = print_to_console
clearConsole = clear_console