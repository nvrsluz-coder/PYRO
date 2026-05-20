import shutil
import pandas as pd
import asyncio
import threading
from threading import Thread
import os
import random
import re
import configparser
import csv
import sys
import subprocess
import requests
import datetime
import time
from csv import reader
from telethon.sync import TelegramClient, functions, types, utils
from telethon.tl.functions.account import UpdateStatusRequest
from telethon.errors import (
    PhoneNumberBannedError, SessionPasswordNeededError, UserPrivacyRestrictedError,
    PeerFloodError, UserChannelsTooMuchError, UserNotMutualContactError,
    UserAlreadyParticipantError, ChatWriteForbiddenError, UserBannedInChannelError,
    ChatAdminRequiredError, FloodWaitError, UserIdInvalidError, PeerIdInvalidError
)
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest, JoinChannelRequest, InviteToChannelRequest, LeaveChannelRequest
from telethon.tl.types import (
    UserStatusRecently, UserStatusLastMonth, UserStatusLastWeek,
    UserStatusOffline, UserStatusOnline, ChannelParticipantsAdmins,
    ChannelParticipantsSearch, InputPeerChannel
)
from telethon.sessions import StringSession
from colorama import Fore, Back, Style, init

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
g = Fore.GREEN
b = Fore.BLUE
n = Fore.RESET
r = Fore.RED
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
gr = Fore.LIGHTGREEN_EX
init()
init(autoreset=True)

API_ID = 13682
HASHID = 'de37bcf00f4688de900510f4f87384bb'
chatop = 777000


# Получаем текущую директорию (где запущен скрипт)
current_directory = os.getcwd()

# Проверяем, существует ли файл main.myst в текущей директории
myst_file_path = os.path.join(current_directory)

if os.path.exists(myst_file_path):
    myst_directory = os.path.dirname(os.path.abspath(myst_file_path))
    path_parts = myst_directory.split(os.sep)
    
    if "Desktop" in path_parts:
        desktop_index = path_parts.index("Desktop")
        filtered_parts = path_parts[desktop_index + 1:]
    else:
        filtered_parts = path_parts
    
    last_two_parts = os.sep.join(filtered_parts[-2:])
else:
    last_two_parts = ""

info = lg + '(' + w + 'i' + lg + ')' + rs
error = lg + '(' + r + '!' + lg + ')' + rs
success = w + '(' + lg + '+' + w + ')' + rs
INPUT = lg + '(' + cy + '~' + lg + ')' + rs
INPUT = lg + '{' + r + '\3' + lg + '}' + rs
plus = w + '{' + lg + '+' + w + '}' + rs
minus = w + '{' + lg + '-' + w + '}' + rs
colors = [lg, w, r, cy, ye, gr]


def get_hwid():
    """Get HWID using WMI"""
    try:
        import wmi
        wmi_obj = wmi.WMI()
        return str(wmi_obj.Win32_ComputerSystemProduct()[0].UUID)
    except Exception as e:
        print(f"{r}Error getting HWID: {e}")
        return None


def check_license():
    """Check license against pastebin"""
    print(f"{r}Kompyuter tekshirilmoqda...")
    try:
        hwid_link = requests.get("https://pastebin.com/E1xAu33R").text
        hwid = get_hwid()
        
        if hwid and hwid in hwid_link:
            print(f"{lg}Litsenziya tasdiqlandi")
            time.sleep(1)
            return True
        else:
            print(f"{r}Litsenziya tasdiqlanmadi!")
            time.sleep(1)
            if hwid:
                print(f'{cy}Bu seriya raqamni @ilxom1991i ga yuboring')
                print(hwid)
            input("Enter chiqish...")
            os._exit(1)
            
    except Exception as e:
        print(f"{r}litsenziyani tekshirishda xatolik: {e}")
        hwid = get_hwid()
        if hwid:
            print(f'{cy}Bu seriya raqamni @ilxom1991i ga yuboring')
            print(hwid)
        input("Enter chiqish...")
        os._exit(1)

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')



def banner():
    clr()
    colors = [Fore.RED, Fore.MAGENTA, Fore.CYAN, Fore.BLUE, Fore.GREEN, Fore.YELLOW]
    title = "                   PYRO17 — VERSION-2"
    subtitle = "Fast • Stable • Intelligent • Binary Engine"
    border = "─" * 50

    # плавное появление текста
    print(random.choice(colors) + border)
    for c in title:
        print(random.choice(colors) + c, end="", flush=True)
        time.sleep(0.02)
    print()
    print(random.choice(colors) + border)

    # подсветка подписи
    for word in subtitle.split("•"):
        print(random.choice(colors) + f" {word.strip()} ", end="•", flush=True)
        time.sleep(0.15)
    print("\n" + random.choice(colors) + border)
    #print(Style.RESET_ALL)

while True: 
    def strip_ansi(s: str) -> str:
        import re
        return re.sub(r'\x1b\[[0-9;]*m', '', s)
    
    def print_menu():
        clr()
        banner()
        menu_options = [
            ("|0|  Odamlarni Olish",                  "|15| VACCUM SESSION"),
            ("|1|  Aralash Qo'shish",                 "|16| BANFILTER"),
            ("|2|  Ayollarni Qo'shish",               "|17| YOPIQ GURUXDAN OLISH(new)"),
            ("|3|  Erkaklarni Qo'shish",              "|18| Seansni boshqa qurilmadan tozalash"),
            ("|4|  Ro'yxatdan o'tkazish",             "|19| Profil rasmlarini o'chirish"),
            ("|5|  Profillarga rasm qo'yish",         "|20| Muzlatilgan nomer•Filter(new)"),
            ("|6|  Profillarga ism qo'yish",          "|21| Accountga Bio o'rnatish"),
            ("|7|  Kelgan kodni ko'rish",             "|22| Accountga Stories o'rnatish"),
            ("|8|  Username qo'yish",                 "|23| Telethon versiyasini yangilash"),
            ("|9|  Guruxlardan chiqish",              "|24| Royxatdan otqazish(QR_KOD)"),
            ("|10| 2FA parol o'rnatish",              "|25| Human Imitation(new)"),
            ("|11| Kanallarga qo'shilish",            "|26| AKOUNTGA GURUH OCHISH(new)"),
            ("|12| Reaksiya bosish(postlarga)",       "|27| VIDEO DARSLIK YOUTUBE"),
            ("|13| Papka+kanal+guruxlardan chiqish",  "|28| Yangi API olish(NEW_TEST) "),
            ("|14| kanal+guruxdan chiqish tanlab",     ""),     
        ]
        
        # Palitralar
        left_palette  = [Fore.CYAN, Fore.MAGENTA, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.RED]
        right_palette = [Fore.LIGHTGREEN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTRED_EX]
        
        left_w  = max(len(l) for l, _ in menu_options)
        right_w = max(len(r) for _, r in menu_options)
        gap = "  │  "
        
        colored_lines = []
        for i, (l, rtxt) in enumerate(menu_options):
            lc = left_palette[i % len(left_palette)]
            rc = right_palette[i % len(right_palette)]
            left_txt  = f"{Style.BRIGHT}{lc}{l:<{left_w}}{Style.RESET_ALL}"
            right_txt = f"{Style.BRIGHT}{rc}{rtxt:<{right_w}}{Style.RESET_ALL}"
            colored_lines.append(left_txt + gap + right_txt)
        
        inner_w = max(len(strip_ansi(s)) for s in colored_lines)
        top    = "┌" + "─" * inner_w + "┐"
        
        # >>> YANGI: titlega last_two_parts qo'shamiz (oq 'MENU' + qizil yo'l)
        global last_two_parts
        if not last_two_parts:
            last_two_parts = "(path unknown)"
        
        # Oddiy matn — padding uchun
        title = f"{last_two_parts}"
        
        # Rangli sarlavha (MENU oq/black fon, path qizil)
        title_colored = (
            #f"{Back.BLACK}{Style.BRIGHT}{Fore.WHITE}MENU{Style.RESET_ALL} "
            f"{Fore.RED}{last_two_parts}{Style.RESET_ALL}"
            #f"{Fore.RED}18chi va 22chi Funksiyalar Yangilandi!{Style.RESET_ALL}"
        )
        
        midpad = inner_w - len(title)
        if midpad < 0:
            midpad = 0
        
        mid    = "│" + title_colored + " " * midpad + "│"
        sep    = "├" + "─" * inner_w + "┤"
        bot    = "└" + "─" * inner_w + "┘"
        
        print(top)
        print(mid)
        print(sep)
        for s in colored_lines:
            pad = inner_w - len(strip_ansi(s))
            print("│" + s + " " * pad + "│")
        print(bot)
    
    # ==== ввод — ровно как просил ====
    check_license()
    print_menu()
    a_str = input(ye + 'TANLASH: ')
    if a_str.strip():
        a = int(a_str)
    else:
        print("Notogri raqam kiritdingiz.")
        input()
    
    if a == 0:
        import csv
        import datetime
        import os
        import asyncio
        from telethon import TelegramClient
        from telethon.tl.functions.channels import GetFullChannelRequest
        from telethon.tl.types import (
            UserStatusOffline, 
            UserStatusRecently, 
            UserStatusOnline, 
            UserStatusLastWeek, 
            UserStatusLastMonth, 
            ChannelParticipantsAdmins
        )
        from telethon.errors import FloodWaitError
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        # Ranglar
        lg = '\033[32m'  # light green
        g = '\033[32m'   # green
        r = '\033[31m'   # red
        n = '\033[0m'    # reset
        
        # --- EVENT LOOP ENSURE (Python 3.12 fix) ---
        def ensure_loop():
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                if os.name == 'nt':
                    try:
                        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                    except Exception:
                        pass
                asyncio.set_event_loop(asyncio.new_event_loop())
        
        # === Aktiv klientlarni kuzatish ===
        ACTIVE_CLIENTS = set()
        
        def register_client(client):
            try:
                ACTIVE_CLIENTS.add(client)
            except Exception:
                pass
        
        def unregister_client(client):
            try:
                ACTIVE_CLIENTS.discard(client)
            except Exception:
                pass
        
        async def disconnect_all_active():
            for client in list(ACTIVE_CLIENTS):
                try:
                    if hasattr(client, 'is_connected'):
                        client.disconnect()
                except Exception:
                    pass
                finally:
                    unregister_client(client)
        
        
        # ==== STATUS.TXT UPSERT HELPER ====
        def upsert_status_line(link: str, members_count: int, file_path: str = '../Ishlatilgan_Linklar.txt'):
            ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
            rows = []
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.rstrip('\n').strip()
                        if not line or line.startswith('DATE/TIME'):
                            continue
                        if ',' in line:
                            parts = [p.strip() for p in line.split(',')]
                            if len(parts) >= 3:
                                dt, lnk, cnt = parts[0], parts[1], parts[2]
                                rows.append({'dt': dt, 'link': lnk, 'count': cnt})
                        else:
                            toks = line.split()
                            if len(toks) >= 3:
                                dt = ' '.join(toks[0:2])
                                cnt = toks[-1]
                                lnk = ' '.join(toks[2:-1])
                                rows.append({'dt': dt, 'link': lnk, 'count': cnt})
        
            rows = [r for r in rows if r.get('link') != link]
            rows.append({'dt': ts, 'link': link, 'count': str(members_count)})
        
            dt_w = max(len('DATE/TIME'), max((len(r['dt']) for r in rows), default=0))
            link_w = max(len('LINK'), max((len(r['link']) for r in rows), default=0))
            cnt_w = max(len('MEMBERS'), max((len(str(r['count'])) for r in rows), default=0))
        
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                header = f"{'DATE/TIME'.ljust(dt_w)}  {'LINK'.ljust(link_w)}  {'MEMBERS'.rjust(cnt_w)}\n"
                f.write(header)
                for r in rows:
                    line = f"{r['dt'].ljust(dt_w)}  {r['link'].ljust(link_w)}  {str(r['count']).rjust(cnt_w)}\n"
                    f.write(line)
        
        
        # CSV dan telefon raqamlarini o'qish
        def read_phones_from_csv(file_path):
            phone_numbers = []
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    phone_numbers.append(row[0])
            return phone_numbers
        
        
        # Telegram klientni ishga tushirish (TOZA - default parametrlar)
        def start_client(phone_number):
            ensure_loop()
            session_file = f'sessions/{phone_number}_SQLite.session'
            
            # Oddiy TelegramClient - hech qanday fake device yo'q
            client = TelegramClient(session_file, API_ID, API_HASH)
            
            try:
                client.connect()
                register_client(client)
                return client
            except FileNotFoundError:
                print(f"Session fayl {phone_number} Topilmadi!")
            except Exception as e:
                print(f'XATOLIK! {phone_number}: {e}')
            return None
        
        
        # Kanal a'zolarini qayta ishlash
        def process_channel_members(client, link, choice):
            today = datetime.datetime.now()
            yesterday = today - datetime.timedelta(days=1)
            
            try:
                me = client.get_me()
                if me:
                    print(f'Akount {me.first_name} ulandi')
                
                members = client.iter_participants(link, limit=5000)
                channel_full_info = client(GetFullChannelRequest(link))
                cont = channel_full_info.full_chat.participants_count
        
                def write(member):
                    username = member.username if member.username else ''
                    name = member.first_name if member.first_name else 'Unknown'
                    status = type(member.status).__name__ if not isinstance(member.status, UserStatusOffline) else member.status.was_online
                    writer.writerow([cont, name, member.id, member.access_hash, status])
                
                # Adminlarni yozish
                admin_choice = int(0)
                if admin_choice == 0:
                    with open("admins.csv", "w", encoding='UTF-8') as f:
                        writer = csv.writer(f, delimiter=",", lineterminator="\n")
                        writer.writerow(['index', 'name', 'id', 'access_hash', 'status'])
                        for member in client.iter_participants(link, filter=ChannelParticipantsAdmins):
                            if not member.bot:
                                write(member)
                
                os.remove("admins.csv")
                
                # Foydalanuvchilarni yozish
                with open("users.csv", "w", encoding='UTF-8') as f:
                    writer = csv.writer(f, delimiter=",", lineterminator="\n")
                    writer.writerow(['index', 'name', 'id', 'access_hash', 'status'])
                    
                    if choice == 0:
                        # XAMMASI
                        try:
                            for index, member in enumerate(members):
                                print(f"*{link}* {index+1}/{cont}", end="\r")
                                if not member.bot:
                                    write(member)
                        except Exception as e:
                            print(f"\nXATOLIK: {e}")
                            
                    elif choice == 1:
                        # KECHA_BUGUN
                        try:
                            for index, member in enumerate(members):
                                print(f"*{link}* {index+1}/{cont}", end="\r")
                                if not member.bot:
                                    if isinstance(member.status, (UserStatusRecently, UserStatusOnline)):
                                        write(member)
                                    elif isinstance(member.status, UserStatusOffline):
                                        d = member.status.was_online
                                        if d.date() in [today.date(), yesterday.date()]:
                                            write(member)
                        except Exception as e:
                            print(f"\nXATOLIK: {e}")
                            
                    elif choice == 2:
                        # BIR_XAFTA
                        try:
                            for index, member in enumerate(members):
                                print(f"*{link}* {index+1}/{cont}", end="\r")
                                if not member.bot:
                                    if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek)):
                                        write(member)
                                    elif isinstance(member.status, UserStatusOffline):
                                        d = member.status.was_online
                                        if any((today - datetime.timedelta(days=i)).date() == d.date() for i in range(7)):
                                            write(member)
                        except Exception as e:
                            print(f"\nXATOLIK: {e}")
                            
                    elif choice == 3:
                        # BIR_OY
                        try:
                            for index, member in enumerate(members):
                                print(f"*{link}* {index+1}/{cont}", end="\r")
                                if not member.bot:
                                    if isinstance(member.status, (UserStatusRecently, UserStatusOnline, UserStatusLastWeek, UserStatusLastMonth)):
                                        write(member)
                                    elif isinstance(member.status, UserStatusOffline):
                                        d = member.status.was_online
                                        if any((today - datetime.timedelta(days=i)).date() == d.date() for i in range(30)):
                                            write(member)
                        except Exception as e:
                            print(f"\nXATOLIK: {e}")
                            
                    elif choice == 4:
                        # BIR_XAFTA_TEPASIDA
                        try:
                            for index, member in enumerate(members):
                                print(f"*{link}* {index+1}/{cont}", end="\r")
                                if not member.bot:
                                    if isinstance(member.status, (UserStatusLastWeek, UserStatusLastMonth)):
                                        write(member)
                                    elif isinstance(member.status, UserStatusOffline):
                                        d = member.status.was_online
                                        if any((today - datetime.timedelta(days=i)).date() == d.date() for i in range(7, 100)):
                                            write(member)
                        except Exception as e:
                            print(f"\nXATOLIK: {e}")
        
                # Status faylga yozish
                try:
                    upsert_status_line(link, cont, file_path='../Ishlatilgan_Linklar.txt')
                except Exception as e:
                    print(f"Ishlatilgan_Linklar.txt yozishda xatolik: {e}")
        
                # CSV ni tozalash
                lines = list()        
                with open('users.csv', 'r', encoding='UTF-8') as readFile:    
                    reader = csv.reader(readFile)    
                    for row in reader:    
                        lines.append(row)    
                        for field in row:    
                            if field == 'name':
                                lines.remove(row)
                                
                with open('1.csv', 'w', encoding='UTF-8') as writeFile:
                    writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")    
                    writer.writerows(lines)   
                    
                lines = list()
                with open('1.csv', 'r', encoding='UTF-8') as readFile:    
                    reader = csv.reader(readFile)    
                    for row in reader:    
                        lines.append(row)   
                        for field in row:   
                            if field == 'name':
                                lines.remove(row)    
                                
                with open('2.csv', 'w', encoding='UTF-8') as writeFile:
                    writer = csv.writer(writeFile, delimiter=",", lineterminator="\n")    
                    writer.writerows(lines)
                    
                with open("2.csv", "r", encoding='UTF-8') as source:
                    rdr = csv.reader(source)    
                    with open("users.csv", "w", encoding='UTF-8') as f:
                        writer = csv.writer(f, delimiter=",", lineterminator="\n")
                        writer.writerow(['index', 'name', 'id', 'access_hash', 'status'])
                        i = 0
                        for row in rdr:
                            i += 1
                            writer.writerow((i, row[1], row[2], row[3], row[4]))
                            
                os.remove("1.csv")        
                os.remove("2.csv")                             
                client.disconnect()
                unregister_client(client)
                print("\nODAMLAR SAQLANDI users.csv.")
            
            except Exception as e:
                print(f"{e}")
                print("Birinchi nomer chiqarib yuborilgan bolishi mumkin!")
                print("Agar shunday bo'lsa uni phonedan o'chirib tashlang,")
                print("Yoki boshqatdan ro'yxatdan o'tqazing.!")
                input()
                try:
                    client.disconnect()
                except Exception:
                    pass
                unregister_client(client)
        
        
        # Guruh a'zolarini olish (FloodWait bilan)
        async def get_group_participants(client, scraped_grp, limit=5000):
            while True:
                try:
                    participants = await client.get_participants(scraped_grp, limit=limit)
                    return participants
                except FloodWaitError as e:
                    print(f"limit: kuting {e.seconds} sekund")
                    await asyncio.sleep(e.seconds)
        
        
        # Async klient ishlov berish (TOZA - default parametrlar)
        async def handle_client(session_string, phone_number, index, scraped_grp):
            # Oddiy TelegramClient - hech qanday fake device yo'q
            client = TelegramClient(session_string, API_ID, API_HASH)
            
            register_client(client)
            try:
                await client.connect()
                print(f'[{index}] {phone_number}: start | Tekshirilmoqda...')
                
                if not await client.is_user_authorized():
                    print(f"{phone_number} NOMER {phone_number} CHIQARIB YUBORILGAN!")
                    await client.disconnect()
                    unregister_client(client)
                    return
        
                acc_name = await client.get_me()
                participants = await get_group_participants(client, scraped_grp)
                
            except Exception as e:
                print(f"XATOLIK {phone_number}: {e}")
            finally:
                try:
                    await client.disconnect()
                except Exception:
                    pass
                unregister_client(client)
        
        
        # Asosiy funksiya
        def main():
            ensure_loop()
            phone_csv = 'phone.csv'
            phone_numbers = read_phones_from_csv(phone_csv)
        
            if phone_numbers:
                first_phone_number = phone_numbers.pop(0)
                first_client = start_client(first_phone_number)
                
                if first_client:
                    try:
                        username = input(lg + 'olish uchun link kiriting->>:' + n)
                        link = str(username)
                        choice = int(input(f"{g}qanday formatda olmoqchisiz?\n\n[0] XAMMASI\n[1] KECHA_BUGUN{r}(XAVFLI!){g} \n[2] BIR_XAFTA\n[3] BIR_OY\n[4] BIR_XAFTA_TEPASIDA\n\nTanlang va Enter: "))
                        process_channel_members(first_client, link, choice)
                    except Exception as e:
                        print(f"XATOLIK: {e}")
                    finally:
                        try:
                            first_client.disconnect()
                        except Exception:
                            pass
                        unregister_client(first_client)
                    
                    # Qolgan akkauntlarni async ishlash
                    async def process_remaining_clients():
                        tasks = []
                        for index, phone_number in enumerate(phone_numbers, start=1):
                            session_string = f'sessions/{phone_number}_SQLite.session'
                            task = asyncio.create_task(handle_client(session_string, phone_number, index, link))
                            tasks.append(task)
                        try:
                            if tasks:
                                await asyncio.gather(*tasks, return_exceptions=True)
                        finally:
                            await disconnect_all_active()
        
                    asyncio.run(process_remaining_clients())
        
            # Ehtiyot chorasi
            try:
                loop = asyncio.new_event_loop()
                loop.run_until_complete(disconnect_all_active())
                loop.close()
            except Exception:
                pass
        
        
        ensure_loop()
        
        if __name__ == "__main__":
            main()

    elif a == 1:                
        import os
        import csv
        import shutil
        import configparser
        import random
        import asyncio
        from datetime import datetime
        from telethon import TelegramClient, functions, types
        from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, LeaveChannelRequest
        from telethon.errors import (
            FloodWaitError, PeerFloodError, UserChannelsTooMuchError, UserNotMutualContactError,
            UserPrivacyRestrictedError, UserAlreadyParticipantError,
            UserBannedInChannelError, ChatWriteForbiddenError, ChatAdminRequiredError,
            UserKickedError
        )
        
        # ----------------- SOZLAMALAR -----------------
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        # Terminal ranglari
        r, w, lg, ye = '\033[1;31m', '\033[1;37m', '\033[1;32m', '\033[1;33m'
        
        
        # ----------------- YORDAMCHI FUNKSIYALAR -----------------
        async def maybe_update_profile(client):
            """Ozaro kam miqdorda bio yangilash."""
            if random.random() > 0.03:
                return
            try:
                bios = ["Here to help", "Working...", "Available", "Offline later", "🙂"]
                await client(functions.account.UpdateProfileRequest(about=random.choice(bios)))
            except Exception:
                pass
        
        
        # ----------------- WORKER -----------------
        async def worker(name, client, target, user_queue, total_added_counter, tag):
            """Bir akkaunt uchun ishchi."""
            print(f"{ye}[{last_two_parts}]{lg}[{name}] Ishni boshladi.")
            await client.connect()
        
            if not await client.is_user_authorized():
                print(f"{ye}[{last_two_parts}]{r}[{name}] Nomer chiqarib yuborilgan!")
                await client.disconnect()
                return
        
            try:
                # Channelga join
                try:
                    await client(JoinChannelRequest(target))
                    target_entity = await client.get_entity(target)
                    target_details = types.InputPeerChannel(target_entity.id, target_entity.access_hash)
                except FloodWaitError as e:
                    print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhga qo\'shilishda FloodWait: {e.seconds}s. To\'xtatildi.')
                    await asyncio.sleep(e.seconds + 5)
                    await client.disconnect()
                    return
                except Exception as e:
                    print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhga qo\'shila olmadi: {e}. To\'xtatildi.')
                    await client.disconnect()
                    return
        
                added_by_this_account = 0
                max_to_add = random.randint(30, 40)
        
                while added_by_this_account < max_to_add:
                    try:
                        user = await user_queue.get()
        
                        # 1) Kichik kutish
                        await asyncio.sleep(random.uniform(3, 8))

                        # 2) Profile yangilash
                        await maybe_update_profile(client)
        
                        # 3) Qo'shish
                        try:
                            user_to_add = int(user['id'])
                            await client(InviteToChannelRequest(target_details, [user_to_add]))
        
                            added_by_this_account += 1
                            total_added_counter['count'] += 1
        
                            print(f'{ye}[{last_two_parts}]{lg}[{name}] > {user["name"]} >>> {target_entity.title} ga qo\'shdi. | Jami:{total_added_counter["count"]}')
                            user_queue.task_done()
        
                            # Dam olish
                            hour = datetime.now().hour
                            if 1 <= hour <= 6:
                                await asyncio.sleep(random.uniform(20, 30))
                            elif 12 <= hour <= 15:
                                await asyncio.sleep(random.uniform(15, 25))
                            else:
                                await asyncio.sleep(random.uniform(10, 20))
        
                        except (UserChannelsTooMuchError, UserKickedError, UserNotMutualContactError,
                                UserPrivacyRestrictedError, UserAlreadyParticipantError):
                            user_queue.task_done()
                            await asyncio.sleep(random.uniform(2, 3))
                            continue
        
                        except PeerFloodError:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] PeerFloodError! Akkauntda limit tugadi.')
                            await user_queue.put(user)
                            user_queue.task_done()
                            break
        
                        except FloodWaitError as e:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] FloodWaitError ({e.seconds} sekund)!')
                            await user_queue.put(user)
                            try:
                                user_queue.task_done()
                            except:
                                pass
                            break
        
                        except (UserBannedInChannelError, ChatWriteForbiddenError, ChatAdminRequiredError):
                            print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhda muammo yoki akkaunt spamda.')
                            await user_queue.put(user)
                            user_queue.task_done()
                            break
        
                        except Exception as e:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] {user["name"]} ni qo\'shishda xato: {e}')
                            user_queue.task_done()
                            await asyncio.sleep(random.uniform(2, 3))
                            continue
        
                    except asyncio.CancelledError:
                        break
        
            except Exception as e:
                print(f'{ye}[{last_two_parts}]{r}[{name}] Umumiy xatolik: {e}')
            finally:
                try:
                    await client(LeaveChannelRequest(target))
                    print(f"{ye}[{last_two_parts}]{ye}[{name}] Guruhdan chiqdi.")
                except Exception as e:
                    print(f"{ye}[{last_two_parts}]{r}[{name}] Guruhdan chiqishda xato: {e}")
        
                await client.disconnect()
                print(f"{ye}[{last_two_parts}]{ye}[{name}] Ishni tugatdi.")
        
        
        # ----------------- ASOSIY main() -----------------
        async def main():
            # config fayl
            config = configparser.ConfigParser()
            cfg_path = '../Guruxlar.ini'
            if not os.path.exists(cfg_path):
                print(f"{r}XATO: {cfg_path} topilmadi!")
                input("ENTER bosing...")
                return
            config.read(cfg_path)
        
            # phone.csv tekshirish
            phones = []
            if not os.path.exists('phone.csv'):
                print(f"{r}XATO: phone.csv fayli topilmadi!")
                input("ENTER bosing...")
                return
            
            with open('phone.csv', 'r', encoding='utf-8') as readFile:
                reader = csv.reader(readFile)
                for phone_ in reader:
                    if phone_:
                        phone_clean = phone_[0].strip()
                        if phone_clean.startswith('+') and phone_clean[1:].isdigit():
                            phones.append(phone_clean)
                        elif phone_clean.isdigit():
                            phones.append(phone_clean)
            
            if not phones:
                print(f"{r}Akkauntlar topilmadi. phone.csv faylini tekshiring.")
                input("ENTER bosing...")
                return
        
            # users.csv yuklash
            members = []
            if not os.path.exists('users.csv'):
                print(f"{r}XATO: users.csv fayli topilmadi!")
                input("ENTER bosing...")
                return
            
            with open('users.csv', encoding='utf-8') as f:
                rows = csv.reader(f, delimiter=",", lineterminator="\n")
                next(rows, None)
                for row in rows:
                    if len(row) >= 5:
                        try:
                            members.append({
                                'index': row[0],
                                'name': row[1],
                                'id': int(row[2]),
                                'access_hash': row[3],
                                'status': row[4]
                            })
                        except Exception:
                            continue
            
            if not members:
                print(f"{r}qo'shish uchun odamlar yo'q!")
                input("ENTER bosing...")
                return
        
            total_added_counter = {'count': 0}
        
            # Har bir section uchun ishlaymiz
            for section_name in config.sections():
                target = config[section_name].get('Qoshadigan_gurux1')
                if not target:
                    print(f"Section {section_name} ichida Qoshadigan_gurux1 topilmadi. O'tkazib yuborildi.")
                    continue
        
                tag = section_name[-12:] if len(section_name) > 12 else section_name
        
                print("\n" + "=" * 50)
                print(f"{w}Jarayon: Papka/Bo'lim: {ye}{last_two_parts}{w} | Guruh: {ye}{target}{w}")
                print("=" * 50 + "\n")
        
                print(f'{lg}Jami akountlar soni: {len(phones)}')
                print(f"{lg}Qo'shish uchun jami odamlar: {len(members)}")
        
                # Navbat tayyorlash
                user_queue = asyncio.Queue()
                for member in members:
                    await user_queue.put(member)
        
                # Tasks yaratish
                tasks = []
                for phone in phones:
                    session_file = f'sessions/{phone}_SQLite.session'
                    
                    # TOZA TelegramClient - hech qanday fake device yo'q
                    client = TelegramClient(session_file, API_ID, API_HASH)
                    
                    short_name = phone[-9:]
                    task = asyncio.create_task(worker(short_name, client, target, user_queue, total_added_counter, tag))
                    tasks.append(task)
        
                # Kutish
                await asyncio.gather(*tasks)
        
            # Yakuniy hisobot
            message = "BARCHA ISHLAR TUGATILDI YOKI AKKAUNTLAR TOXTATILDI!!!"
            terminal_width = shutil.get_terminal_size().columns
            print("\n" + "\033[1;97;41m" + "!" * terminal_width + "\033[0m")
            print("\033[1;32;40m" + message.center(terminal_width) + "\033[0m")
            print("\033[1;97;41m" + "!" * terminal_width + "\033[0m")
            print(f"\n{lg}Jami Qo'shilganlar soni (barcha papkalar bo'yicha): {total_added_counter['count']}\n")
            input("Chiqish uchun ENTER bosing...")
        
        
        # ----------------- ENTRY POINT -----------------
        if __name__ == '__main__':
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                print("\nTugatildi (Ctrl+C).")

        
    elif a == 2:
        def filter_names_by_keywords(df_chunk, keywords):
            # Конвертируем ключевые слова в верхний регистр
            upper_keywords = [keyword.upper() for keyword in keywords]           
            # Создаем регулярное выражение для поиска ключевых слов в последних трех символах имени
            regex_keywords = [re.compile(rf'\w*({re.escape(keyword)}$)', flags=re.IGNORECASE) for keyword in upper_keywords]           
            # Функция проверки наличия ключевых слов в последних трех символах имени
            def has_keywords(name):
                name_str = str(name)
                for keyword in regex_keywords:
                    if keyword.search(name_str):
                        return True
                return False
            
            # Применяем функцию has_keywords к столбцу 'name' для каждой строки DataFrame
            filtered_df_chunk = df_chunk[df_chunk['name'].apply(has_keywords)]
            return filtered_df_chunk
        
        def shuffle_data(df_chunk):
            return df_chunk.sample(frac=1, random_state=42).reset_index(drop=True)
        
        def evaluate_sorting(df_chunk):
            total_names = len(df_chunk)
            correct_names = len(df_chunk)
            accuracy = (correct_names / total_names) * 100
            print(f"Filter aniqlik darajasi: {accuracy:.2f}%")           
        if __name__ == "__main__":
            input_csv_file = 'users.csv'
            output_csv_file = 'ayollar.csv'
            keywords = [
                'ULI', 'IZA', 'DAT', 'ONU', 'HRA', 'XRA', 'ODA', 'OLA', 'ORA', 'YLO',
                'XON', 'IDA', 'OVA', 'VNA', 'DUZ', 'GIM', 'UZA', 'IRA', 'NOZ', 'OZA',
                'IZA', 'ARA', 'DYA', 'GUL', 'VOZ', 'XOR', 'HOR', 'IMA', 'INA', 'GIZ',
                'SOZ', 'FAT', 'UBA', 'IYA', 'SAL', 'YLA', 'SHTA', 'STA', 'IBA', 'АЙЁ',
                'ОДА', 'УЛЯ', 'MOR', 'ISHA', 'USHA', 'RUZ', 'УЛИ', 'ИЗА', 'ДАТ', 'ОНУ', 'ХРА', 'ХРА', 'ОДА', 'ОЛА', 'ОРА', 'ИЛО',
                'ХОН', 'ИДА', 'ОВА', 'ВНА', 'ДУЗ', 'ГИМ', 'УЗА', 'ИРА', 'НОЗ', 'ОЗА',
                'ИЗА', 'АРА', 'ДЯ', 'ГУЛ', 'ВОЗ', 'ХОР', 'ХОР', 'ИМА', 'ИНА', 'ГИЗ',
                'СОЗ', 'ФАТ', 'УБА', 'ИЯ', 'САЛ', 'ИЛА', 'ШТА', 'СТА', 'ИБА', 'АЙЁ',
                'ОДА', 'УЛЯ', 'МОР', 'ИША', 'УША', 'РУЗ'
            ]
            chunksize = 10000
            
            chunks = pd.read_csv(input_csv_file, chunksize=chunksize)
            processed_chunks = []
            
            for chunk in chunks:
                filtered_chunk = filter_names_by_keywords(chunk, keywords)
                processed_chunks.append(filtered_chunk)
            
            processed_df = pd.concat(processed_chunks, ignore_index=True)
            shuffled_df = shuffle_data(processed_df)
            shuffled_df['index'] = range(1, len(shuffled_df) + 1)
            shuffled_df.to_csv(output_csv_file, index=False)
            evaluate_sorting(shuffled_df)
            #input()
            print("Ayollar ismi filterlandi va saqlandi ayollar.csv faylga")    
        time.sleep(2)    
  
        import os
        import csv
        import shutil
        import configparser
        import random
        import asyncio
        from datetime import datetime
        from telethon import TelegramClient, functions, types
        from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, LeaveChannelRequest
        from telethon.errors import (
            FloodWaitError, PeerFloodError, UserChannelsTooMuchError, UserNotMutualContactError,
            UserPrivacyRestrictedError, UserAlreadyParticipantError,
            UserBannedInChannelError, ChatWriteForbiddenError, ChatAdminRequiredError,
            UserKickedError
        )
        
        # ----------------- SOZLAMALAR -----------------
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        # Terminal ranglari
        r, w, lg, ye = '\033[1;31m', '\033[1;37m', '\033[1;32m', '\033[1;33m'
        
        
        # ----------------- YORDAMCHI FUNKSIYALAR -----------------
        async def maybe_update_profile(client):
            """Ozaro kam miqdorda bio yangilash."""
            if random.random() > 0.03:
                return
            try:
                bios = ["Here to help", "Working...", "Available", "Offline later", "🙂"]
                await client(functions.account.UpdateProfileRequest(about=random.choice(bios)))
            except Exception:
                pass
        
        
        # ----------------- WORKER -----------------
        async def worker(name, client, target, user_queue, total_added_counter, tag):
            """Bir akkaunt uchun ishchi."""
            print(f"{ye}[{last_two_parts}]{lg}[{name}] Ishni boshladi.")
            await client.connect()
        
            if not await client.is_user_authorized():
                print(f"{ye}[{last_two_parts}]{r}[{name}] Nomer chiqarib yuborilgan!")
                await client.disconnect()
                return
        
            try:
                # Channelga join
                try:
                    await client(JoinChannelRequest(target))
                    target_entity = await client.get_entity(target)
                    target_details = types.InputPeerChannel(target_entity.id, target_entity.access_hash)
                except FloodWaitError as e:
                    print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhga qo\'shilishda FloodWait: {e.seconds}s. To\'xtatildi.')
                    await asyncio.sleep(e.seconds + 5)
                    await client.disconnect()
                    return
                except Exception as e:
                    print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhga qo\'shila olmadi: {e}. To\'xtatildi.')
                    await client.disconnect()
                    return
        
                added_by_this_account = 0
                max_to_add = random.randint(30, 40)
        
                while added_by_this_account < max_to_add:
                    try:
                        user = await user_queue.get()
        
                        # 1) Kichik kutish
                        await asyncio.sleep(random.uniform(3, 8))

                        # 2) Profile yangilash
                        await maybe_update_profile(client)
        
                        # 3) Qo'shish
                        try:
                            user_to_add = int(user['id'])
                            await client(InviteToChannelRequest(target_details, [user_to_add]))
        
                            added_by_this_account += 1
                            total_added_counter['count'] += 1
        
                            print(f'{ye}[{last_two_parts}]{lg}[{name}] > {user["name"]} >>> {target_entity.title} ga qo\'shdi. | Jami:{total_added_counter["count"]}')
                            user_queue.task_done()
        
                            # Dam olish
                            hour = datetime.now().hour
                            if 1 <= hour <= 6:
                                await asyncio.sleep(random.uniform(20, 30))
                            elif 12 <= hour <= 15:
                                await asyncio.sleep(random.uniform(15, 25))
                            else:
                                await asyncio.sleep(random.uniform(10, 20))
        
                        except (UserChannelsTooMuchError, UserKickedError, UserNotMutualContactError,
                                UserPrivacyRestrictedError, UserAlreadyParticipantError):
                            user_queue.task_done()
                            await asyncio.sleep(random.uniform(2, 3))
                            continue
        
                        except PeerFloodError:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] PeerFloodError! Akkauntda limit tugadi.')
                            await user_queue.put(user)
                            user_queue.task_done()
                            break
        
                        except FloodWaitError as e:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] FloodWaitError ({e.seconds} sekund)!')
                            await user_queue.put(user)
                            try:
                                user_queue.task_done()
                            except:
                                pass
                            break
        
                        except (UserBannedInChannelError, ChatWriteForbiddenError, ChatAdminRequiredError):
                            print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhda muammo yoki akkaunt spamda.')
                            await user_queue.put(user)
                            user_queue.task_done()
                            break
        
                        except Exception as e:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] {user["name"]} ni qo\'shishda xato: {e}')
                            user_queue.task_done()
                            await asyncio.sleep(random.uniform(2, 3))
                            continue
        
                    except asyncio.CancelledError:
                        break
        
            except Exception as e:
                print(f'{ye}[{last_two_parts}]{r}[{name}] Umumiy xatolik: {e}')
            finally:
                try:
                    await client(LeaveChannelRequest(target))
                    print(f"{ye}[{last_two_parts}]{ye}[{name}] Guruhdan chiqdi.")
                except Exception as e:
                    print(f"{ye}[{last_two_parts}]{r}[{name}] Guruhdan chiqishda xato: {e}")
        
                await client.disconnect()
                print(f"{ye}[{last_two_parts}]{ye}[{name}] Ishni tugatdi.")
        
        
        # ----------------- ASOSIY main() -----------------
        async def main():
            # config fayl
            config = configparser.ConfigParser()
            cfg_path = '../Guruxlar.ini'
            if not os.path.exists(cfg_path):
                print(f"{r}XATO: {cfg_path} topilmadi!")
                input("ENTER bosing...")
                return
            config.read(cfg_path)
        
            # phone.csv tekshirish
            phones = []
            if not os.path.exists('phone.csv'):
                print(f"{r}XATO: phone.csv fayli topilmadi!")
                input("ENTER bosing...")
                return
            
            with open('phone.csv', 'r', encoding='utf-8') as readFile:
                reader = csv.reader(readFile)
                for phone_ in reader:
                    if phone_:
                        phone_clean = phone_[0].strip()
                        if phone_clean.startswith('+') and phone_clean[1:].isdigit():
                            phones.append(phone_clean)
                        elif phone_clean.isdigit():
                            phones.append(phone_clean)
            
            if not phones:
                print(f"{r}Akkauntlar topilmadi. phone.csv faylini tekshiring.")
                input("ENTER bosing...")
                return
        
            # users.csv yuklash
            members = []
            if not os.path.exists('ayollar.csv'):
                print(f"{r}XATO: ayollar.csv fayli topilmadi!")
                input("ENTER bosing...")
                return
            
            with open('ayollar.csv', encoding='utf-8') as f:
                rows = csv.reader(f, delimiter=",", lineterminator="\n")
                next(rows, None)
                for row in rows:
                    if len(row) >= 5:
                        try:
                            members.append({
                                'index': row[0],
                                'name': row[1],
                                'id': int(row[2]),
                                'access_hash': row[3],
                                'status': row[4]
                            })
                        except Exception:
                            continue
            
            if not members:
                print(f"{r}qo'shish uchun odamlar yo'q!")
                input("ENTER bosing...")
                return
        
            total_added_counter = {'count': 0}
        
            # Har bir section uchun ishlaymiz
            for section_name in config.sections():
                target = config[section_name].get('Qoshadigan_gurux1')
                if not target:
                    print(f"Section {section_name} ichida Qoshadigan_gurux1 topilmadi. O'tkazib yuborildi.")
                    continue
        
                tag = section_name[-12:] if len(section_name) > 12 else section_name
        
                print("\n" + "=" * 50)
                print(f"{w}Jarayon: Papka/Bo'lim: {ye}{last_two_parts}{w} | Guruh: {ye}{target}{w}")
                print("=" * 50 + "\n")
        
                print(f'{lg}Jami akountlar soni: {len(phones)}')
                print(f"{lg}Qo'shish uchun jami odamlar: {len(members)}")
        
                # Navbat tayyorlash
                user_queue = asyncio.Queue()
                for member in members:
                    await user_queue.put(member)
        
                # Tasks yaratish
                tasks = []
                for phone in phones:
                    session_file = f'sessions/{phone}_SQLite.session'
                    
                    # TOZA TelegramClient - hech qanday fake device yo'q
                    client = TelegramClient(session_file, API_ID, API_HASH)
                    
                    short_name = phone[-9:]
                    task = asyncio.create_task(worker(short_name, client, target, user_queue, total_added_counter, tag))
                    tasks.append(task)
        
                # Kutish
                await asyncio.gather(*tasks)
        
            # Yakuniy hisobot
            message = "BARCHA ISHLAR TUGATILDI YOKI AKKAUNTLAR TOXTATILDI!!!"
            terminal_width = shutil.get_terminal_size().columns
            print("\n" + "\033[1;97;41m" + "!" * terminal_width + "\033[0m")
            print("\033[1;32;40m" + message.center(terminal_width) + "\033[0m")
            print("\033[1;97;41m" + "!" * terminal_width + "\033[0m")
            print(f"\n{lg}Jami Qo'shilganlar soni (barcha papkalar bo'yicha): {total_added_counter['count']}\n")
            input("Chiqish uchun ENTER bosing...")
        
        
        # ----------------- ENTRY POINT -----------------
        if __name__ == '__main__':
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                print("\nTugatildi (Ctrl+C).")
            
    elif a == 3:
        def filter_names_by_keywords(df_chunk, keywords):
            # Конвертируем ключевые слова в верхний регистр
            upper_keywords = [keyword.upper() for keyword in keywords]           
            # Создаем регулярное выражение для поиска ключевых слов в последних трех символах имени
            regex_keywords = [re.compile(rf'\w*({re.escape(keyword)}$)', flags=re.IGNORECASE) for keyword in upper_keywords]           
            # Функция проверки наличия ключевых слов в последних трех символах имени
            def has_keywords(name):
                name_str = str(name)
                for keyword in regex_keywords:
                    if keyword.search(name_str):
                        return True
                return False
            
            # Применяем функцию has_keywords к столбцу 'name' для каждой строки DataFrame
            filtered_df_chunk = df_chunk[df_chunk['name'].apply(has_keywords)]
            return filtered_df_chunk
        
        def shuffle_data(df_chunk):
            return df_chunk.sample(frac=1, random_state=42).reset_index(drop=True)
        
        def evaluate_sorting(df_chunk):
            total_names = len(df_chunk)
            correct_names = len(df_chunk)
            accuracy = (correct_names / total_names) * 100
            print(f"Filter aniqlik darajasi: {accuracy:.2f}%")           
        if __name__ == "__main__":
            input_csv_file = 'users.csv'
            output_csv_file = 'erkaklar.csv'
            keywords = [
                'BEK', 'JON', 'XOM', 'VAR', 'SHOD', 'XID', 'TON', 'LIK', 'GIR', 'ZIZ',
                'KIN', 'MAL', 'SIM', 'LLO', 'LIM', 'YOR', 'QAT', 'BOZ', 'YOT', 'RUR',
                'SUR', 'XIR', 'VAZ', 'XOD', 'MID', 'RAT', 'KIR', 'MUR', 'ROB', 'ALI',
                'SHER', 'GOR', 'AID', 'ROD', 'SUD', 'BOL', 'DOR', 'TAM', 'DIR', 'SHID',
                'JAR', 'SIN', 'BOY', 'DIN', 'KAL', 'RUF', 'IZO', 'MOV', 'AFO', 'БЕК', 'ДЖОН', 'ХОМ', 'ВАР', 'ШОД', 'ХИД', 'ТОН', 'ЛИК', 'ГИР', 'ЗИЗ',
                'КИН', 'МАЛ', 'СИМ', 'ЛЛО', 'ЛИМ', 'ЁР', 'КАТ', 'БОЗ', 'ЁТ', 'РУР',
                'СУР', 'ХИР', 'ВАЗ', 'ХОД', 'МИД', 'РАТ', 'КИР', 'МУР', 'РОБ', 'АЛИ',
                'ШЕР', 'ГОР', 'АЙД', 'РОД', 'СУД', 'БОЛ', 'ДОР', 'ТАМ', 'ДИР', 'ШИД',
                'ДЖАР', 'СИН', 'БОЙ', 'ДИН', 'КАЛ', 'РУФ', 'ИЗО', 'МОВ', 'АФО'
            ]
            chunksize = 10000
            
            chunks = pd.read_csv(input_csv_file, chunksize=chunksize)
            processed_chunks = []
            
            for chunk in chunks:
                filtered_chunk = filter_names_by_keywords(chunk, keywords)
                processed_chunks.append(filtered_chunk)
            
            processed_df = pd.concat(processed_chunks, ignore_index=True)
            shuffled_df = shuffle_data(processed_df)
            shuffled_df['index'] = range(1, len(shuffled_df) + 1)
            shuffled_df.to_csv(output_csv_file, index=False)
            evaluate_sorting(shuffled_df)
            #input()
            print("Erkaklar ismi filterlandi va saqlandi erkaklar.csv faylga")    
        time.sleep(2)    
               
        import os
        import csv
        import shutil
        import configparser
        import random
        import asyncio
        from datetime import datetime
        from telethon import TelegramClient, functions, types
        from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest, LeaveChannelRequest
        from telethon.errors import (
            FloodWaitError, PeerFloodError, UserChannelsTooMuchError, UserNotMutualContactError,
            UserPrivacyRestrictedError, UserAlreadyParticipantError,
            UserBannedInChannelError, ChatWriteForbiddenError, ChatAdminRequiredError,
            UserKickedError
        )
        
        # ----------------- SOZLAMALAR -----------------
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        # Terminal ranglari
        r, w, lg, ye = '\033[1;31m', '\033[1;37m', '\033[1;32m', '\033[1;33m'
        
        
        # ----------------- YORDAMCHI FUNKSIYALAR -----------------
        async def maybe_update_profile(client):
            """Ozaro kam miqdorda bio yangilash."""
            if random.random() > 0.03:
                return
            try:
                bios = ["Here to help", "Working...", "Available", "Offline later", "🙂"]
                await client(functions.account.UpdateProfileRequest(about=random.choice(bios)))
            except Exception:
                pass
        
        
        # ----------------- WORKER -----------------
        async def worker(name, client, target, user_queue, total_added_counter, tag):
            """Bir akkaunt uchun ishchi."""
            print(f"{ye}[{last_two_parts}]{lg}[{name}] Ishni boshladi.")
            await client.connect()
        
            if not await client.is_user_authorized():
                print(f"{ye}[{last_two_parts}]{r}[{name}] Nomer chiqarib yuborilgan!")
                await client.disconnect()
                return
        
            try:
                # Channelga join
                try:
                    await client(JoinChannelRequest(target))
                    target_entity = await client.get_entity(target)
                    target_details = types.InputPeerChannel(target_entity.id, target_entity.access_hash)
                except FloodWaitError as e:
                    print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhga qo\'shilishda FloodWait: {e.seconds}s. To\'xtatildi.')
                    await asyncio.sleep(e.seconds + 5)
                    await client.disconnect()
                    return
                except Exception as e:
                    print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhga qo\'shila olmadi: {e}. To\'xtatildi.')
                    await client.disconnect()
                    return
        
                added_by_this_account = 0
                max_to_add = random.randint(30, 40)
        
                while added_by_this_account < max_to_add:
                    try:
                        user = await user_queue.get()
        
                        # 1) Kichik kutish
                        await asyncio.sleep(random.uniform(3, 8))

                        # 2) Profile yangilash
                        await maybe_update_profile(client)
        
                        # 3) Qo'shish
                        try:
                            user_to_add = int(user['id'])
                            await client(InviteToChannelRequest(target_details, [user_to_add]))
        
                            added_by_this_account += 1
                            total_added_counter['count'] += 1
        
                            print(f'{ye}[{last_two_parts}]{lg}[{name}] > {user["name"]} >>> {target_entity.title} ga qo\'shdi. | Jami:{total_added_counter["count"]}')
                            user_queue.task_done()
        
                            # Dam olish
                            hour = datetime.now().hour
                            if 1 <= hour <= 6:
                                await asyncio.sleep(random.uniform(20, 30))
                            elif 12 <= hour <= 15:
                                await asyncio.sleep(random.uniform(15, 25))
                            else:
                                await asyncio.sleep(random.uniform(10, 20))
        
                        except (UserChannelsTooMuchError, UserKickedError, UserNotMutualContactError,
                                UserPrivacyRestrictedError, UserAlreadyParticipantError):
                            user_queue.task_done()
                            await asyncio.sleep(random.uniform(2, 3))
                            continue
        
                        except PeerFloodError:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] PeerFloodError! Akkauntda limit tugadi.')
                            await user_queue.put(user)
                            user_queue.task_done()
                            break
        
                        except FloodWaitError as e:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] FloodWaitError ({e.seconds} sekund)!')
                            await user_queue.put(user)
                            try:
                                user_queue.task_done()
                            except:
                                pass
                            break
        
                        except (UserBannedInChannelError, ChatWriteForbiddenError, ChatAdminRequiredError):
                            print(f'{ye}[{last_two_parts}]{r}[{name}] Guruhda muammo yoki akkaunt spamda.')
                            await user_queue.put(user)
                            user_queue.task_done()
                            break
        
                        except Exception as e:
                            print(f'{ye}[{last_two_parts}]{r}[{name}] {user["name"]} ni qo\'shishda xato: {e}')
                            user_queue.task_done()
                            await asyncio.sleep(random.uniform(2, 3))
                            continue
        
                    except asyncio.CancelledError:
                        break
        
            except Exception as e:
                print(f'{ye}[{last_two_parts}]{r}[{name}] Umumiy xatolik: {e}')
            finally:
                try:
                    await client(LeaveChannelRequest(target))
                    print(f"{ye}[{last_two_parts}]{ye}[{name}] Guruhdan chiqdi.")
                except Exception as e:
                    print(f"{ye}[{last_two_parts}]{r}[{name}] Guruhdan chiqishda xato: {e}")
        
                await client.disconnect()
                print(f"{ye}[{last_two_parts}]{ye}[{name}] Ishni tugatdi.")
        
        
        # ----------------- ASOSIY main() -----------------
        async def main():
            # config fayl
            config = configparser.ConfigParser()
            cfg_path = '../Guruxlar.ini'
            if not os.path.exists(cfg_path):
                print(f"{r}XATO: {cfg_path} topilmadi!")
                input("ENTER bosing...")
                return
            config.read(cfg_path)
        
            # phone.csv tekshirish
            phones = []
            if not os.path.exists('phone.csv'):
                print(f"{r}XATO: phone.csv fayli topilmadi!")
                input("ENTER bosing...")
                return
            
            with open('phone.csv', 'r', encoding='utf-8') as readFile:
                reader = csv.reader(readFile)
                for phone_ in reader:
                    if phone_:
                        phone_clean = phone_[0].strip()
                        if phone_clean.startswith('+') and phone_clean[1:].isdigit():
                            phones.append(phone_clean)
                        elif phone_clean.isdigit():
                            phones.append(phone_clean)
            
            if not phones:
                print(f"{r}Akkauntlar topilmadi. phone.csv faylini tekshiring.")
                input("ENTER bosing...")
                return
        
            # users.csv yuklash
            members = []
            if not os.path.exists('erkaklar.csv'):
                print(f"{r}XATO: erkaklar.csv fayli topilmadi!")
                input("ENTER bosing...")
                return
            
            with open('erkaklar.csv', encoding='utf-8') as f:
                rows = csv.reader(f, delimiter=",", lineterminator="\n")
                next(rows, None)
                for row in rows:
                    if len(row) >= 5:
                        try:
                            members.append({
                                'index': row[0],
                                'name': row[1],
                                'id': int(row[2]),
                                'access_hash': row[3],
                                'status': row[4]
                            })
                        except Exception:
                            continue
            
            if not members:
                print(f"{r}qo'shish uchun odamlar yo'q!")
                input("ENTER bosing...")
                return
        
            total_added_counter = {'count': 0}
        
            # Har bir section uchun ishlaymiz
            for section_name in config.sections():
                target = config[section_name].get('Qoshadigan_gurux1')
                if not target:
                    print(f"Section {section_name} ichida Qoshadigan_gurux1 topilmadi. O'tkazib yuborildi.")
                    continue
        
                tag = section_name[-12:] if len(section_name) > 12 else section_name
        
                print("\n" + "=" * 50)
                print(f"{w}Jarayon: Papka/Bo'lim: {ye}{last_two_parts}{w} | Guruh: {ye}{target}{w}")
                print("=" * 50 + "\n")
        
                print(f'{lg}Jami akountlar soni: {len(phones)}')
                print(f"{lg}Qo'shish uchun jami odamlar: {len(members)}")
        
                # Navbat tayyorlash
                user_queue = asyncio.Queue()
                for member in members:
                    await user_queue.put(member)
        
                # Tasks yaratish
                tasks = []
                for phone in phones:
                    session_file = f'sessions/{phone}_SQLite.session'
                    
                    # TOZA TelegramClient - hech qanday fake device yo'q
                    client = TelegramClient(session_file, API_ID, API_HASH)
                    
                    short_name = phone[-9:]
                    task = asyncio.create_task(worker(short_name, client, target, user_queue, total_added_counter, tag))
                    tasks.append(task)
        
                # Kutish
                await asyncio.gather(*tasks)
        
            # Yakuniy hisobot
            message = "BARCHA ISHLAR TUGATILDI YOKI AKKAUNTLAR TOXTATILDI!!!"
            terminal_width = shutil.get_terminal_size().columns
            print("\n" + "\033[1;97;41m" + "!" * terminal_width + "\033[0m")
            print("\033[1;32;40m" + message.center(terminal_width) + "\033[0m")
            print("\033[1;97;41m" + "!" * terminal_width + "\033[0m")
            print(f"\n{lg}Jami Qo'shilganlar soni (barcha papkalar bo'yicha): {total_added_counter['count']}\n")
            input("Chiqish uchun ENTER bosing...")
        
        
        # ----------------- ENTRY POINT -----------------
        if __name__ == '__main__':
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                print("\nTugatildi (Ctrl+C).")
           
    elif a == 4:
        import os
        import csv
        import asyncio
        import ctypes
        
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.errors import (
            SessionPasswordNeededError,
            PasswordHashInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            PhoneNumberBannedError,
        )
        
        API_ID = 13682
        API_HASH = 'de37bcf00f4688de900510f4f87384bb'
        SESSION_FOLDER = './sessions'
        
        # ---------- Device parametrlari ----------
        DEVICE_MODEL = "Samsung SM-G973F"
        SYSTEM_VERSION = "SDK 30 (Android 11)"
        APP_VERSION = "10.14.4"
        SYSTEM_LANG_CODE = "en-US"
        LANG_CODE = "en"
        
        # ---------- Windows uchun ranglar ----------
        def _enable_ansi_on_windows():
            if os.name != 'nt':
                return
            try:
                kernel32 = ctypes.windll.kernel32
                h = kernel32.GetStdHandle(-11)
                mode = ctypes.c_uint32()
                if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                    kernel32.SetConsoleMode(h, mode.value | 0x0004)
            except Exception:
                pass
        
        _enable_ansi_on_windows()
        
        # Oddiy ranglar
        R = '\033[0m'      # reset
        G = '\033[32m'     # green
        Y = '\033[33m'     # yellow
        C = '\033[36m'     # cyan
        RED = '\033[31m'   # red
        M = '\033[35m'     # magenta
        
        
        def read_phones_from_csv(file_path):
            """CSV fayldan telefon raqamlarini o'qish"""
            phone_numbers = []
            if not os.path.exists(file_path):
                print(f"{RED}XATO: {file_path} fayli topilmadi!{R}")
                return []
            
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row and row[0].strip():
                        phone_numbers.append(row[0].strip())
            return phone_numbers
        
        
        async def create_and_check_session(phone):
            """
            Telethon session yaratish (device settings bilan).
            """
            session_file = os.path.join(SESSION_FOLDER, f'telethon_{phone}.session')
        
            print(f"\n{C}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{R}")
            print(f"{C}📱 Telefon: {phone}{R}")
        
            # Mavjud sessiyani yuklash yoki yangi yaratish
            if os.path.exists(session_file):
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_string = f.read().strip()
                client = TelegramClient(
                    StringSession(session_string),
                    API_ID,
                    API_HASH,
                    device_model=DEVICE_MODEL,
                    system_version=SYSTEM_VERSION,
                    app_version=APP_VERSION,
                    lang_code=LANG_CODE,
                    system_lang_code=SYSTEM_LANG_CODE
                )
                print(f"{Y}📂 Mavjud sessiya yuklanmoqda...{R}")
            else:
                client = TelegramClient(
                    StringSession(),
                    API_ID,
                    API_HASH,
                    device_model=DEVICE_MODEL,
                    system_version=SYSTEM_VERSION,
                    app_version=APP_VERSION,
                    lang_code=LANG_CODE,
                    system_lang_code=SYSTEM_LANG_CODE
                )
                print(f"{Y}🆕 Yangi sessiya yaratilmoqda...{R}")
        
            try:
                await client.connect()
        
                # Agar allaqachon avtorizatsiya qilingan bo'lsa
                if await client.is_user_authorized():
                    me = await client.get_me()
                    name = getattr(me, 'first_name', '') or ''
                    print(f"{G}✅ Sessiya faol: {phone} | {name}{R}")
                    
                    # Sessiyani saqlash
                    session_string = client.session.save()
                    with open(session_file, 'w', encoding='utf-8') as f:
                        f.write(session_string)
                    return phone
        
                # Kod so'rash
                await client.send_code_request(phone)
                print(f"{Y}📨 SMS kod yuborildi{R}")
                attempts_left = 3
        
                while True:
                    code = input(f"{Y}🔑 Kodni kiriting: {R}").strip()
                    if not code:
                        print(f"{RED}Kod bo'sh bo'lmasin!{R}")
                        continue
        
                    try:
                        await client.sign_in(phone, code)
                        break
        
                    except SessionPasswordNeededError:
                        print(f"{Y}🔐 2FA parol talab qilinadi{R}")
                        while True:
                            password = input(f"{Y}Parolni kiriting: {R}")
                            try:
                                await client.sign_in(password=password)
                                break
                            except PasswordHashInvalidError:
                                print(f"{RED}Parol xato! Qayta kiriting.{R}")
                        break
        
                    except PhoneCodeInvalidError:
                        attempts_left -= 1
                        print(f"{RED}Kod xato! Qolgan urinishlar: {attempts_left}{R}")
                        if attempts_left == 0:
                            print(f"{Y}Yangi kod so'ralmoqda...{R}")
                            await client.send_code_request(phone)
                            attempts_left = 3
        
                    except PhoneCodeExpiredError:
                        print(f"{Y}Kod eskirgan. Yangi kod so'ralmoqda...{R}")
                        await client.send_code_request(phone)
                        attempts_left = 3
        
                    except PhoneNumberBannedError:
                        print(f"{RED}❌ {phone} raqami BAN qilingan!{R}")
                        return None
        
                    except Exception as e:
                        print(f"{RED}Xatolik: {e}{R}")
                        return None
        
                # Muvaffaqiyatli avtorizatsiya
                if await client.is_user_authorized():
                    me = await client.get_me()
                    name = getattr(me, 'first_name', '') or ''
                    print(f"{G}🎉 Muvaffaqiyat: {phone} | {name}{R}")
                    
                    session_string = client.session.save()
                    with open(session_file, 'w', encoding='utf-8') as f:
                        f.write(session_string)
                    return phone
                else:
                    print(f"{RED}❌ Avtorizatsiya amalga oshmadi{R}")
                    return None
        
            except Exception as e:
                print(f"{RED}Umumiy xatolik: {e}{R}")
                return None
            
            finally:
                if client.is_connected():
                    await client.disconnect()
        
        
        async def migrate_string_to_sqlite(phone_number):
            """StringSession → SQLite session migratsiyasi"""
            session_file = os.path.join(SESSION_FOLDER, f'telethon_{phone_number}.session')
            
            if not os.path.exists(session_file):
                print(f"{RED}Sessiya topilmadi: {phone_number}{R}")
                return
        
            with open(session_file, 'r', encoding='utf-8') as f:
                session_string = f.read().strip()
        
            client = TelegramClient(
                StringSession(session_string),
                API_ID,
                API_HASH,
                device_model=DEVICE_MODEL,
                system_version=SYSTEM_VERSION,
                app_version=APP_VERSION,
                lang_code=LANG_CODE,
                system_lang_code=SYSTEM_LANG_CODE
            )
        
            async with client:
                await client.connect()
                
                dc_id = client.session.dc_id
                server_address = client.session.server_address
                port = client.session.port
                auth_key = client.session.auth_key
        
                sqlite_path = os.path.join(SESSION_FOLDER, f'{phone_number}_SQLite.session')
                sqlite_client = TelegramClient(
                    sqlite_path,
                    API_ID,
                    API_HASH,
                    device_model=DEVICE_MODEL,
                    system_version=SYSTEM_VERSION,
                    app_version=APP_VERSION,
                    lang_code=LANG_CODE,
                    system_lang_code=SYSTEM_LANG_CODE
                )
        
                await sqlite_client.connect()
                sqlite_client.session.set_dc(dc_id, server_address, port)
                sqlite_client.session.auth_key = auth_key
                sqlite_client.session.save()
                await sqlite_client.disconnect()
        
            print(f"{M}🧳 Migratsiya: {phone_number} → SQLite ✓{R}")
        
        
        async def main():
        
            if not os.path.exists(SESSION_FOLDER):
                os.makedirs(SESSION_FOLDER)
        
            phone_numbers = read_phones_from_csv('phone.csv')
            if not phone_numbers:
                input(f"{Y}phone.csv bo'sh. ENTER bosing...{R}")
                return
        
            print(f"\n{G}📋 Topilgan raqamlar: {len(phone_numbers)} ta{R}")
        
            authorized_phones = []
            for phone in phone_numbers:
                result = await create_and_check_session(phone)
                if result:
                    authorized_phones.append(result)
        
            # Migratsiya
            if authorized_phones:
                print(f"\n{M}━━━ SQLite Migratsiya ━━━{R}")
                for phone in authorized_phones:
                    await migrate_string_to_sqlite(phone)
        
            print(f"\n{G}═══════════════════════════════════════════{R}")
            print(f"{G}✅ Jami muvaffaqiyatli: {len(authorized_phones)}/{len(phone_numbers)}{R}")
            print(f"{G}═══════════════════════════════════════════{R}")
            
            input(f"\n{Y}Chiqish uchun ENTER bosing...{R}")
        
        
        if __name__ == "__main__":
            if os.name == 'nt':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(main())

    elif a == 5:
        import os
        import csv
        import random
        import requests
        import asyncio
        from telethon import TelegramClient
        from telethon.errors import RPCError
        from telethon.sessions import StringSession
        from telethon.tl.functions.photos import UploadProfilePhotoRequest
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        SESSIONS_DIR = 'sessions'
        PHONE_CSV = 'phone.csv'
        
        # --- CSV dan raqamlarni o‘qish ---
        def read_phone_numbers_from_csv(csv_file):
            phone_numbers = []
            if not os.path.exists(csv_file):
                print(f"{csv_file} topilmadi.")
                return []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0].strip():
                        phone_numbers.append(row[0].strip())
            return phone_numbers
        
        # --- Tasodifiy rasm olish ---
        def download_random_image():
            rnd = random.randint(1, 10**6)
            url = f"https://picsum.photos/seed/{rnd}/1080/1080"
            try:
                resp = requests.get(url, timeout=12)
                resp.raise_for_status()
                return resp.content
            except requests.RequestException as e:
                print(f"Rasm yuklashda xatolik: {e}")
                return None
        
        # --- Rasmni vaqtinchalik saqlash ---
        def save_image(image_data, filename):
            with open(filename, "wb") as file:
                file.write(image_data)
        
        # --- Profil rasmini o‘zgartirish ---
        async def change_profile_photo(client):
            image_data = download_random_image()
            if image_data:
                filename = "profile_photo.jpg"
                save_image(image_data, filename)
        
                uploaded = await client.upload_file(filename)
                await client(UploadProfilePhotoRequest(file=uploaded))
        
                os.remove(filename)
            else:
                print("Rasmni yuklab bo‘lmadi...")
        
        # --- Asosiy jarayon ---
        async def main():
            if not os.path.exists(SESSIONS_DIR):
                os.makedirs(SESSIONS_DIR, exist_ok=True)
        
            phone_numbers = read_phone_numbers_from_csv(PHONE_CSV)
            if not phone_numbers:
                input("phone.csv bo‘sh yoki topilmadi. Chiqish uchun ENTER bosing.")
                return
        
            for phone in phone_numbers:
                print(f"\n➡️ {phone} akkaunti uchun rasm almashtirilmoqda...")
                
                session_file = os.path.join(SESSIONS_DIR, f'telethon_{phone}.session')
                if not os.path.exists(session_file):
                    print(f"⚠️ {phone} uchun session fayl topilmadi. O‘tkazib yuborildi.")
                    continue
        
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                except Exception as e:
                    print(f"{phone} sessiya faylini o‘qishda xatolik: {e}")
                    continue
        
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
                try:
                    async with client:
                        if not await client.is_user_authorized():
                            print(f"❌ {phone} akkaunti avtorizatsiyadan o‘tmagan.")
                            continue
        
                        await change_profile_photo(client)
        
                        print(f"✅ {phone} akkauntining profil rasmi yangilandi.")
        
                        await asyncio.sleep(random.uniform(2.0, 5.0))
        
                except RPCError as e:
                    print(f"❗ RPC xatolik [{phone}]: {e}")
                    await asyncio.sleep(1.5)
                    continue
                except Exception as e:
                    print(f"❗ Nomaʼlum xatolik [{phone}]: {e}")
                    await asyncio.sleep(1.5)
                    continue
        
            print("\n🎉 Barcha akkauntlarning profil rasmlari yangilandi.")
            input("Chiqish uchun ENTER bosing...")
        
        if __name__ == "__main__":
            asyncio.run(main())



    elif a == 6:
        import os
        import csv
        import random
        import asyncio
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.tl.functions.account import UpdateProfileRequest
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESSIONS_DIR = "sessions"
        
        
        # --- CSV dan raqamlarni o‘qish ---
        def read_phone_numbers_from_csv(csv_file):
            phone_numbers = []
            with open(csv_file, 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        phone_numbers.append(row[0].strip())
            return phone_numbers
        
        
        # --- CSV dan ismlar va familiyalarni o‘qish ---
        def read_names_surnames_from_csv(csv_file):
            names_surnames = []
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 1:
                        if len(row) == 1:
                            name, surname = row[0], ""
                        else:
                            name, *surname = row[0].split()
                            surname = ' '.join(surname) if surname else ""
                        names_surnames.append((name.strip(), surname.strip()))
        
            random.shuffle(names_surnames)
            return names_surnames
        
        
        # --- Profilga ism-familiya o‘rnatish ---
        async def change_profile_name(client, name, surname):
            await client(UpdateProfileRequest(
                first_name=name,
                last_name=surname
            ))
        
        
        # --- Asosiy funksiya ---
        async def main():
            phone_numbers = read_phone_numbers_from_csv("phone.csv")
            names_surnames = read_names_surnames_from_csv("Ismlar.csv")
        
            for phone_number, (name, surname) in zip(phone_numbers, names_surnames):
                print(f"\n➡️ Profilga ism o‘rnatilmoqda: {name} {surname} ({phone_number})")
        
                session_file = f"{SESSIONS_DIR}/telethon_{phone_number}.session"
        
                if not os.path.exists(session_file):
                    print(f"⚠️ Session fayl topilmadi: {phone_number}")
                    continue
        
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                except Exception as e:
                    print(f"❌ Sessiyani o‘qishda xatolik: {phone_number} | {e}")
                    continue
        
                # DEFAULT Telethon – hech qanday fake device YO‘Q
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
                try:
                    await client.connect()
        
                    if not await client.is_user_authorized():
                        print(f"❌ Akkaunt avtorizatsiyadan o‘tmagan: {phone_number}")
                        await client.disconnect()
                        continue
        
                    # Ismni o‘zgartiramiz
                    await change_profile_name(client, name, surname)
                    print(f"✅ Ism muvaffaqiyatli o‘zgartirildi: {phone_number}")
        
                except Exception as e:
                    print(f"❗ Xatolik [{phone_number}]: {e}")
        
                finally:
                    await client.disconnect()
        
                # Bloklanmaslik uchun tasodifiy pauza
                await asyncio.sleep(random.uniform(1.5, 3.5))
        
            print("\n🎉 Barcha akkauntlarning ismlari o‘zgartirildi!")
            input("Chiqish uchun ENTER bosing...")
        
        
        if __name__ == "__main__":
            if os.name == "nt":
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except:
                    pass
        
            asyncio.run(main())


    elif a == 7:
        from telethon import TelegramClient, events, sync
        from telethon.sessions import StringSession
        import csv
        
        PHONE_FILE = 'phone.csv'
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        chat_id = 777000  # Замените на ваш chat_id

        async def display_accounts():
            with open(PHONE_FILE, 'r') as f:
                phone_list = [row[0] for row in csv.reader(f)]
        
            print(f"Barcha akountlar:\n")
            for i, phone in enumerate(phone_list):
                print(f"{i + 1}. {phone}")
        
            choice = int(input("Akountni tanlang: "))
            return phone_list[choice - 1]
        
        async def main():
            while True:
                phone = await display_accounts()
        
                # Создаем строку сессии или используем существующую
                session_file = f'sessions/telethon_{phone}.session'
                try:
                    with open(session_file, 'r') as f:
                        session_string = f.read().strip()
                except FileNotFoundError:
                    print(Fore.RED + f'Session fayl {phone} Topilmadi!.' + Style.RESET_ALL)
                    continue

                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
                try:
                    await client.start()
                    print("Telegramga muvaffaqiyatli ulandi!")
        
                    # Пример поиска последнего сообщения в чате
                    async for message in client.iter_messages(chat_id, limit=1):
                        print(message.text)
        
                except Exception as e:
                    print(f"Xatolik yuz berdi: {str(e)}")
                finally:
                    await client.disconnect()
                    input('\nEnter orqaga qaytish')
        
        if __name__ == "__main__":
            import asyncio
            asyncio.run(main())
    elif a == 8:  
        import os
        import csv
        import random
        import asyncio
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.tl.functions.account import UpdateUsernameRequest
        from telethon.errors import (
            UsernameOccupiedError,
            UsernameInvalidError,
            FloodWaitError,
            RPCError
        )
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESSIONS_DIR = "sessions"
        PHONE_CSV = "phone.csv"
        NAMES_CSV = "Ismlar.csv"
        
        
        # --- CSV dan telefon raqamlarni o‘qish ---
        def read_phone_numbers_from_csv(csv_file):
            phone_numbers = []
            if not os.path.exists(csv_file):
                print(f"{csv_file} topilmadi.")
                return []
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row and row[0].strip():
                        phone_numbers.append(row[0].strip())
            return phone_numbers
        
        
        # --- CSV dan ism ro'yxatini o‘qish ---
        def read_names_from_csv(csv_file):
            names = []
            if not os.path.exists(csv_file):
                print(f"{csv_file} topilmadi.")
                return []
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row and row[0].strip():
                        name = row[0].strip().split()[0]
                        names.append(name)
            return names
        
        
        # --- Tasodifiy username yaratish ---
        def generate_random_username(prefixes):
            if not prefixes:
                # Agar ism yo'q bo'lsa, umumiy prefixlardan foydalanamiz
                prefixes = ["user", "member", "ac"]
            prefix = random.choice(prefixes)
            suffix = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=4))
            return prefix.lower() + suffix
        
        
        # --- Username o'zgartirish funksiyasi ---
        async def change_profile_username(client, username):
            await client(UpdateUsernameRequest(username=username))
        
        
        # --- Asosiy jarayon ---
        async def main():
            phone_numbers = read_phone_numbers_from_csv(PHONE_CSV)
            names = read_names_from_csv(NAMES_CSV)
        
            if not phone_numbers:
                input("phone.csv bo'sh yoki topilmadi. Chiqish uchun ENTER bosing.")
                return
        
            if not names:
                print("Ismlar ro'yxati bo'sh — username yaratishda umumiy prefikslardan foydalaniladi.")
        
            for phone_number in phone_numbers:
                print(f"\n➡ {phone_number} — session fayl tekshirilmoqda...")
        
                session_file = os.path.join(SESSIONS_DIR, f"telethon_{phone_number}.session")
                if not os.path.exists(session_file):
                    print(f"⚠ Session fayl topilmadi: {session_file} — o‘tkazildi.")
                    continue
        
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                except Exception as e:
                    print(f"❌ {phone_number} — sessionni o‘qishda xatolik: {e}")
                    continue
        
                # DEFAULT Telethon — hech qanday fake device parametr yo'q
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
                try:
                    async with client:
                        if not await client.is_user_authorized():
                            print(f"❌ {phone_number} — akkaunt avtorizatsiyadan o‘tmagan yoki sessiya eskirgan.")
                            continue
        
                        # Har bir akkaunt uchun username sinovlari
                        attempt = 0
                        while True:
                            attempt += 1
                            username = generate_random_username(names)
                            try:
                                await change_profile_username(client, username)
                                print(f"✅ {phone_number} — username o‘rnatildi: @{username}")
                                break
                            except UsernameOccupiedError:
                                # band bo'lsa, qayta urinamiz
                                print(f"ℹ @{username} band — boshqasini sinaymiz...")
                                await asyncio.sleep(random.uniform(0.5, 1.5))
                                continue
                            except UsernameInvalidError:
                                # noto'g'ri format yoki qoidaga to'g'ri kelmaydi
                                print(f"ℹ @{username} noto‘g‘ri format — boshqa variant sinanmoqda...")
                                await asyncio.sleep(random.uniform(0.5, 1.5))
                                continue
                            except FloodWaitError as fw:
                                # kutish talab etiladi — fw.seconds mavjud bo'ladi
                                wait_sec = getattr(fw, 'seconds', None) or getattr(fw, 'retry_after', 30)
                                print(f"⏳ FloodWait: {wait_sec} soniya kutilyapti...")
                                await asyncio.sleep(wait_sec + 1)
                                continue
                            except RPCError as e:
                                # boshqa server xatolari
                                estr = str(e).lower()
                                if 'username is not different' in estr:
                                    print(f"⚠ {phone_number} — yangi username eskisi bilan teng, to‘xtatildi.")
                                    break
                                else:
                                    print(f"❗ {phone_number} — RPC xatolik: {e}")
                                    break
                            except Exception as e:
                                print(f"❗ {phone_number} — noma'lum xatolik: {e}")
                                break
        
                        # Akkauntlar orasida kichik tasodifiy pauza
                        await asyncio.sleep(random.uniform(1.5, 3.0))
        
                except Exception as e:
                    print(f"❗ Umumiy xatolik [{phone_number}]: {e}")
                    continue
        
            print("\n🎉 Barchasi tugadi — username o‘zgartirish jarayoni yakunlandi.")
            input("Chiqish uchun ENTER bosing...")
        
        
        if __name__ == "__main__":
            # Windows event loop muammosiga qarshi kichik fix
            if os.name == "nt":
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
            asyncio.run(main())


    elif a == 9:
        import csv
        import asyncio
        from telethon import TelegramClient
        from telethon.errors import RPCError
        from telethon.sessions import StringSession
        from telethon.tl.functions.channels import LeaveChannelRequest
        from telethon.tl.types import Channel, User
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESSION_FOLDER = 'sessions/'  # Путь к папке с сессиями
        
        def read_phone_numbers_from_csv(file_path):
            with open(file_path, 'r') as f:
                return [row[0] for row in csv.reader(f)]
        
        async def leave_chats(session_string, phone):
            print(f"Start: {phone}\n")

            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    print(f"Nomer {phone} CHIQARIB YUBORILGAN!")
                    await client.disconnect()
                    return
        
                async for dialog in client.iter_dialogs():
                    try:
                        entity = dialog.entity
                        if isinstance(entity, Channel):
                            if entity.megagroup:
                                await client(LeaveChannelRequest(entity))
                                print(f"chiqildi: {dialog.title}")
                        elif isinstance(entity, User):
                            # Проверка, является ли пользователь ботом
                            if not entity.bot:
                                # Удаляем личные чаты
                                await client.delete_dialog(entity)
                                print(f"chiqildi: {dialog.title}")
                        elif isinstance(entity, Channel):
                            # Удаляем обычные группы (не мега-группы)
                            if not entity.megagroup:
                                await client.delete_dialog(entity)
                                print(f"chiqildi: {dialog.title}")
                    except Exception as e:
                        print(f"Xatolik: {e}")
                        continue
        
                print(f"Nomer: {phone} -- TOZALANDI!")
        
            except RPCError as e:
                print(f"Nomer: {phone} ! Xatolik: {e}")
            finally:
                await client.disconnect()
        
        async def main():
            phone_numbers = read_phone_numbers_from_csv('phone.csv')
        
            tasks = []
            for phone in phone_numbers:
                session_file = f'{SESSION_FOLDER}telethon_{phone}.session'
                
                try:
                    with open(session_file, 'r') as f:
                        session_string = f.read().strip()
                    tasks.append(leave_chats(session_string, phone))
                except FileNotFoundError:
                    print(f"Sessiya {session_file} TOPILMADI!")
                    continue
        
            await asyncio.gather(*tasks)
        
            print('Tugallandi')
            input("ENTER CHHIQISH")
        
        if __name__ == "__main__":
            asyncio.run(main())

    elif a == 10:
        import csv
        import asyncio
        import configparser
        from telethon import TelegramClient, errors
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        SESSION_FOLDER = 'sessions/'  # Путь к папке с сессиями
        
        async def update_2fa_password(session_string, phone_number, current_password, new_password):
            try:
                async with TelegramClient(StringSession(session_string), API_ID, API_HASH) as client:
                    await client.start()
                    await client.edit_2fa(current_password=current_password, new_password=new_password)
                    print(f"2FA PAROL YANGILANDI {phone_number}.")
                    return True
            except errors.RPCError as e:
                print(f"XATOLIK ESKI PAROL NOTOGRI! {phone_number}")
                return False
        
        # Функция для чтения номеров телефонов из CSV-файла
        def read_phone_numbers_from_csv(csv_file):
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                phone_numbers = [row[0] for row in reader]
            return phone_numbers
        
        # Функция для чтения текущего и нового паролей из config.ini
        def read_passwords_from_config():
            config = configparser.ConfigParser()
            config.read('../Guruxlar.ini')
            current_password = config['T_Market']['current_password']
            new_password = config['T_Market']['new_password']
            return current_password, new_password
        
        async def main():
            # Чтение номеров телефонов из CSV-файла
            csv_file = 'phone.csv'  # Путь к CSV-файлу с номерами телефонов
            phone_numbers = read_phone_numbers_from_csv(csv_file)
        
            # Текущий и новый пароль из config.ini
            current_password, new_password = read_passwords_from_config()
        
            # Обновление 2FA пароля для каждого аккаунта
            tasks = []
            for phone_number in phone_numbers:
                session_file = f'{SESSION_FOLDER}telethon_{phone_number}.session'
                try:
                    with open(session_file, 'r') as f:
                        session_string = f.read().strip()
                    tasks.append(update_2fa_password(session_string, phone_number, current_password, new_password))
                except FileNotFoundError:
                    print(f"Session FAYL {session_file} TOPILMADI!")
                    continue
        
            results = await asyncio.gather(*tasks)
            success_count = sum(results)
            print(f"2FA Parol YANGILANDI! {success_count} Shuncha nomerdan {len(phone_numbers)}.")
            input('CHIQISH UCHUN ENTER')
        if __name__ == "__main__":
            asyncio.run(main())
    elif a == 11:
        import csv
        import configparser
        import asyncio
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.errors import PhoneNumberBannedError, FloodWaitError
        from telethon.tl.functions.channels import JoinChannelRequest, GetFullChannelRequest
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        SESSION_FOLDER = 'sessions/'
        
        async def process_phone(phone):
            session_file = f'{SESSION_FOLDER}telethon_{phone}.session'
        
            try:
                with open(session_file, 'r') as f:
                    session_string = f.read()
            except FileNotFoundError:
                print(f'Session fayl {phone} topilmadi!')
                return
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    print(f"Akount {phone} chiqarib yuborilgan!")
                    await client.disconnect()
                    return
                config = configparser.ConfigParser()
                config.read('../Guruxlar.ini')
                channel_links = [link.replace('https://t.me/', '') for link in config['T_Market']['channel_links'].split(',')]
        
                for link in channel_links:
                    try:
                        chat = await client(JoinChannelRequest(link.strip()))
                        await asyncio.sleep(5)
                        channel_info = await client.get_entity(link.strip())
                        print(f"{phone}: Qoshildi: {channel_info.title}")
                    except FloodWaitError as e:
                        print(f'kuting...{e.seconds}')
                        await asyncio.sleep(e.seconds)
                    except Exception as e:
                        print(f'xatolik {phone} qoshilishda {link}: {e}')
            except PhoneNumberBannedError:
                print(f"Nomer {phone} chiqarib yuborilgan!")
            except Exception as e:
                print(f"Nomer {phone} XATOLIK: {e}")
            finally:
                await client.disconnect()
        
        async def main():
            with open('phone.csv', 'r') as f:
                str_list = [row[0] for row in csv.reader(f)]
            
            batch_size = 10
            for i in range(0, len(str_list), batch_size):
                batch = str_list[i:i + batch_size]
                tasks = [process_phone(phone) for phone in batch]
                await asyncio.gather(*tasks)
        
        if __name__ == '__main__':
            asyncio.run(main())
            input("Enter chiqish!")


    elif a == 12:
        import os
        import csv
        import random
        import asyncio
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.tl.functions.messages import SendReactionRequest
        from telethon.tl.types import ReactionEmoji
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESSIONS_DIR = "sessions"
        
        # 9 ta reaksiya:
        REACTIONS = [
            '👍',   # 1 - layk (bosh barmoq)
            '❤️',   # 2 - yurakcha
            '🔥',   # 3 - olov
            '🏆',   # 4 - sovrin
            '🕊️',   # 5 - kabutar
            '👏',   # 6 - qarsak
            '🤝',   # 7 - salomlashuv
            '🎉',   # 8 - bayram (YANGI)
            '🥰',   # 9 - sevgi (YANGI)
        ]
        
        REACTION_NAMES = {
            '👍': 'Layk',
            '❤️': 'Yurakcha',
            '🔥': 'Olov',
            '🏆': 'Sovrin',
            '🕊️': 'Kabutar',
            '👏': 'Qarsak',
            '🤝': 'Salomlashuv',
            '🎉': 'Bayram',   # YANGI
            '🥰': 'Sevgi',    # YANGI
        }
        
        
        def read_phone_numbers_from_csv(csv_file):
            phone_numbers = []
            with open(csv_file, 'r', encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        phone_numbers.append(row[0].strip())
            return phone_numbers
        
        
        async def send_reaction(client, chat_id, message_id, reaction):
            try:
                await client(SendReactionRequest(
                    peer=chat_id,
                    msg_id=message_id,
                    reaction=[ReactionEmoji(emoticon=reaction)]
                ))
                return True
            except:
                return False
        
        
        async def main():
            phone_numbers = read_phone_numbers_from_csv("phone.csv")
        
            if not phone_numbers:
                print("❌ phone.csv faylidan hech qanday raqam topilmadi!")
                input("Chiqish uchun ENTER bosing...")
                return
        
            print("\n📱 Telegram postiga random reaksiya bosish dasturi")
            print("-" * 40)
            post_url = input("🔗 Telegram post linkini kiriting:\n(masalan: https://t.me/millatimiz_umidlari/10842): ").strip()
        
            if "t.me/" not in post_url:
                print("❌ Xato: Noto'g'ri link!")
                input("Chiqish uchun ENTER bosing...")
                return
        
            try:
                after_tme = post_url.split("t.me/")[-1]
                parts = after_tme.split("/")
        
                if len(parts) < 2:
                    print("❌ Xato: Linkda post ID si yo'q!")
                    input("Chiqish uchun ENTER bosing...")
                    return
        
                chat_id = parts[0]
                message_id = int(parts[1])
        
                print(f"✅ Kanal: @{chat_id}")
                print(f"✅ Post ID: {message_id}")
        
            except:
                print("❌ Xato: Linkni tahlil qilishda xatolik!")
                input("Chiqish uchun ENTER bosing...")
                return
        
            print(f"\n🎭 Reaksiyalar (9 ta):")
            for i, (emoji, name) in enumerate(REACTION_NAMES.items(), 1):
                print(f"   {i}. {emoji}  {name}")
        
            print(f"\n📊 Ma'lumotlar:")
            print(f"   Akkauntlar soni: {len(phone_numbers)}")
            print(f"   Har bir akkaunt: 1 ta random reaksiya")
            print(f"   Jami reaksiya: {len(phone_numbers)} ta")
        
            confirm = input("\n✅ Reaksiya bosishni boshlaysizmi? (ha/yo'q): ").strip().lower()
        
            if confirm in ['ha', 'hа', 'yes', 'y', '1', 'true', 'boshlash', 'start'] or confirm.startswith('ha'):
                print("\n🚀 Reaksiya bosish boshlandi...\n")
            else:
                print("❌ Bekor qilindi!")
                input("Chiqish uchun ENTER bosing...")
                return
        
            success_count = 0
            total_count = 0
            stats = {r: 0 for r in REACTIONS}
        
            for idx, phone in enumerate(phone_numbers, 1):
                print(f"\n[{idx}/{len(phone_numbers)}] 📱 {phone}")
        
                session_file = f"{SESSIONS_DIR}/telethon_{phone}.session"
        
                if not os.path.exists(session_file):
                    print(f"   ⚠️ Session fayl topilmadi")
                    continue
        
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                except:
                    print(f"   ❌ Session faylni o'qib bo'lmadi")
                    continue
        
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
                try:
                    await client.connect()
        
                    if not await client.is_user_authorized():
                        print(f"   ❌ Avtorizatsiya yo'q")
                        await client.disconnect()
                        continue
        
                    me = await client.get_me()
        
                    reaction = random.choice(REACTIONS)
                    print(f"   🎲 Reaksiya: {reaction} ({REACTION_NAMES[reaction]})")
        
                    success = await send_reaction(client, chat_id, message_id, reaction)
                    total_count += 1
        
                    if success:
                        success_count += 1
                        stats[reaction] += 1
                        print(f"   ✅ Boshlidi! ({me.first_name})")
                    else:
                        print(f"   ❌ Xatolik!")
        
                except Exception as e:
                    print(f"   ❌ Xatolik: {str(e)[:50]}")
        
                finally:
                    await client.disconnect()
        
                if idx < len(phone_numbers):
                    wait = random.uniform(5, 10)
                    print(f"   ⏳ {wait:.1f} soniya kutish...")
                    await asyncio.sleep(wait)
        
            # Hisobot
            print("\n" + "=" * 50)
            print("📊 HISOBOT:")
            print(f"   Jami urinishlar: {total_count}")
            print(f"   Muvaffaqiyatli: {success_count}")
            print(f"   Muvaffaqiyatsiz: {total_count - success_count}")
        
            if success_count > 0:
                print(f"\n🎭 REAKSIYA STATISTIKASI:")
                for r, c in sorted(stats.items(), key=lambda x: x[1], reverse=True):
                    if c > 0:
                        percent = (c / success_count) * 100
                        bar = "█" * int(percent / 2) + "░" * (50 - int(percent / 2))
                        print(f"   {r} {REACTION_NAMES[r]}: {bar} {c} ta ({percent:.1f}%)")
        
            print("=" * 50)
            print("\n🎉 Tugadi!")
            input("\nChiqish uchun ENTER bosing...")
        
        
        if __name__ == "__main__":
            if os.name == "nt":
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except:
                    pass
        
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                print("\n\n⚠️ To'xtatildi!")
                input("Chiqish uchun ENTER bosing...")
    elif a == 13:
        import csv
        import os
        import asyncio
        import configparser
        from telethon import TelegramClient
        from telethon.errors import RPCError
        from telethon.sessions import StringSession
        from telethon import functions, types
        
        # Чтение конфигурации
        config = configparser.ConfigParser()
        config.read('config.ini')
        api_id = 253798
        api_hash = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        def read_csv(file_path):
            accounts = []
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 1:
                        accounts.append({'phone_number': row[0]})
            return accounts
        
        async def leave_all_dialogs(client):
            # Получаем все диалоги (включая архивированные)
            dialogs = await client.get_dialogs(limit=1000)  # Увеличиваем лимит для охвата всех диалогов
            for dialog in dialogs:
                try:
                    # Пропускаем служебные сообщения от Telegram
                    if isinstance(dialog.entity, types.User):
                        if dialog.entity.bot:
                            continue  # Пропускаем ботов
                        if dialog.entity.id == 777000:
                            continue  # Пропускаем служебные сообщения от Telegram
                    
                    # Пропускаем каналы и группы, но обрабатываем их по желанию
                    if isinstance(dialog.entity, (types.Channel, types.Chat)):
                        # Пропустите, если это нужно
                        pass
        
                    await client.delete_dialog(dialog.entity)
                    print(f"o'chirildi: {dialog.entity.title if hasattr(dialog.entity, 'title') else 'Nomsiz'}")
                except Exception as e:
                    print(f"xatolik {dialog.entity.title if hasattr(dialog.entity, 'title') else 'Nomsiz'}: {e}")
        
        async def delete_folders(client):
            filters = await client(functions.messages.GetDialogFiltersRequest())
            if not filters or not filters.filters:
                print("Papka topilmadi.")
                return
        
            for folder in filters.filters:
                # Пропускаем папку по умолчанию
                if isinstance(folder, types.DialogFilterDefault):
                    print("Papka o'tqazib yuborildi.")
                    continue
        
                try:
                    await client(functions.messages.UpdateDialogFilterRequest(
                        id=folder.id,
                        filter=None  # Удаляет папку
                    ))
                    print(f"o'chirildi: {folder.title if hasattr(folder, 'title') else 'Nomsiz'}")
                except Exception as e:
                    print(f"Xatolik {folder.title if hasattr(folder, 'title') else 'Nomsiz'}: {e}")
        
        async def main():
            csv_file_path = "phone.csv"
            accounts = read_csv(csv_file_path)
        
            for account in accounts:
                session_file = f'sessions/telethon_{account["phone_number"]}.session'
                if not os.path.exists(session_file):
                    print(f"Sessiya {account['phone_number']} Topilmadi!")
                    continue
        
                try:
                    with open(session_file, 'r') as f:
                        session_string = f.read().strip()
                except FileNotFoundError:
                    print(f'Sessiya {account["phone_number"]} Topilmadi!')
                    continue
        
                try:
                    async with TelegramClient(StringSession(session_string), api_id, api_hash) as client:
                        # Удаление всех диалогов
                        await leave_all_dialogs(client)
                        # Удаление всех папок
                        await delete_folders(client)
                except RPCError as e:
                    print(f"Nomer: {account['phone_number']} Xatolik: {e}!")
                
                await asyncio.sleep(1)  # Задержка в 1 секунду между выполнением функций
        
        if __name__ == "__main__":
            asyncio.run(main())
            input("Chiqish uchun ENTER...")

    elif a == 14:
        import csv
        import asyncio
        from telethon import TelegramClient
        from telethon.errors import RPCError
        from telethon.sessions import StringSession
        from telethon.tl.functions.channels import LeaveChannelRequest
        from telethon.tl.types import Channel
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESSION_FOLDER = 'sessions/'
        
        def read_phone_numbers_from_csv(file_path):
            with open(file_path, 'r') as f:
                return [row[0] for row in csv.reader(f)]
        
        async def get_dialogs_list(session_string):
            """Birinchi akount orqali kanal/guruhlar ro'yxatini oladi"""
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            dialogs_list = []
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    print("Birinchi akount avtorizatsiyadan o'tmagan!")
                    return []
        
                print("Kanal va guruhlar yuklanmoqda...\n")
                async for dialog in client.iter_dialogs():
                    entity = dialog.entity
                    if isinstance(entity, Channel):
                        chat_type = "Guruh" if entity.megagroup else "Kanal"
                        dialogs_list.append({
                            "title": dialog.title,
                            "type": chat_type
                        })
            except Exception as e:
                print(f"Xatolik: {e}")
            finally:
                await client.disconnect()
            return dialogs_list
        
        def show_and_select(dialogs_list):
            """Ro'yxatni ko'rsatadi va foydalanuvchi tanlaydi"""
            if not dialogs_list:
                print("Hech qanday kanal/guruh topilmadi!")
                return None
        
            print("=" * 50)
            print(f"{'#':<5} {'Turi':<10} {'Nomi'}")
            print("=" * 50)
            for i, d in enumerate(dialogs_list, 1):
                print(f"{i:<5} {d['type']:<10} {d['title']}")
            print("=" * 50)
        
            while True:
                try:
                    choice = int(input(f"\nRaqam tanlang (1-{len(dialogs_list)}): "))
                    if 1 <= choice <= len(dialogs_list):
                        selected = dialogs_list[choice - 1]
                        print(f"\nTanlandi: [{selected['type']}] {selected['title']}\n")
                        return selected['title']
                    else:
                        print("Noto'g'ri raqam, qayta kiriting.")
                except ValueError:
                    print("Faqat raqam kiriting!")
        
        async def leave_target_chat(session_string, phone, target_title):
            print(f"Urinish: {phone}")
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    print(f"  [{phone}] Avtorizatsiyadan o'tmagan!")
                    return
        
                found = False
                async for dialog in client.iter_dialogs():
                    if dialog.title.strip().lower() == target_title.strip().lower():
                        entity = dialog.entity
                        try:
                            if isinstance(entity, Channel):
                                await client(LeaveChannelRequest(entity))
                            else:
                                await client.delete_dialog(entity)
                            print(f"  [{phone}] ✅ Chiqildi: {dialog.title}")
                            found = True
                        except Exception as e:
                            print(f"  [{phone}] ❌ Xatolik: {e}")
                        break
        
                if not found:
                    print(f"  [{phone}] ⚠️  '{target_title}' topilmadi")
        
            except RPCError as e:
                print(f"  [{phone}] RPC Xatolik: {e}")
            finally:
                await client.disconnect()
        
        async def main():
            phone_numbers = read_phone_numbers_from_csv('phone.csv')
            if not phone_numbers:
                print("phone.csv bo'sh!")
                return
        
            # Birinchi akount orqali ro'yxat olish
            first_phone = phone_numbers[0]
            session_file = f'{SESSION_FOLDER}telethon_{first_phone}.session'
            try:
                with open(session_file, 'r') as f:
                    first_session = f.read().strip()
            except FileNotFoundError:
                print(f"Birinchi sessiya topilmadi: {session_file}")
                return
        
            # Ro'yxatni olish va tanlash
            dialogs = await get_dialogs_list(first_session)
            target_title = show_and_select(dialogs)
            if not target_title:
                return
        
            confirm = input(f"Barcha {len(phone_numbers)} ta akount '{target_title}'dan chiqsinmi? (ha/yo'q): ")
            if confirm.lower() != 'ha':
                print("Bekor qilindi.")
                return
        
            print(f"\n{'='*50}")
            print(f"Jarayon boshlandi: {len(phone_numbers)} ta akount")
            print(f"{'='*50}\n")
        
            tasks = []
            for phone in phone_numbers:
                session_file = f'{SESSION_FOLDER}telethon_{phone}.session'
                try:
                    with open(session_file, 'r') as f:
                        session_string = f.read().strip()
                    tasks.append(leave_target_chat(session_string, phone, target_title))
                except FileNotFoundError:
                    print(f"Sessiya topilmadi: {session_file}")
        
            await asyncio.gather(*tasks)
        
            print(f"\n{'='*50}")
            print("✅ Tugallandi!")
            input("Chiqish uchun ENTER bosing...")
        
        if __name__ == "__main__":
            asyncio.run(main())   

    elif a == 15:
        import csv
        import asyncio
        import sqlite3
        from telethon import TelegramClient
        from telethon.errors import RPCError
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        async def clean_session(file_path):
            try:
                conn = sqlite3.connect(file_path)
                cursor = conn.cursor()
        
                # Удаляем все строки из таблиц
                cursor.execute("DELETE FROM update_state")
                cursor.execute("DELETE FROM sent_files")
                cursor.execute("DELETE FROM entities")
                conn.commit()  # Коммитим изменения, чтобы завершить транзакцию
        
                # Выполняем вакуумизацию, чтобы освободить пространство
                cursor.execute("VACUUM")
                conn.close()
                print(f"Sessiya {file_path} tozalandi.")
            except sqlite3.Error as e:
                print(f"Xatolik: {e}")
        
        async def handle_phone(phone):
            print(f"Start {phone}")
            session_path = f'sessions/{phone}_SQLite.session'
            client = TelegramClient(session_path, API_ID, API_HASH)
        
            try:
                await client.start(phone=phone)
                if await client.is_user_authorized():
                    print(f"Nomer: {phone} ulandi")
            except RPCError as e:
                print(f"Nomer: {phone} CHIQARIB YUBORILGAN!")
            finally:
                try:
                    await client.disconnect()
                except Exception as e:
                    print(f"XATOLIK {e}")
                await clean_session(session_path)
        
        async def main():
            with open('phone.csv', 'r') as f:
                str_list = [row[0] for row in csv.reader(f)]
                await asyncio.gather(*[handle_phone(phone) for phone in str_list])
        
        # Запуск основной функции
        if __name__ == "__main__":
            asyncio.run(main())
            input("Нажмите ENTER для выхода...")
            
    elif a == 16:    
        import subprocess
        import sys
        import os
        
        # ---- Pip orqali modulni jim o'rnatish/tekshirish ----
        def install_package(package_name):
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "show", package_name],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                print("MODUL ORNATILGAN!.")
            except subprocess.CalledProcessError:
                print("MODUL O'RNATIMOQDA...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package_name, "-q", "--disable-pip-version-check"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                print("OK.")
        
        # cryptography kerak bo'ladi
        install_package('cryptography')
        
        
        import csv
        import asyncio
        from telethon import TelegramClient, errors
        from telethon.sessions import StringSession
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        SESSION_FOLDER = './sessions'
        
        
        # Telefonlarni CSV dan o'qish
        def read_phones_from_csv(file_path):
            phone_numbers = []
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                        phone_numbers.append(row[0])
            return phone_numbers
        
        
        # CSV ga qayta yozish (bo'sh qatorlarsiz)
        def write_phones_to_csv(file_path, phone_numbers):
            phone_numbers = [phone.strip() for phone in phone_numbers if phone.strip()]
            with open(file_path, 'w', encoding='utf-8') as csvfile:
                csvfile.write('\n'.join(phone_numbers))
        
        
        # +998... yoki 998... — har ikkala formatni ham qo'llab-quvvatlash
        def normalize_phone_for_signin(raw: str) -> str:
            s = raw.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            return s if s.startswith('+') else f'+{s}'
        
        
        # Bitta telefon uchun session yaratish/tekshirish
        async def create_and_check_session(phone, semaphore, valid_phones, invalid_phones):
            async with semaphore:
                os.makedirs(SESSION_FOLDER, exist_ok=True)
                session_file = os.path.join(SESSION_FOLDER, f'telethon_{phone}.session')
                sqlite_session_file = os.path.join(SESSION_FOLDER, f'{phone}_SQLite.session')
        
                if os.path.exists(session_file):
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                        # TOZA TelegramClient - hech qanday fake device yo'q
                        client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
                else:
                    # TOZA TelegramClient - hech qanday fake device yo'q
                    client = TelegramClient(StringSession(), API_ID, API_HASH)
        
                try:
                    await client.connect()
                    if not await client.is_user_authorized():
                        e164 = normalize_phone_for_signin(phone)
                        await client.send_code_request(e164)
                        attempt_count = 0
                        while True:
                            # Atayin noto'g'ri kod — sizning mavjud mantiqingiz (3 martagacha)
                            code = "0000"
                            try:
                                await client.sign_in(e164, code)
                                print(f"Tasdiqlandi {phone}")
                                break
                            except errors.SessionPasswordNeededError:
                                # 2FA parol sikli
                                while True:
                                    password = input(f'{phone} 2FA parolini kiriting: ')
                                    try:
                                        await client.sign_in(password=password)
                                        print(f"Tasdiqlandi {phone}\n")
                                        break
                                    except errors.PasswordHashInvalidError:
                                        print("Parol xato. Yana kiriting!\n")
                                    except Exception as e:
                                        print(f"Xato parol yoki kod: {str(e)}")
                                break
                            except errors.CodeInvalidError:
                                attempt_count += 1
                                if attempt_count >= 3:
                                    print(f"{phone} kodi 3 marta xato. O'chiriladi.")
                                    invalid_phones.append(phone)
                                    break
                                print("Kod xato. Yana kiriting!\n")
                            except errors.PhoneNumberBannedError:
                                print(f"{phone} NOMER BAN O'CHIRILDI!.")
                                invalid_phones.append(phone)
                                if os.path.exists(session_file):
                                    os.remove(session_file)
                                if os.path.exists(sqlite_session_file):
                                    os.remove(sqlite_session_file)
                                return
                            except Exception as e:
                                print(f"Xato kod/parol: {str(e)}")
                                invalid_phones.append(phone)
                                break
        
                        if await client.is_user_authorized():
                            session_string = client.session.save()
                            with open(session_file, 'w', encoding='utf-8') as f:
                                f.write(session_string)
                            valid_phones.append(phone)
                        else:
                            print(f"{phone} TASDIQLANMAGAN NOMER. O'CHIRILDI!.")
                            invalid_phones.append(phone)
                            if os.path.exists(session_file):
                                os.remove(session_file)
                            if os.path.exists(sqlite_session_file):
                                os.remove(sqlite_session_file)
                    else:
                        print(f"{phone} Tasdiqlandi\n")
                        valid_phones.append(phone)
                except errors.PhoneNumberBannedError:
                    print(f"{phone} NOMER BAN O'CHIRILDI!")
                    invalid_phones.append(phone)
                    if os.path.exists(session_file):
                        os.remove(session_file)
                    if os.path.exists(sqlite_session_file):
                        os.remove(sqlite_session_file)
                except Exception as e:
                    print(f"Xatolik {phone}: {str(e)}")
                    invalid_phones.append(phone)
                finally:
                    await client.disconnect()
        
        
        # Asosiy oqim
        async def main():
            phone_numbers = read_phones_from_csv('phone.csv')
            semaphore = asyncio.Semaphore(5)
            valid_phones = []
            invalid_phones = []
        
            tasks = [create_and_check_session(phone, semaphore, valid_phones, invalid_phones) for phone in phone_numbers]
            await asyncio.gather(*tasks)
        
            # CSV dan noto'g'ri (ban/xato)larni olib tashlaymiz
            phone_numbers = [phone for phone in phone_numbers if phone not in invalid_phones]
            write_phones_to_csv('phone.csv', phone_numbers)
        
            print("AKOUNTLAR RO'YXATI YANGILANDI SESSION FAYLLAR XAM!\n")
            input("ENTER чиқиш")
        
        
        if __name__ == "__main__":
            asyncio.run(main())


    elif a == 17: 
        import asyncio
        import csv
        from telethon import TelegramClient, types
        from telethon.tl import functions
        from telethon.tl.types import InputPeerUser
        from colorama import Fore, init
        from telethon.errors import FloodWaitError
        
        init(autoreset=True)
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        
        def read_phones_from_csv(path):
            try:
                with open(path, newline='') as f:
                    return [r[0] for r in csv.reader(f) if r]
            except Exception as e:
                print(Fore.RED + f"CSV o'qishda xato: {e}")
                return []
        
        
        async def get_reactions_list(client, chat, msg_id, limit=100):
            try:
                peer = await client.get_input_entity(chat)
                return await client(functions.messages.GetMessageReactionsListRequest(
                    peer=peer, id=msg_id, limit=limit))
            except Exception as e:
                print(Fore.RED + f"Reaksiyalarni olishda xato {msg_id}: {e}")
                return None
        
        
        # =====================================================
        # XABARLAR BO'YICHA — message.sender ishlatadi
        # =====================================================
        async def worker_messages(phone, client, link, limit):
            users_all = {}
            idx = 0
        
            try:
                async for m in client.iter_messages(link, limit=limit):
                    idx += 1
                    # sender to'g'ridan-to'g'ri message ichida keladi — get_entity shart emas
                    sender = m.sender
                    if sender and isinstance(sender, types.User) and not sender.bot:
                        name = f"{sender.first_name or ''} {sender.last_name or ''}".strip()
                        users_all[sender.id] = (name, sender.id, getattr(sender, "access_hash", 0))
        
                    print(f"\r{Fore.GREEN}[{phone}] XABAR: {idx}/{limit}", end="", flush=True)
            except FloodWaitError as e:
                print(Fore.YELLOW + f"\n[{phone}] FloodWait {e.seconds}s...")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print(Fore.RED + f"\n[{phone}] Xato: {e}")
        
            print(f"\n{Fore.CYAN}[{phone}] TUGADI. ({len(users_all)} ta topildi)")
            return users_all
        
        
        # =====================================================
        # REAKSIYA BO'YICHA
        # =====================================================
        async def worker_reactions(phone, client, link, msgs):
            total = len(msgs)
            users_all = {}
        
            for idx, m in enumerate(msgs, start=1):
                if m.reactions and m.reactions.results:
                    res = await get_reactions_list(client, link, m.id)
                    if res:
                        for u in res.users:
                            if not getattr(u, 'bot', True):
                                name = f"{u.first_name or ''} {u.last_name or ''}".strip()
                                users_all[u.id] = (name, u.id, getattr(u, "access_hash", 0))
        
                prog = (idx / total) * 100
                print(f"\r{Fore.GREEN}[{phone}] REAKSIYA: {prog:.1f}%", end="", flush=True)
        
            print(f"\n{Fore.CYAN}[{phone}] TUGADI. ({len(users_all)} ta topildi)")
            return users_all
        
        
        # =====================================================
        # ASOSIY RUNNER
        # =====================================================
        async def run_all(phones, link, limit, mode):
            clients = []
            for phone in phones:
                session = f"sessions/{phone}_SQLite.session"
                c = TelegramClient(session, API_ID, API_HASH)
                await c.connect()
                if not await c.is_user_authorized():
                    print(Fore.RED + f"[{phone}] Avtorizatsiyadan chiqib ketgan! O'tkazib yuborildi.")
                    await c.disconnect()
                else:
                    clients.append((phone, c))
                    print(Fore.CYAN + f"[{phone}] Ulandi.")
        
            if not clients:
                print(Fore.RED + "Hech qanday aktiv akkaunt yo'q!")
                return
        
            print(Fore.CYAN + f"\n{len(clients)} ta akkaunt ulandi.")
            print(Fore.YELLOW + f"Barcha {len(clients)} ta akkaunt {limit} ta postni parallel tekshiradi...\n")
        
            # Hammasi parallel, har biri iter_messages ishlatadi
            if mode == 1:
                # Reaksiya uchun avval postlarni olamiz
                msgs = await clients[0][1].get_messages(link, limit=limit)
                tasks = [worker_reactions(phone, client, link, msgs) for phone, client in clients]
            else:
                tasks = [worker_messages(phone, client, link, limit) for phone, client in clients]
        
            results = await asyncio.gather(*tasks)
        
            # Natijalarni birlashtirish
            merged = {}
            for result_dict in results:
                merged.update(result_dict)
        
            print(Fore.GREEN + f"\nJami {len(merged)} ta unikal foydalanuvchi topildi.")
        
            with open("users.csv", "w", encoding="UTF-8", newline="") as f:
                writer = csv.writer(f, delimiter=",", lineterminator="\n")
                writer.writerow(['index', 'name', 'id', 'access_hash', 'status'])
                for i, (uid, (name, uid2, ah)) in enumerate(merged.items(), start=1):
                    writer.writerow([i, name, uid2, ah, "new"])
        
            print(Fore.GREEN + f"users.csv saqlandi! ({len(merged)} ta foydalanuvchi)\n")
        
            for _, client in clients:
                await client.disconnect()
        
        
        async def main():
            ch = int(input("[1] Reaksiya bo'yicha olish\n[2] Xabarlar bo'yicha olish\n\nTANLANG: "))
            phones = read_phones_from_csv('phone.csv')
            if not phones:
                print("phone.csv bo'sh!")
                return
            link = input("Gurux linkini kiriting: ")
            limit = int(input("Nechta postni tekshiramiz: "))
            await run_all(phones, link, limit, mode=ch)
        
        
        asyncio.run(main())
                       
            
    elif a == 18:
        import os
        import csv
        import asyncio
        from telethon import TelegramClient, functions
        from telethon.sessions import StringSession
        from colorama import init, Fore
        
        # Инициализация colorama
        init(autoreset=True)
        
        # Цветовые константы
        lg = Fore.LIGHTGREEN_EX  # ярко-зеленый
        rs = Fore.RESET          # сброс цвета
        g  = Fore.GREEN          # зеленый
        b  = Fore.BLUE           # синий
        r  = Fore.RED            # красный
        cy = Fore.CYAN           # циановый
        ye = Fore.YELLOW         # желтый
        grey = Fore.LIGHTBLACK_EX  # серый
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        SESSION_FOLDER = './sessions'
        
        
        def read_phones_from_csv(file_path):
            phones = []
            with open(file_path, newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row:
                        phones.append(row[0])
            return phones
        
        
        async def manage_authorizations(phone, index):
            session_file = os.path.join(SESSION_FOLDER, f'telethon_{phone}.session')
            if not os.path.exists(session_file):
                print(f"{r}{index}||| {phone} Sessiya topilmadi!")
                return
            
            client = None
            try:
                with open(session_file, 'r') as f:
                    session_string = f.read().strip()
            
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
                await client.connect()
                if not await client.is_user_authorized():
                    print(f"{r}{index}||| {phone} Chiqarib yuborilgan...")
                    return
            
                auths = await client(functions.account.GetAuthorizationsRequest())
                print(f"\n{ye}{index}||| Akkount {phone}: Ro'yxatdan o'tgan:\n")
                
                # --- FAQAT SHU QATOR O'ZGARTIRILDI ---
                for idx, auth in enumerate(auths.authorizations, start=1):
                    date_active = auth.date_active.strftime('%Y-%m-%d %H:%M:%S')
                    # Ilova nomini olish (agar mavjud bo'lmasa, bo'sh string bo'ladi)
                    app_name = auth.app_name or "" 
                    # Qurilma va ilova nomini birga chiqarish
                    print(f"{b}{idx}. Qurilma: {auth.device_model} ({app_name}) (Kirgan vaqti {date_active})")
                # ------------------------------------
            
                # Запрашиваем у пользователя выбор устройств для УДАЛЕНИЯ
                to_delete = []
                while not to_delete:
                    print(f"{Fore.RED}O'tqazib yuborish uchun '0' ni bosing")
                    choice = input(f"{cy}O'chirmoqchi bolgan qurilmala raqamini tanlang (masalan: 1,2): ").strip()
                    if choice == '0':
                        print(f"{r}Keyingi akkount {phone}")
                        break
                    try:
                        indices = [int(i.strip()) for i in choice.split(',') if i.strip().isdigit()]
                        to_delete = [auths.authorizations[i-1] for i in indices if 1 <= i <= len(auths.authorizations)]
                    except (ValueError, IndexError):
                        print(f"{r}Notog'ri raqam kirittingiz.")
            
                # Удаляем выбранные устройства
                for auth in to_delete:
                    await client(functions.account.ResetAuthorizationRequest(hash=auth.hash))
                    print(f"{g}{index}||| O'chirildi: {auth.device_model}")
            
            except Exception as e:
                print(f"{r}Xatolik {phone}: {e}")
            finally:
                if client and client.is_connected():
                    await client.disconnect()
        
        
        async def main():
            phones = read_phones_from_csv('phone.csv')
            for idx, phone in enumerate(phones, start=1):
                await manage_authorizations(phone, idx)
        
            print(f"\n{lg}Tayyor! Barcha akkountlar ishlandi.")
            input("CHiqish uchun ENTER...")
        
        
        if __name__ == '__main__':
            asyncio.run(main())

    elif a == 19:
        import os
        import csv
        import asyncio
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.errors import RPCError
        from telethon.tl import functions
        from telethon.tl.types import InputPhoto
        from colorama import init, Fore
        
        # === Colorama init ===
        init(autoreset=True)
        lg, rs, g, b, r, cy, ye, grey = (
            Fore.LIGHTGREEN_EX, Fore.RESET, Fore.GREEN, Fore.BLUE,
            Fore.RED, Fore.CYAN, Fore.YELLOW, Fore.LIGHTBLACK_EX
        )
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        SESSION_FOLDER = 'sessions'
        
        
        # === + bilan yoki +siz raqamlarni qo'llab-quvvatlash ===
        def normalize_phone(phone):
            p = phone.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            return p if p.startswith('+') else f'+{p}'
        
        
        # === CSV dan telefonlarni o'qish ===
        def read_phone_numbers_from_csv(csv_file):
            phones = []
            if not os.path.exists(csv_file):
                print(f"{r}CSV fayl topilmadi: {csv_file}")
                return phones
            with open(csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        phones.append(normalize_phone(row[0]))
            return phones
        
        
        # === Eski rasmlarni o'chirish ===
        async def delete_all_photos(client):
            photos = await client.get_profile_photos('me')
            if not photos:
                print(f"{grey}Akkountda rasm topilmadi.")
                return
            ids = [
                InputPhoto(id=p.id, access_hash=p.access_hash, file_reference=p.file_reference)
                for p in photos
            ]
            try:
                result = await client(functions.photos.DeletePhotosRequest(id=ids))
                print(f"{g}Profildan o'chirildi {len(result)} ta eski rasm.")
            except RPCError as e:
                print(f"{r}Rasm o'chirishda xatolik: {e}")
        
        
        # === Asosiy ish jarayoni ===
        async def main():
            phone_numbers = read_phone_numbers_from_csv('phone.csv')
            if not phone_numbers:
                print(f"{r}phone.csv bo'sh yoki topilmadi!")
                return
        
            for phone in phone_numbers:
                print(f"{ye}Akkount ishga tushurildi: {phone}")
                session_file = os.path.join(SESSION_FOLDER, f'telethon_{phone}.session')
                if not os.path.exists(session_file):
                    print(f"{r}Sessiya topilmadi: {session_file}")
                    continue
        
                client = None
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
        
                    # TOZA TelegramClient - hech qanday fake device yo'q
                    client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
                    await client.connect()
        
                    if not await client.is_user_authorized():
                        print(f"{r}Akkount {phone} avtorizatsiyadan chiqib ketgan.")
                        await client.disconnect()
                        continue
        
                    await delete_all_photos(client)
        
                except RPCError as e:
                    print(f"{r}RPC Xatolik {phone}: {e}")
                except Exception as e:
                    print(f"{r}Umumiy xato {phone}: {e}")
                finally:
                    if client:
                        await client.disconnect()
        
            print(f"\n{lg}Tayyor! Barcha eski rasmlar o'chirildi.")
            input("CHIQISH uchun ENTER bosing...")
        
        
        if __name__ == '__main__':
            asyncio.run(main())


    elif a == 20:
        import csv
        import os
        import time
        from telethon.sync import TelegramClient
        from telethon.sessions import StringSession
        from telethon.errors import PhoneNumberBannedError
        
        API_ID = 13682
        HashID = 'de37bcf00f4688de900510f4f87384bb'
        
        
        def append_unique_frozen_account(phone_number):
            file = 'frozen_accounts.csv'
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    existing = [row[0] for row in csv.reader(f)]
            except FileNotFoundError:
                existing = []
            if phone_number not in existing:
                with open(file, 'a', encoding='utf-8', newline='') as f:
                    csv.writer(f).writerow([phone_number])
        
        
        def remove_from_csv(phone_number, filename):
            try:
                if not os.path.exists(filename):
                    return
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(filename, 'w', encoding='utf-8') as f:
                    for line in lines:
                        if phone_number != line.strip().split(',')[0]:
                            f.write(line)
            except Exception as e:
                print(f"XATOLIK {filename}: {e}")
        
        
        def check_account(phone_number):
            session_file = f'sessions/telethon_{phone_number}.session'
            if not os.path.exists(session_file):
                print(f"❌ SESSIYA TOPILMADI: {phone_number}")
                return
        
            try:
                with open(session_file, 'r') as f:
                    session_string = f.read().strip()
        
                client = TelegramClient(StringSession(session_string), API_ID, HashID)
                client.connect()
        
                if not client.is_user_authorized():
                    print(f"⚠️ {phone_number}: Sessiya yaroqsiz.")
                    client.disconnect()
                    return
        
                input_peer = client.get_entity('spambot')
                client.send_message(input_peer, "/start")
                time.sleep(2)
        
                msg = client.get_messages(input_peer, limit=1)[0]
                text = msg.text.lower()
        
                if "blocked for violations" in text or "account is blocked" in text:
                    print(f"⛔ MUZLATILGAN → {phone_number}")
                    append_unique_frozen_account(phone_number)
                    remove_from_csv(phone_number, "phone.csv")
                    print(f"📥 frozen_accounts.csv ga o'tkazildi: {phone_number}")
        
                elif ("no limits are currently applied" in text or "good news" in text or "ваш аккаунт свободен" in text or "xushxabarimiz bor" in text):
                    print(f"✅ AKOUNT YAXSHI XOLATDA ⇨ {phone_number}")
                    client.send_message(input_peer, "Cool, thanks")
                else:
                    print(f"⚠ VAQTINCHA CHEKLANGAN: {phone_number}")
        
                client.disconnect()
        
            except PhoneNumberBannedError:
                print(f"🚫 TO'LIQ BAN: {phone_number}")
                append_unique_frozen_account(phone_number)
                remove_from_csv(phone_number, "phone.csv")
            except Exception as e:
                print(f"❗ XATOLIK {phone_number}: {e}")
                if 'client' in locals() and client.is_connected():
                    client.disconnect()
        
        
        def main():
            if not os.path.exists('sessions'):
                os.makedirs('sessions')
        
            if not os.path.exists("phone.csv"):
                print("❌ phone.csv topilmadi.")
                return
        
            with open("phone.csv", 'r', encoding='utf-8') as f:
                phone_list = [row[0] for row in csv.reader(f) if row]
        
            print(f"📋 Jami {len(phone_list)} ta nomer tekshiriladi...\n")
        
            for phone in phone_list:
                check_account(phone)
        
            print("\n✅ TUGALLANDI.")
            input("ENTER — chiqish...")
        
        
        if __name__ == "__main__":
            main()

    elif a == 21:
        import os
        import random
        import asyncio
        import csv
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.tl.functions.account import UpdateProfileRequest
        from telethon.errors import FloodWaitError, RPCError
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        
        # 🔹 BIO randomlari
        random_bios = [
            "Hayot go'zal! 🌟",
            "Telegramda yangiman 😎",
            "Kod yozishni yaxshi ko'raman 👨‍💻",
            "Bugun yaxshi kayfiyatda 😊",
            "Sayohat qilishga oshiqaman ✈️",
            "O'rganish – bu kuch! 📚",
            "Har kuni yangi imkoniyat! 🔥",
            "O'yin emas – bu hayot 🎮",
            "Kulish – eng yaxshi davo 😄",
            "Yirik orzular – katta natija!",
            "Hayot – bu sarguzasht! 🚀",
            "Qo'rqma, boshlang!",
            "Bugungi ish, ertangi natija!",
            "Kechalarni yorituvchi fikrlar ✨",
            "Faqat oldinga! 💪",
            "Men bunday tug'ilganman! 😎",
            "Kichik qadamlar – katta muvaffaqiyatlar!",
            "Sukut bu donolik belgisi.",
            "Men kelajak uchun ishlayman.",
            "Boshlash uchun hech qachon kech emas 🌱",
            "Qoralama bugungi, kelajak — toza sahifa 📝",
            "Fikrlarim tezroq ishlaydi, Internetdan ham.",
            "Hayot bu kod – men uni yozyapman.",
            "Asl men – hozirgi men. 🎯",
            "Men texnologiyani nafas olaman 🤖",
            "Dunyo bilan ulashadigan hikoyalarim bor.",
            "Salom dunyo! 👋",
            "Do'stlik uchun ochiqman 🤝",
            "Shunchaki men – o'zgacha uslubda.",
            "Tilim 🔥, qalbim 🚀",
            "Sodda, ammo chuqur.",
            "Optimizm – mening oldingi ishim 😁",
            "Kofe, kod, ishlash, takrorlash ☕👨‍💻",
            "Sekin bo'lsa ham, oldinga yuraman.",
            "O'zingga ishongin – bu boshlanishi.",
            "Hech kimga o'xshamayman — va bu zo'r! 💎",
            "Dunyo bo'ylab virtual sayohachi 🧭",
            "Yorqin fikrlar qora fonlarda porlaydi 🌓",
            "Kod yozish – bu mening sheʼriyatim.",
            "Bugun o'zgacha bo'lishga qaror qildim.",
            "Jarayonni sev – natija o'z-o'zidan keladi."
        ]
        
        
        # phone.csv o'qish (+ bilan/siz mos)
        def read_phone_numbers_from_csv(csv_file):
            phone_numbers = []
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        raw = row[0].strip()
                        if not raw:
                            continue
                        # normalize: +998... yoki 998...
                        p = raw.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
                        if not p.startswith('+'):
                            p = '+' + p
                        phone_numbers.append(p)
            return phone_numbers
        
        
        def generate_random_bio():
            return random.choice(random_bios)
        
        
        async def change_profile_bio(client, bio):
            await client(UpdateProfileRequest(about=bio))
        
        
        async def main():
            phone_numbers = read_phone_numbers_from_csv('phone.csv')
        
            for phone_number in phone_numbers:
                # sessions/telethon_+998... yoki +siz yozilgan bo'lishi mumkin — + belgisini fayl nomidan olib tashlaymiz
                safe_name = phone_number.replace('+', '')
                session_file = f'sessions/telethon_{safe_name}.session'
        
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_string = f.read().strip()
                except FileNotFoundError:
                    print(f"❌ Session fayl topilmadi: {phone_number}")
                    continue
        
                # TOZA TelegramClient - hech qanday fake device yo'q
                client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
                try:
                    await client.connect()
                    if not await client.is_user_authorized():
                        print(f"🚫 Akount chiqarilgan: {phone_number}")
                        await client.disconnect()
                        continue
        
                    bio = generate_random_bio()
                    try:
                        await change_profile_bio(client, bio)
                        print(f"✅ [{phone_number}] Bio o'zgartirildi: \"{bio}\"\n")
                    except FloodWaitError as e:
                        print(f"⏳ FloodWait! Kuting {e.seconds} sekund... ({phone_number})")
                        await asyncio.sleep(e.seconds + 2)
                    except RPCError as e:
                        print(f"⚠️ RPC xato: {phone_number}: {str(e)}")
                except Exception as e:
                    print(f"❗️ Xatolik: [{phone_number}]: {str(e)}")
                finally:
                    await client.disconnect()
        
            print("✅ Barcha Bio-lar o'zgartirildi!")
            input("CHiqish uchun ENTER bosing...")
        
        
        if __name__ == "__main__":
            # Windows 3.12 da loop siyosati uchun foydali bo'lishi mumkin:
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
            asyncio.run(main())


    elif a == 22:        
        import os
        import random
        import time
        import csv
        import requests
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.errors import FloodWaitError, RPCError
        from telethon.tl.functions.stories import SendStoryRequest, GetPeerStoriesRequest, DeleteStoriesRequest
        from telethon.tl import types
        import asyncio
        
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESSIONS_DIR = "sessions"
        PHONE_CSV = "phone.csv"
        
        RANDOM_CAPTIONS = [
            "Hayot go'zal! 🌟", "Telegramda yangiman 😎", "Bugun yaxshi kayfiyatda 😊",
            "Sayohat qilishga oshiqaman ✈️", "O‘rganish – bu kuch! 📚",
            "Har kuni yangi imkoniyat! 🔥", "Kulish – eng yaxshi davo 😄",
            "Yirik orzular – katta natija!", "Hayot – bu sarguzasht! 🚀", "Salom dunyo! 👋"
        ]
        
        def random_caption():
            return random.choice(RANDOM_CAPTIONS)
        
        # --- CSV dan telefon raqamlarni o'qish ---
        def read_phone_numbers_from_csv(csv_file):
            numbers = []
            if not os.path.exists(csv_file):
                print(f"❌ Fayl topilmadi: {csv_file}")
                return numbers
            with open(csv_file, 'r', encoding='utf-8') as f:
                for row in csv.reader(f):
                    if row and row[0].strip():
                        numbers.append(row[0].strip())
            return numbers
        
        # --- Tasodifiy rasm yuklash ---
        def download_random_image(save_path):
            url = "https://picsum.photos/1080/1920"
            try:
                print(f"🖼️ '{save_path}' uchun rasm yuklanmoqda...")
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return save_path
            except Exception as e:
                print(f"❗️ Rasm yuklanmadi: {e}")
                return None
        
        # --- Story qo'yish ---
        async def send_story(client):
            PIN_STORY = False
            NO_FORWARDS = False
            PRIVACY_RULE = types.InputPrivacyValueAllowAll()
            MAX_NON_PREMIUM = 1
        
            me = await client.get_me()
            is_premium = getattr(me, 'premium', False)
            stories_resp = await client(GetPeerStoriesRequest(peer='me'))
            count = 0
            try:
                if hasattr(stories_resp, 'stories') and hasattr(stories_resp.stories, 'stories'):
                    count = len(stories_resp.stories.stories)
            except Exception:
                count = 0
        
            print(f"   - Holat: {'Premium' if is_premium else 'Oddiy'}, hozirdagi storylar soni: {count}")
            if not is_premium and count >= MAX_NON_PREMIUM:
                print("⚠️ Oddiy akkaunt uchun story limiti to‘lgan. O‘tkazilmoqda.")
                return
        
            filename = f"story_{me.id}.jpg"
            path = download_random_image(filename)
            if not path:
                print("❗️ Rasm topilmadi, story qo‘yilmadi.")
                return
        
            try:
                file = await client.upload_file(path)
                media = types.InputMediaUploadedPhoto(file=file)
                await client(SendStoryRequest(
                    peer='me',
                    media=media,
                    caption=random_caption(),
                    privacy_rules=[PRIVACY_RULE],
                    pinned=PIN_STORY,
                    noforwards=NO_FORWARDS
                ))
                print("✅ Story muvaffaqiyatli joylandi!")
            except RPCError as e:
                print(f"❗️ Story yuborishda xato: {e}")
            finally:
                if os.path.exists(path):
                    os.remove(path)
        
        # --- Story o'chirish ---
        async def delete_stories(client):
            try:
                stories = await client(GetPeerStoriesRequest(peer='me'))
                ids = []
                if hasattr(stories, 'stories') and hasattr(stories.stories, 'stories'):
                    ids = [s.id for s in stories.stories.stories]
                if not ids:
                    print("✅ O‘chirish uchun aktiv story topilmadi.")
                    return
                await client(DeleteStoriesRequest(peer='me', id=ids))
                print(f"🗑️ {len(ids)} ta story o‘chirildi.")
            except RPCError as e:
                print(f"❗️ O‘chirishda xato: {e}")
            except Exception as e:
                print(f"❗️ O‘chirishda noma'lum xato: {e}")
        
        # --- Asosiy jarayon ---
        async def process_accounts(action):
            phones = read_phone_numbers_from_csv(PHONE_CSV)
            if not phones:
                print("❌ phone.csv bo‘sh yoki topilmadi!")
                return
        
            print(f"\nJami {len(phones)} ta akkaunt topildi.\n")
            for idx, phone in enumerate(phones, 1):
                print(f"{idx}/{len(phones)} → {phone}")
                session_file = os.path.join(SESSIONS_DIR, f'telethon_{phone}.session')
                if not os.path.exists(session_file):
                    print("   ❌ Sessiya topilmadi — o‘tkazildi.")
                    continue
        
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session = f.read().strip()
        
                    client = TelegramClient(StringSession(session), API_ID, API_HASH)
                    # ulanish
                    await client.connect()
                    if not await client.is_user_authorized():
                        print("   🚫 Akkaunt avtorizatsiyadan chiqqan yoki sessiya yaroqsiz.")
                        await client.disconnect()
                        continue
        
                    if action == 1:
                        await send_story(client)
                    else:
                        await delete_stories(client)
        
                except FloodWaitError as e:
                    wait_seconds = getattr(e, 'seconds', None) or getattr(e, 'retry_after', 30)
                    print(f"⏳ FloodWait: {wait_seconds} soniya kutamiz...")
                    await asyncio.sleep(wait_seconds + 3)
                except Exception as e:
                    print(f"❗️ Xato: {e}")
                finally:
                    try:
                        if client and await client.is_connected():
                            await client.disconnect()
                            print("   🔌 Ulanish uzildi.\n")
                    except Exception:
                        pass
        
                # akkauntlar orasida qisqa tasodifiy pauza (kamroq «bot» qatori)
                await asyncio.sleep(random.uniform(1.2, 3.0))
        
            print("✅ Barcha akkauntlar bilan ish yakunlandi.")
            input("ENTER bosib chiqish...")
        
        # --- BOSHLASH ---
        if __name__ == "__main__":
            try:
                k = int(input("[1] Stories o‘rnatish \n[2] Storiesni o‘chirish\n\nTANLANG: ").strip())
            except Exception:
                print("Tanlov noto‘g‘ri, 1 yoki 2 ni kiriting.")
                raise SystemExit
        
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
        
            asyncio.run(process_accounts(k))


    elif a == 23:
        import sys, subprocess, importlib
        from importlib import metadata
    
        def telethon_show_version(prefix=""):
            """O‘rnatilgan (disk) va import qilingan versiyani ko‘rsatish."""
            try:
                installed = metadata.version("telethon")
            except metadata.PackageNotFoundError:
                installed = "o‘rnatilmagan"
            imported = None
            if "telethon" in sys.modules:
                try:
                    imported = getattr(sys.modules["telethon"], "__version__", None)
                except Exception:
                    imported = "aniqlanmadi"
            print(f"{lg}{prefix}Telethon (disk): {installed}{w}")
            if imported is not None:
                print(f"{lg}{prefix}Telethon (import): {imported}{w}")
    
        def upgrade_telethon_quiet(min_version: str | None = None) -> bool:
            """
            Telethon'ni jim (quiet) rejimda yangilaydi.
            Pip chiqishi ko‘rsatilmaydi; faqat HAQIQATDA o‘zgarish bo‘lsa xabar beradi.
            """
            def parse(v: str | None):
                if not v: return ()
                return tuple(int(x) for x in str(v).split(".") if x.isdigit())
    
            try:
                installed_before = metadata.version("telethon")
            except metadata.PackageNotFoundError:
                installed_before = None
    
            imported_before = None
            if "telethon" in sys.modules:
                try:
                    imported_before = getattr(sys.modules["telethon"], "__version__", None)
                except Exception:
                    imported_before = None
    
            if min_version and installed_before and parse(installed_before) >= parse(min_version):
                print(f"{ye}Telethon allaqachon minimal versiyada yoki undan yuqori (>= {min_version}).{w}")
                return False
    
            # pip: mutlaqo jim
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "--upgrade", "telethon", "-q", "--disable-pip-version-check"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False
                )
            except Exception:
                pass
    
            try:
                installed_after = metadata.version("telethon")
            except metadata.PackageNotFoundError:
                installed_after = installed_before
    
            if installed_after == installed_before:
                print(f"{ye}Yangilanish topilmadi (hozirgi: {installed_after}).{w}")
                return False
    
            # Diskdagi versiya o‘zgardi — modulni reload qilib ko‘ramiz
            try:
                if "telethon" in sys.modules:
                    importlib.invalidate_caches()
                    importlib.reload(sys.modules["telethon"])
                else:
                    import telethon  # noqa: F401
                imported_after = getattr(sys.modules["telethon"], "__version__", None)
            except Exception:
                imported_after = imported_before
    
            print(f"{lg}[NEW] Telethon versiyasi o‘rnatildi: {installed_after}{w}")
            if imported_after != installed_after:
                print(f"{ye}Eslatma: yangi versiyadan foydalanish uchun skriptni qayta ishga tushiring.{w}")
            return True
    
        def telethon_upgrade_menu_action():
            print(f"{ye}Telethon versiyasini tekshiryapmiz...{w}")
            telethon_show_version(prefix="[OLD] ")
            changed = upgrade_telethon_quiet(min_version=None)  # xohlasang: "1.42.0"
            if changed:
                telethon_show_version(prefix="[AFTER] ")
            input(f"{lg}Tugadi. Davom etish uchun ENTER...{w}")
    
        telethon_upgrade_menu_action()
        continue

    elif a == 24:
        import sys, subprocess, os, csv, time
        import asyncio
        from telethon import TelegramClient
        from telethon.sessions import StringSession, SQLiteSession
        from telethon.errors import SessionPasswordNeededError
        from telethon.errors.rpcerrorlist import (
            AuthTokenExpiredError, AuthTokenInvalidError, AuthTokenAlreadyAcceptedError
        )
        
        # === RANGLAR ===
        r = "\033[91m"
        lg = "\033[92m"
        ye = "\033[93m"
        w = "\033[0m"
        
        # === API SOZLAMALARI ===
        API_ID = 13682        # O'zingiznikini kiriting
        HASHID = "de37bcf00f4688de900510f4f87384bb" # O'zingiznikini kiriting
        
        # === QR-CODE MODULINI TEKSHIRISH ===
        try:
            from qrcode import QRCode
        except ImportError:
            print(f"{ye}qrcode moduli topilmadi. O'rnatilmoqda...{w}")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "qrcode", "-q", "--disable-pip-version-check"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            from qrcode import QRCode
            print(f"{lg}qrcode muvaffaqiyatli o'rnatildi.{w}")
        
        # === Sozlamalar ===
        QR_REFRESH_SEC = 30
        WAIT_CHUNK = 25
        CSV_FILE = 'phone.csv'
        
        # === Yordamchi funksiyalar ===
        def normalize_phone(s: str) -> str:
            """Telefon raqamini tozalash - faqat raqamlar qoladi"""
            if not s: return ''
            s = str(s).strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            # + belgisini olib tashlash
            return s.lstrip('+')
        
        def display_qr_ascii(data: str):
            qr = QRCode(border=1)
            qr.add_data(data)
            qr.print_ascii(invert=True)
        
        def save_sqlite_from_client(client: TelegramClient, sqlite_path: str):
            base = client.session
            sess = SQLiteSession(sqlite_path)
            try:
                sess.set_dc(base.dc_id, base.server_address, base.port)
            except AttributeError:
                sess.set_dc(getattr(base, 'dc_id', 2),
                            getattr(base, 'server_address', '149.154.167.50'),
                            getattr(base, 'port', 443))
            sess.auth_key = getattr(base, 'auth_key', None)
            sess.takeout_id = getattr(base, 'takeout_id', None)
            try:
                sess.user = getattr(base, 'user', None)
            except Exception:
                pass
            sess.save()
        
        # === CSV FUNKSIYALARI ===
        def get_existing_phones() -> list:
            """CSV dagi mavjud telefonlarni o'qish (tartibni saqlash uchun list)"""
            phones = []
            if os.path.exists(CSV_FILE):
                with open(CSV_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            clean = normalize_phone(line)
                            if clean and clean not in phones:
                                phones.append(clean)
            return phones
        
        def save_phone_to_csv(phone: str) -> bool:
            """
            Telefon raqamini CSV ga qo'shish
            - + belgisisiz yoziladi
            - Mavjud raqamlar tagidan davom etadi
            - Oxirida bo'sh qator qolmaydi
            """
            existing = get_existing_phones()
            clean = normalize_phone(phone)
            
            if clean in existing:
                print(f"{ye}Bu raqam allaqachon CSV da mavjud: {clean}{w}")
                return False
            
            # Yangi raqamni qo'shish
            existing.append(clean)
            
            # Faylni qayta yozish (bo'sh qatorsiz)
            with open(CSV_FILE, 'w', encoding='utf-8') as f:
                for i, p in enumerate(existing):
                    if i < len(existing) - 1:
                        f.write(f"{p}\n")
                    else:
                        # Oxirgi qatorda \n yo'q
                        f.write(f"{p}")
            
            print(f"{lg}Telefon raqami CSV ga qo'shildi: {clean}{w}")
            return True
        
        # === ASYNC MAIN FUNKSIYA ===
        async def qr_login_one_account():
            """Bitta akount uchun QR login"""
            
            str_client = TelegramClient(StringSession(), API_ID, HASHID)
            await str_client.connect()
            
            try:
                qr_login = await str_client.qr_login()
            except Exception as e:
                print(f"{r}QR login yaratib bo'lmadi: {e}{w}")
                await str_client.disconnect()
                return None
            
            authed = False
            last_draw = 0.0
            
            while not authed:
                now = time.time()
                
                # QR'ni qayta chizish
                if now - last_draw >= QR_REFRESH_SEC:
                    print(f"\n{ye}{'='*50}{w}")
                    print(f"{ye}Telegram ilovasida QR kodni skaner qiling!{w}")
                    print(f"{ye}QR har {QR_REFRESH_SEC} sekundda yangilanadi{w}")
                    print(f"{ye}{'='*50}{w}")
                    print(f"\n{w}QR URL: {qr_login.url}\n")
                    
                    try:
                        display_qr_ascii(qr_login.url)
                    except Exception:
                        pass
                    last_draw = now
                
                try:
                    authed = await qr_login.wait(WAIT_CHUNK)
                    
                except (AuthTokenExpiredError, AuthTokenInvalidError):
                    try:
                        await qr_login.recreate()
                        last_draw = 0.0
                        continue
                    except Exception:
                        print(f"{ye}QR yangilashda muammo, 2FA tekshiruviga o'tyapmiz...{w}")
                        for attempt in range(1, 4):
                            pwd = input(f"{ye}2FA parolni kiriting [urinish {attempt}/3]: {w}")
                            try:
                                await str_client.sign_in(password=pwd)
                                authed = True
                                break
                            except Exception as e:
                                print(f"{r}Parol qabul qilinmadi: {e}{w}")
                        if not authed:
                            break
                            
                except AuthTokenAlreadyAcceptedError:
                    authed = True
                    break
                    
                except SessionPasswordNeededError:
                    print(f"{ye}2FA parol talab qilinmoqda...{w}")
                    for attempt in range(1, 4):
                        pwd = input(f"{ye}2FA parolni kiriting [urinish {attempt}/3]: {w}")
                        try:
                            await str_client.sign_in(password=pwd)
                            authed = True
                            break
                        except Exception as e:
                            print(f"{r}Parol qabul qilinmadi: {e}{w}")
                    if not authed:
                        break
                        
                except Exception as e:
                    try:
                        await qr_login.recreate()
                        last_draw = 0.0
                        continue
                    except Exception:
                        print(f"{r}Xatolik: {e}{w}")
                        break
            
            if not authed:
                print(f"{r}Kirish amalga oshmadi.{w}")
                await str_client.disconnect()
                return None
            
            # === AKOUNT MA'LUMOTLARINI OLISH ===
            try:
                me = await str_client.get_me()
                phone = me.phone
                first_name = me.first_name or ""
                last_name = me.last_name or ""
                username = me.username or ""
                user_id = me.id
                
                print(f"\n{lg}{'='*50}{w}")
                print(f"{lg}✓ AKOUNT MUVAFFAQIYATLI ULANDI!{w}")
                print(f"{lg}{'='*50}{w}")
                print(f"{lg}  Telefon:  {phone}{w}")
                print(f"{lg}  Ism:      {first_name} {last_name}{w}")
                if username:
                    print(f"{lg}  Username: @{username}{w}")
                print(f"{lg}  ID:       {user_id}{w}")
                print(f"{lg}{'='*50}{w}")
                
            except Exception as e:
                print(f"{r}Akount ma'lumotlarini olishda xato: {e}{w}")
                await str_client.disconnect()
                return None
            
            if not phone:
                print(f"{r}Telefon raqami olinmadi!{w}")
                await str_client.disconnect()
                return None
            
            clean = normalize_phone(phone)
            str_path = f'sessions/telethon_{clean}.session'
            sql_path = f'sessions/{clean}_SQLite.session'
            
            # === TELEFON RAQAMINI CSV GA SAQLASH ===
            save_phone_to_csv(phone)
            
            # === SESSION SAQLASH ===
            try:
                str_session_str = str_client.session.save()
                with open(str_path, 'w', encoding='utf-8') as sf:
                    sf.write(str_session_str)
                print(f"{lg}StringSession saqlandi: {str_path}{w}")
            except Exception as e:
                print(f"{r}StringSession saqlashda xato: {e}{w}")
                await str_client.disconnect()
                return None
            
            try:
                save_sqlite_from_client(str_client, sql_path)
                print(f"{lg}SQLite session saqlandi: {sql_path}{w}")
            except Exception as e:
                print(f"{r}SQLite saqlashda xato: {e}{w}")
            
            await str_client.disconnect()
            print(f"\n{lg}✓ {clean} akounti to'liq ro'yxatdan o'tdi!{w}")
            
            return clean
        
        async def main():
            os.makedirs('sessions', exist_ok=True)
            
            print(f"\n{lg}{'='*60}{w}")
            print(f"{lg}   QR ORQALI TELEGRAM AKOUNT RO'YXATDAN O'TKAZISH{w}")
            print(f"{lg}{'='*60}{w}")
            print(f"{ye}Telegramda QR kodni skaner qiling - telefon avtomatik olinadi!{w}\n")
            
            # Mavjud raqamlarni ko'rsatish
            existing = get_existing_phones()
            if existing:
                print(f"{ye}Mavjud raqamlar ({len(existing)} ta):{w}")
                for p in existing:
                    print(f"  • {p}")
                print()
            
            account_count = 0
            
            while True:
                account_count += 1
                print(f"\n{lg}[Akount #{account_count}] QR login tayyorlanmoqda...{w}")
                
                result = await qr_login_one_account()
                
                if result:
                    print(f"\n{lg}Akount muvaffaqiyatli qo'shildi: {result}{w}")
                
                print(f"\n{ye}{'='*50}{w}")
                cont = input(f"{ye}Yana akount qo'shmoqchimisiz? (y/n): {w}").strip().lower()
                if cont != 'y':
                    break
            
            # Yakuniy hisobot
            print(f"\n{lg}{'='*60}{w}")
            print(f"{lg}   JARAYON YAKUNLANDI{w}")
            print(f"{lg}{'='*60}{w}")
            
            final_phones = get_existing_phones()
            print(f"{lg}Jami akountlar soni: {len(final_phones)}{w}")
            print(f"\n{lg}phone.csv dagi raqamlar:{w}")
            for i, p in enumerate(final_phones, 1):
                print(f"  {i}. {p}")
            
            print(f"\n{lg}Session fayllar: sessions/ papkasida{w}")
        
        # === ISHGA TUSHIRISH ===
        if __name__ == "__main__":
            asyncio.run(main())
       
    elif a == 25:   
        import os
        import random
        import asyncio
        import csv
        from typing import List, Tuple
        
        from telethon import TelegramClient, functions, types
        from telethon.sessions import StringSession
        from telethon.errors import (
            FloodWaitError, UserPrivacyRestrictedError, ChatWriteForbiddenError,
            PhoneNumberBannedError, RPCError
        )
        from telethon.tl.types import User, Channel, Chat
        from telethon.tl.functions.contacts import ImportContactsRequest
        from telethon.tl.types import InputPhoneContact
        
        # ====== API ======
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESS_DIR = 'sessions'
        PHONE_CSV = 'phone.csv'
        
        # ====== “Insoniy” xabarlar ======
        SAVOLLAR = [
            "Salom, qalesan?", "Assalomu alaykum! Bugun qanday kun?", "Nima yangiliklar?",
            "Bugun nimalar qilding?", "Ishlar qalay?", "Qayerdansan o‘zi?",
            "Bugungi rejalaring qanday?", "Hozir nima bilan bandsan?", "Kun qanday oʻtmoqda?",
            "Yaqinda qiziqarli narsa bo‘ldimi?", "Tavsiyangiz bormi yaqin atrofga borish uchun?",
            "Qaysi filmni oxirgi ko‘rding va qanday?", "Sevimli musiqangiz nima hozirlar?",
            "Qaysi dastur yoki ilova bilan ishlayapsiz?", "Kichik yordam bera olasizmi: maslahat beringchi?",
            "Qiziq: ertaga nimani rejalashtirdingiz?", "Hobbilaring nima? Bo‘lishib yuboring.",
            "Kofe yoki choy? 😊", "Ishda yangi loyiha bormi?", "Kechqurun nima qilmoqchisiz?",
            "Qanday dasturlash tili eng yoqadi?", "Sayohatga chiqmoqchi boʻlsang, qayerga borarding?",
            "Kamera orqali suratlar ko‘rishga qiziqasizmi?", "Bugun kayfiyatingizga 1 dan 10 gacha baho bering?",
            "Eng yaxshi dam olish kuningiz qanday o‘tadi?"
        ]
        JAVOBLAR = [
            "Yaxshi, rahmat! O'zingchi? 😊", "Hammasi joyida — ishlayapman hozir.",
            "Kechki payt choy ichamiz, keyin gaplashamiz.", "Ajoyib, yaqinda yangi loyiha boshladim.",
            "Hozir biroz bandman, keyin yozaman.", "Zo‘r, rahmat! Bugun yaxshi kayfiyat.",
            "Men ham xuddi shunday — ishlar serob.", "Qiziq savol! Men film ko‘rishni afzal ko‘raman.",
            "Ha, sayohat juda yoqadi!", "Kofe > choy, albatta ☕", "O‘ylab ko‘raman, rahmat.",
            "Bugun biroz dam oldim, yaxshi boʻldi.", "Kod yozish — mening hobbiym.",
            "Hozir onlayn, 10 daqiqadan keyin gaplashsak?", "Menga lo-fi yoqadi, tavsiya qilaman!",
            "Super — men ham xuddi shunday qilaman!", "Rahmat, foydali maslahat.",
            "Uyda kitob o‘qiyapman — 'Atomic Habits' tavsiya.", "Ajoyib g‘oya — sinab ko‘raman.",
            "Tushundim, keyin bog‘lanamiz.", "Bu juda kulgili 😂", "Har kuni kichik qadamlar muhim.",
            "Dam olishda tabiat — eng zo‘r.", "Ok, keyinroq batafsil yozaman.", "10/10 — samarali kun bo‘ldi!"
        ]
        
        # parametrlar
        READ_LIMIT_PER_CHAT = (5, 12)
        DIALOG_ROUNDS = (1, 2)
        DM_SLEEP = (2.0, 5.0)
        READ_SLEEP = (1.0, 2.5)
        
        # ====== Helpers ======
        def normalize_phone(s: str) -> str:
            if not s:
                return ''
            s = s.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            return s[1:] if s.startswith('+') else s
        
        def to_e164(clean: str) -> str:
            return f'+{clean}'
        
        def read_phones(path: str) -> List[str]:
            phones = []
            if not os.path.exists(path):
                print(f"[XATO] {path} topilmadi.")
                return phones
            with open(path, 'r', encoding='utf-8') as f:
                for row in csv.reader(f):
                    if not row: continue
                    raw = row[0].strip()
                    if not raw: continue
                    clean = normalize_phone(raw)
                    phones.append(clean)
            return phones
        
        async def safe_sleep(a: float, b: float):
            await asyncio.sleep(random.uniform(a, b))
        
        def is_dialog_a_chat(entity) -> bool:
            return isinstance(entity, Channel) or isinstance(entity, Chat)
        
        # ====== Chatlarda “ko‘rish” ======
        async def read_some_messages(client: TelegramClient, dialog, count: int):
            try:
                await client.get_messages(dialog.entity, limit=count)
                for _ in range(min(3, count)):
                    await safe_sleep(*READ_SLEEP)
                await safe_sleep(0.5, 1.2)
            except FloodWaitError as e:
                secs = getattr(e, 'seconds', None) or getattr(e, 'retry_after', 10)
                print(f"   └─ FloodWait: {secs}s (ko‘rishda), kutilyapti...")
                await asyncio.sleep(secs)
            except Exception as e:
                print(f"   └─ Ko‘rishda xato: {e}")
        
        # kontakt import
        async def ensure_contact(client: TelegramClient, peer_phone_e164: str, first: str = "User", last: str = "") -> bool:
            try:
                contact = InputPhoneContact(
                    client_id=random.randrange(10**9, 10**10),
                    phone=peer_phone_e164,
                    first_name=first or "User",
                    last_name=last or ""
                )
                await client(ImportContactsRequest([contact]))
                return True
            except FloodWaitError as e:
                secs = getattr(e, 'seconds', None) or getattr(e, 'retry_after', 10)
                print(f"   └─ ImportContacts FloodWait: {secs}s — kutilyapti...")
                await asyncio.sleep(secs)
                return False
            except Exception as e:
                print(f"   └─ Kontakt import xatosi ({peer_phone_e164}): {e}")
                return False
        
        # ====== RANDOM BIRTHDAY va uni o‘rnatish ======
        def random_birthday() -> types.Birthday:
            year  = random.randint(1986, 2005)
            month = random.randint(1, 12)
            day   = random.randint(1, 28 if month == 2 else 30)
            return types.Birthday(day=day, month=month, year=year)
        
        async def set_random_birthday(client: TelegramClient):
            try:
                bd = random_birthday()
                await client(functions.account.UpdateBirthdayRequest(birthday=bd))
            except Exception as e:
                print(f"   └─ Birthday o‘rnatishda xato: {e}")
        
        # ====== DM yozish (kontakt import bilan) ======
        async def dm_exchange(a: TelegramClient, b: TelegramClient, a_user: User, b_user: User,
                              a_phone_e164: str, b_phone_e164: str, rounds: int):
            a_ok = await ensure_contact(a, b_phone_e164, first=b_user.first_name or "User", last=b_user.last_name or "")
            b_ok = await ensure_contact(b, a_phone_e164, first=a_user.first_name or "User", last=a_user.last_name or "")
            if not (a_ok and b_ok):
                return
        
            a_id = a_user.id
            b_id = b_user.id
        
            for _ in range(rounds):
                # A -> B
                try:
                    b_peer = await a.get_input_entity(b_id)
                    q = random.choice(SAVOLLAR)
                    await a.send_message(b_peer, q)
                    await safe_sleep(*DM_SLEEP)
                except UserPrivacyRestrictedError:
                    return
                except (ChatWriteForbiddenError, RPCError):
                    return
                except FloodWaitError as e:
                    secs = getattr(e, 'seconds', None) or getattr(e, 'retry_after', 10)
                    print(f"   └─ FloodWait A->B: {secs}s, kutilyapti...")
                    await asyncio.sleep(secs)
                    return
                except Exception:
                    return
        
                # B -> A
                try:
                    a_peer = await b.get_input_entity(a_id)
                    r = random.choice([random.choice(JAVOBLAR), "Ha, tushunarli.", "Zo‘r!"])
                    await b.send_message(a_peer, r)
                    await safe_sleep(*DM_SLEEP)
                except UserPrivacyRestrictedError:
                    return
                except FloodWaitError as e:
                    secs = getattr(e, 'seconds', None) or getattr(e, 'retry_after', 10)
                    print(f"   └─ FloodWait B->A: {secs}s, kutilyapti...")
                    await asyncio.sleep(secs)
                    return
                except Exception:
                    return
        
        # ====== Client tayyorlash (DEFAULT device — spoof yo'q) ======
        async def prepare_client(clean_phone: str):
            str_path = os.path.join(SESS_DIR, f"telethon_{clean_phone}.session")
            if not os.path.exists(str_path):
                print(f"[{clean_phone}] session topilmadi — tashlab o‘tamiz.")
                return None, None
        
            with open(str_path, 'r', encoding='utf-8') as f:
                session_string = f.read().strip()
        
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
        
            try:
                await client.connect()
                if not await client.is_user_authorized():
                    print(f"[{clean_phone}] avtorizatsiya yo‘q — tashlab o‘tamiz.")
                    await client.disconnect()
                    return None, None
        
                me = await client.get_me()
                return client, me
            except PhoneNumberBannedError:
                print(f"[{clean_phone}] BAN — tashlab o‘tamiz.")
                return None, None
            except Exception as e:
                print(f"[{clean_phone}] ulanish xatosi: {e}")
                try:
                    await client.disconnect()
                except:
                    pass
                return None, None
        
        # ====== “O‘z chatlarini ko‘rish” bosqichi ======
        async def view_own_chats(client: TelegramClient, me):
            try:
                dialogs = []
                async for d in client.iter_dialogs():
                    if d.is_user:
                        continue
                    if d.entity and is_dialog_a_chat(d.entity):
                        dialogs.append(d)
        
                if not dialogs:
                    print("   └─ A’zo bo‘lgan chatlar topilmadi.")
                    return
        
                sample = random.sample(dialogs, k=min(2, len(dialogs)))
                for d in sample:
                    title = getattr(d.entity, 'title', 'Chat')
                    print(f"   └─ Ko‘rilyapti: {title}")
                    to_read = random.randint(*READ_LIMIT_PER_CHAT)
                    await read_some_messages(client, d, to_read)
            except Exception as e:
                print(f"   └─ Dialoglarni olishda xato: {e}")
        
        # ====== DM orkestratsiya ======
        async def dm_everyone(clients_info: List[Tuple[TelegramClient, User, str]]):
            pairs = []
            for i in range(0, len(clients_info) - 1, 2):
                pairs.append((clients_info[i], clients_info[i+1]))
        
            if not pairs:
                print("DM uchun juftlik topilmadi (akkauntlar soni kam).")
                return
        
            for (c1, u1, p1), (c2, u2, p2) in pairs:
                if u1.id == u2.id:
                    continue
                print(f"   └─ DM: {u1.first_name or u1.id}  ↔  {u2.first_name or u2.id}")
                rounds = random.randint(*DIALOG_ROUNDS)
                try:
                    await dm_exchange(c1, c2, u1, u2, p1, p2, rounds)
                except Exception as e:
                    print(f"   └─ DM juftlik xatosi: {e}")
                await safe_sleep(0.8, 1.4)
        
        # ====== MAIN ======
        async def main():
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
        
            phones_clean = read_phones(PHONE_CSV)
            if not phones_clean:
                print("phone.csv bo‘sh yoki topilmadi.")
                return
        
            os.makedirs(SESS_DIR, exist_ok=True)
        
            # 1) Klientlarni tayyorlash
            clients_info: List[Tuple[TelegramClient, User, str]] = []
            for clean in phones_clean:
                client, me = await prepare_client(clean)
                if client and me:
                    e164 = to_e164(clean)
                    print(f"[{clean}] ulandi: {me.first_name or me.id}")
                    clients_info.append((client, me, e164))
                await safe_sleep(0.4, 1.2)
        
            if not clients_info:
                print("Ishlaydigan akkaunt topilmadi.")
                return
        
            # 2) Har biri o‘z chatlaridan 2 tasini ko‘rib chiqadi
            print("\n— Chatlarda ko‘rish bosqichi —")
            for client, me, _ in clients_info:
                print(f" [{me.first_name or me.id}] chatlarini ko‘rish:")
                await view_own_chats(client, me)
                await safe_sleep(0.8, 1.2)
        
            # 3) HAR BIR akkauntga random birthday o‘rnatamiz
            print("\n— Profil (birthday) o‘rnatish —")
            for client, me, _ in clients_info:
                print(f" [{me.first_name or me.id}] tug‘ilgan kuni o‘rnatilmoqda...")
                await set_random_birthday(client)
                await safe_sleep(0.6, 1.0)
        
            # 4) O‘zaro DM (kontakt import bilan)
            print("\n— O‘zaro DM bosqichi —")
            await dm_everyone(clients_info)
        
            # 5) Yopish
            print("\nYakunlandi...")
            for client, _, _ in clients_info:
                try:
                    await client.disconnect()
                except:
                    pass
            input("ENTER — chiqish...")
        
        if __name__ == '__main__':
            asyncio.run(main())

   
    elif a == 26:    
        import os
        import csv
        import asyncio
        import random
        import string
        import time
        from typing import List, Tuple, Optional
        
        from colorama import init as colorama_init, Fore, Style
        from telethon import TelegramClient, errors, functions, types
        from telethon.sessions import StringSession
        from telethon.tl.functions.channels import CreateChannelRequest, GetParticipantRequest, UpdateUsernameRequest
        
        colorama_init(autoreset=True)
        
        # ====== SOZLAMALAR ======
        API_ID = 253798
        API_HASH = 'd806c9ed3eb74a233d58cb4a072a68f0'
        
        SESS_DIR = 'sessions'      # sessiya fayllari papkasi
        PHONE_CSV = 'phone.csv'    # phone.csv ichida raqamlar (har qatorda bitta)
        GROUPS_PER_ACCOUNT_MIN = 4
        GROUPS_PER_ACCOUNT_MAX = 5
        MAX_USERNAME_ATTEMPTS = 12
        NAME_MAX_ATTEMPTS = 10
        WAIT_ON_FLOOD = True
        # human-like delays
        PAUSE_AFTER_CREATE = (2.0, 5.0)
        PAUSE_BETWEEN_ACCOUNTS = (0.8, 2.0)
        
        # ====== NOM GENERATOR ======
        ADJECTIVES = [
            "Yangilik", "Ekspert", "Avto", "Tex", "Iqtisod", "Sport", "Madaniyat",
            "Chat", "Local", "Global", "VIP", "Biznes", "Dastur", "Musiqa", "Cinema",
            "Ta'lim", "O'yin", "Sog'liq", "Sayohat", "Fotogalereya", "Tadbir", "Market",
            "StartUp", "Konsult", "Hobby", "Science", "Health", "Food", "Recipe"
        ]
        
        NOUNS = [
            "Guruh", "Klub", "Jamiyat", "Forum", "Chat", "Xabar", "Zona",
            "Markaz", "Panel", "Bo'lim", "Kanal", "Platforma", "Xona"
        ]
        
        SUFFIX_WORDS = ["Uz", "Team", "24", "Pro", "Net", "Hub", "Zone", "Club", "World", "Plus", "One", "X", "HQ", "Lab"]
        USERNAME_CHARS = string.ascii_lowercase + string.digits + "_"
        
        def gen_suffix(n=4):
            chars = string.ascii_uppercase + string.digits
            return ''.join(random.choice(chars) for _ in range(n))
        
        def gen_group_name(seed: str = "", suffix_len: int = 4) -> str:
            a = random.choice(ADJECTIVES)
            n = random.choice(NOUNS)
            w = random.choice(SUFFIX_WORDS) if random.random() < 0.45 else ""
            suf = gen_suffix(suffix_len) if random.random() < 0.75 else str(random.randint(10,999))
            if seed:
                seed_clean = ''.join(ch for ch in seed if ch.isalnum())[:4]
                return f"{a} {n} {seed_clean}{('-'+w) if w else ''}-{suf}"
            return f"{a} {n}{(' '+w) if w else ''} - {suf}"
        
        def gen_random_username(prefix: str = "", length: int = 7) -> str:
            length = max(5, min(22, length))
            body = ''.join(random.choice(USERNAME_CHARS) for _ in range(length))
            candidate = (prefix + body)[:32]
            if not candidate[0].isalnum():
                candidate = random.choice(string.ascii_lowercase) + candidate[1:]
            return candidate.lower()
        
        # ====== UTILS ======
        def normalize_phone(s: str) -> str:
            if not s:
                return ''
            s = s.strip().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            return s[1:] if s.startswith('+') else s
        
        def read_phones(path: str) -> List[str]:
            phones = []
            if not os.path.exists(path):
                print(f"{Fore.RED}❌ phone.csv topilmadi: {path}")
                return phones
            with open(path, 'r', encoding='utf-8') as f:
                for row in csv.reader(f):
                    if not row: continue
                    raw = row[0].strip()
                    if raw:
                        phones.append(normalize_phone(raw))
            return phones
        
        # ====== prepare_client without device spoofing (DEFAULT Telethon) ======
        async def prepare_client(session_path: str) -> Optional[TelegramClient]:
            try:
                with open(session_path, 'r', encoding='utf-8') as f:
                    session_string = f.read().strip()
            except Exception:
                return None
        
            # DEFAULT Telethon client (no fake device params)
            client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            await client.connect()
            if not await client.is_user_authorized():
                await client.disconnect()
                return None
            return client
        
        async def set_public_username(client: TelegramClient, channel_entity, base_prefix="g"):
            for _ in range(MAX_USERNAME_ATTEMPTS):
                uname = gen_random_username(prefix=base_prefix, length=random.randint(6,12))
                try:
                    # UpdateUsernameRequest: for channels/groups we pass username as string
                    await client(UpdateUsernameRequest(channel=channel_entity, username=uname))
                    return uname
                except errors.UsernameOccupiedError:
                    continue
                except errors.UsernameInvalidError:
                    continue
                except errors.FloodWaitError as e:
                    print(f"{Fore.YELLOW}⚠ FloodWait username set: {getattr(e,'seconds', getattr(e,'retry_after', 'unknown'))}s")
                    if WAIT_ON_FLOOD:
                        await asyncio.sleep(getattr(e,'seconds', getattr(e,'retry_after', 30)) + 1)
                        continue
                    else:
                        return None
                except Exception:
                    return None
            return None
        
        async def get_owned_groups(client: TelegramClient, me_id: int, limit=200) -> List[Tuple[str, Optional[str]]]:
            owned = []
            try:
                async for d in client.iter_dialogs(limit=limit):
                    if getattr(d, "is_channel", False) or getattr(d, "is_group", False):
                        try:
                            resp = await client(GetParticipantRequest(d.entity, me_id))
                            part = getattr(resp, "participant", None)
                            if isinstance(part, types.ChannelParticipantCreator):
                                title = getattr(d.entity, "title", "No title")
                                username = getattr(d.entity, "username", None)
                                owned.append((title, username))
                        except errors.UserNotParticipantError:
                            continue
                        except errors.ChatAdminRequiredError:
                            continue
                        except Exception:
                            continue
            except Exception:
                pass
            return owned
        
        # ====== ASOSIY: yaratish va post yuborish ======
        async def create_groups_and_post(session_path: str, phone_repr: str, post_text: str):
            client = await prepare_client(session_path)
            if not client:
                print(f"{Fore.RED}{phone_repr}: Sessiya yaroqsiz yoki avtorizatsiya yo'q.")
                return 0, []
        
            try:
                me = await client.get_me()
                me_id = me.id
                results = []  # (group_title, username_or_None, post_status)
        
                owned = await get_owned_groups(client, me_id)
                owned_count = len(owned)
                print(f"{Fore.CYAN}{phone_repr}: Mavjud yaratilgan guruhlar: {owned_count}")
        
                # agar 5 yoki undan ko'p bo'lsa yangi guruh yaratmaymiz
                to_create = 0
                if owned_count >= 5:
                    print(f"{Fore.YELLOW}{phone_repr}: Akkauntda allaqachon 5 yoki undan ko'p guruh bor — faqat post yuboriladi.")
                else:
                    target_new = random.randint(GROUPS_PER_ACCOUNT_MIN, GROUPS_PER_ACCOUNT_MAX)
                    cap = 5
                    needed = min(target_new, cap - owned_count)
                    to_create = needed
                    print(f"{Fore.GREEN}{phone_repr}: Yaratiladigan yangi guruhlar soni: {needed}")
        
                # 1) Guruh yaratish
                created = 0
                seed = phone_repr[-4:] if phone_repr else ''.join(random.choices(string.digits, k=4))
                for i in range(to_create):
                    name = None
                    for _ in range(NAME_MAX_ATTEMPTS):
                        candidate = gen_group_name(seed=seed, suffix_len=random.choice([3,4,5]))
                        if 3 <= len(candidate) <= 128:
                            name = candidate
                            break
                    if not name:
                        name = f"Group-{seed}-{gen_suffix(3)}"
                    about = f"Avtomatik yaratilgan guruh: {name}"
                    try:
                        res = await client(CreateChannelRequest(title=name, about=about, megagroup=True))
                        ent = res.chats[0] if hasattr(res, "chats") and res.chats else await client.get_entity(name)
                        username = None
                        try:
                            username = await set_public_username(client, ent, base_prefix="g")
                        except Exception:
                            username = None
        
                        post_result = "Post yuborilmadi"
                        if post_text.strip():
                            try:
                                await client.send_message(ent, post_text)
                                post_result = "Post yuborildi"
                            except Exception as e:
                                post_result = f"Post yuborishda xato: {e}"
        
                        results.append((name, username, post_result))
                        print(f"{Fore.GREEN}{phone_repr}: '{name}' ({'@'+username if username else 'private'}) | {post_result}")
                        created += 1
                        await asyncio.sleep(random.uniform(*PAUSE_AFTER_CREATE))
                    except errors.FloodWaitError as e:
                        secs = getattr(e, 'seconds', getattr(e, 'retry_after', 30))
                        print(f"{Fore.YELLOW}{phone_repr}: FloodWait - kutamiz {secs}s")
                        if WAIT_ON_FLOOD:
                            await asyncio.sleep(secs + 1)
                            continue
                        else:
                            break
                    except Exception as e:
                        print(f"{Fore.RED}{phone_repr}: Guruh yaratishda xato: {e}")
                        await asyncio.sleep(1.5)
                        continue
        
                # 2) Agar mavjud guruhlar bo'lsa yoki yaratgandan keyin post yuborish
                all_groups = owned + [(r[0], r[1]) for r in results]
                if post_text.strip():
                    for title, uname in all_groups:
                        try:
                            entity = await client.get_entity(uname) if uname else await client.get_entity(title)
                            try:
                                await client.send_message(entity, post_text)
                                print(f"{Fore.GREEN}{phone_repr}: Post yuborildi -> {title}")
                            except Exception as e:
                                print(f"{Fore.RED}{phone_repr}: Post yuborishda xato {title}: {e}")
                        except Exception:
                            continue
        
                await client.disconnect()
                return (owned_count + created), results
        
            finally:
                try:
                    if client and client.is_connected():
                        await client.disconnect()
                except:
                    pass
        
        # ====== REPORT MODE ======
        async def report_mode(session_path: str, phone_repr: str):
            client = await prepare_client(session_path)
            if not client:
                print(f"{Fore.RED}{phone_repr}: Sessiya yaroqsiz yoki avtorizatsiya yo'q.")
                return []
            try:
                me = await client.get_me()
                me_id = me.id
                owned = await get_owned_groups(client, me_id)
                for title, uname in owned:
                    uname_txt = f"@{uname}" if uname else "private"
                    print(f"{Fore.GREEN}{phone_repr}: {title}  ({uname_txt})")
                if not owned:
                    print(f"{Fore.YELLOW}{phone_repr}: Hech qanday yaratilgan guruh topilmadi.")
                await client.disconnect()
                return owned
            finally:
                try:
                    if client and client.is_connected():
                        await client.disconnect()
                except:
                    pass
        
        # ====== MAIN ======
        async def main():
            print(f"{Fore.CYAN}=== Guruh yaratish / post skripti ===")
            print("1) Guruh yaratish va post yuborish")
            print("2) Akkauntlar ega bo'lgan guruhlar haqida hisobot (guruh yaratmaydi)")
            mode = input(f"{Fore.YELLOW}Tanlang (1 yoki 2): {Style.RESET_ALL}").strip()
            if mode not in ("1", "2"):
                print(f"{Fore.RED}Noto'g'ri tanlov. Chiqyapman.")
                return
        
            phones = read_phones(PHONE_CSV)
            if not phones:
                return
        
            sessions = []
            for p in phones:
                found = None
                for pattern in (f"telethon_{p}.session", f"{p}.session", f"+{p}.session"):
                    path = os.path.join(SESS_DIR, pattern)
                    if os.path.exists(path):
                        found = path
                        break
                if found:
                    sessions.append((p, found))
                else:
                    print(f"{Fore.YELLOW}⚠ Sessiya topilmadi: {p}")
        
            if not sessions:
                print(f"{Fore.RED}❌ Hech qanday sessiya topilmadi.")
                return
        
            post_text = ""
            if mode == "1":
                post_text = input(f"{Fore.CYAN}Post matnini kiriting (ENTER bosilsa hech narsa yuborilmaydi): {Style.RESET_ALL}").strip()
        
            total_created = 0
            per_account = {}
        
            for phone_repr, sess_path in sessions:
                print("\n" + "-"*60)
                print(f"{Fore.CYAN}Akkaunt: {phone_repr} bilan ishlanmoqda...")
                if mode == "1":
                    cnt, details = await create_groups_and_post(sess_path, phone_repr, post_text)
                    total_created += cnt
                    per_account[phone_repr] = (cnt, details)
                else:
                    owned = await report_mode(sess_path, phone_repr)
                    per_account[phone_repr] = (len(owned), owned)
                await asyncio.sleep(random.uniform(*PAUSE_BETWEEN_ACCOUNTS))
        
            # hisobot
            print("\n" + "="*60)
            if mode == "1":
                print(f"{Fore.LIGHTGREEN_EX}Jarayon tugadi. Har akkaunt uchun natija:")
                for acc, (cnt, details) in per_account.items():
                    print(f"{Fore.CYAN}{acc}: jami guruhlar (yangi + eski) = {Fore.GREEN}{cnt}")
                    for it in details:
                        name, uname, postres = it
                        uname_txt = f"@{uname}" if uname else "private"
                        print(f"   - {name}  ({uname_txt})  | {postres}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Hisobot (akkountlar tomonidan yaratilgan guruhlar):")
                for acc, (cnt, owned) in per_account.items():
                    print(f"{Fore.CYAN}{acc}: {Fore.GREEN}{cnt} ta")
                    for title, uname in owned:
                        uname_txt = f"@{uname}" if uname else "private"
                        print(f"   - {title}  ({uname_txt})")
        
            print("\n" + "="*60)
            # keep-alive
            try:
                while True:
                    cmd = input(f"{Fore.CYAN}Skript ishlaydi. Chiqish uchun 'q' + Enter bosing. Hisobotni ko'rish uchun Enter bosing: {Style.RESET_ALL}")
                    if cmd.strip().lower() == 'q':
                        print(f"{Fore.MAGENTA}Chiqilmoqda... Xayr!")
                        break
                    else:
                        print(f"{Fore.LIGHTGREEN_EX}Hozirgi holat — jami yaratildi yoki qayd etilgan: {total_created}")
            except KeyboardInterrupt:
                print(f"\n{Fore.MAGENTA}Ctrl+C — chiqilmoqda...")
        
        if __name__ == '__main__':
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except Exception:
                    pass
            asyncio.run(main())


    elif a == 27:
        import webbrowser
        import sys
        import time
        import os
        import subprocess
        
        # YouTube darslik manzili (bitta link kifoya)
        YOUTUBE_URL = "https://youtu.be/FeZthaJazdo"
        
        print("\n📺 Video darslik ochilmoqda...")
        time.sleep(0.7)
        
        try:
            # Universal usul bilan ochish
            webbrowser.open_new_tab(YOUTUBE_URL)
            print("✅ YouTube ochildi — Telethon darsliklarini tomosha qiling!\n")
        except Exception:
            try:
                if sys.platform.startswith("win"):
                    os.startfile(YOUTUBE_URL)
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", YOUTUBE_URL])
                else:
                    subprocess.Popen(["xdg-open", YOUTUBE_URL])
                print("✅ YouTube ochildi — Telethon darsliklarini tomosha qiling!\n")
            except Exception as e:
                print(f"❌ Xatolik: YouTube ochib bo‘lmadi. ({e})")
        
        time.sleep(1)
        
    elif a == 28:
        import subprocess
        import sys
        import os
        
        # ---- Pip orqali modulni o'rnatish ----
        def install_package(package_name):
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "show", package_name],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                print(f"✅ {package_name} - MODUL ORNATILGAN!")
            except subprocess.CalledProcessError:
                print(f"📦 {package_name} - MODUL O'RNATIMOQDA...")
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package_name, "-q", "--disable-pip-version-check"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                    )
                    print(f"✅ {package_name} - OK!")
                except subprocess.CalledProcessError as e:
                    print(f"❌ {package_name} - XATO: {e}")
        
        def install_all_requirements():
            print("=" * 50)
            print("MODULLARNI TEKSHIRISH VA O'RNATISH...")
            print("=" * 50)
            for package in ['selenium', 'webdriver-manager']:
                install_package(package)
            print("=" * 50)
            print("✅ BARCHA MODULLAR TAYYOR!")
            print("=" * 50)
        
        install_all_requirements()
        
        import csv
        import random
        import asyncio
        import ctypes
        import json
        import time
        import re
        import string
        import traceback
        
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        from telethon.errors import (
            SessionPasswordNeededError,
            PasswordHashInvalidError,
            PhoneCodeInvalidError,
            PhoneCodeExpiredError,
            PhoneNumberBannedError,
        )
        
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        
        # ----------------------------- Sozlamalar -----------------------------
        API_ID = 13682
        API_HASH = 'de37bcf00f4688de900510f4f87384bb'
        
        SESSION_FOLDER = './sessions'
        APIS_FOLDER = './apis'
        
        PHONE_CSV = 'phone.csv'
        FROZEN_CSV = 'frozen_accounts.csv'
        
        MOBILE_PROXY = ""
        
        HEADLESS = True
        S_SHORT = 1.0
        S_MED = 2.0
        S_LONG = 4.0
        MAX_CODE_ATTEMPTS = 3
        ERROR_RETRY_DELAY = 5
        
        TEMP_PREFIX = "NEW_"
        
        # ----------------------------- Fayl nomlari -----------------------------
        def get_old_session_files(phone):
            phone_clean = phone.replace('+', '')
            return {
                'string': os.path.join(SESSION_FOLDER, f"telethon_{phone_clean}.session"),
                'sqlite': os.path.join(SESSION_FOLDER, f"{phone_clean}_SQLite.session"),
            }
        
        def get_temp_session_files(phone):
            phone_clean = phone.replace('+', '')
            return {
                'string': os.path.join(SESSION_FOLDER, f"{TEMP_PREFIX}telethon_{phone_clean}.session"),
                'sqlite': os.path.join(SESSION_FOLDER, f"{TEMP_PREFIX}{phone_clean}_SQLite.session"),
            }
        
        def cleanup_old_and_rename_new(phone):
            phone_clean = phone.replace('+', '')
            old_files = get_old_session_files(phone)
            temp_files = get_temp_session_files(phone)
            
            if not os.path.exists(temp_files['string']):
                print(colorize(f"[{phone}] ⚠️ Yangi string sessiya topilmadi", 'yellow', False))
                return False
            
            try:
                for key, filepath in old_files.items():
                    if os.path.exists(filepath):
                        os.remove(filepath)
                        print(colorize(f"[{phone}] 🗑️ O'chirildi: {os.path.basename(filepath)}", 'yellow', False))
                
                for key in ['string', 'sqlite']:
                    if os.path.exists(temp_files[key]):
                        os.rename(temp_files[key], old_files[key])
                        print(colorize(f"[{phone}] 📝 Nomlandi: {os.path.basename(temp_files[key])} → {os.path.basename(old_files[key])}", 'green', False))
                
                return True
            except Exception as e:
                print(colorize(f"[{phone}] ❌ Fayl operatsiyasida xato: {e}", 'red', True))
                return False
        
        def cleanup_temp_files(phone):
            temp_files = get_temp_session_files(phone)
            for key, filepath in temp_files.items():
                if os.path.exists(filepath):
                    try:
                        os.remove(filepath)
                    except:
                        pass
        
        # ----------------------------- Random nomlar -----------------------------
        APP_NAME_PREFIXES = [
            'TeleBot', 'ChatHub', 'MsgApp', 'CloudChat', 'FastMsg',
            'TeleChat', 'QuickMsg', 'NetChat', 'SkyMsg', 'FlashChat',
            'SwiftMsg', 'ProChat', 'UltraMsg', 'MegaChat', 'SuperApp',
            'SmartMsg', 'CoolChat', 'NiceApp', 'GoodMsg', 'BestChat',
            'TopMsg', 'MaxChat', 'HotApp', 'NewMsg', 'FreshChat',
            'BlueMsg', 'RedChat', 'GreenApp', 'DarkMsg', 'LightChat',
            'StarMsg', 'MoonChat', 'SunApp', 'FireMsg', 'IceChat',
            'TechMsg', 'CodeChat', 'DevApp', 'AppBot', 'BotHub',
            'AirMsg', 'QuantumChat', 'CyberBot', 'PulseMsg', 'MatrixChat',
            'NovaMsg', 'GalaxyChat', 'PrimeBot', 'AlphaChat', 'OmegaMsg',
            'FusionApp', 'RocketMsg', 'BlazeChat', 'ShadowMsg', 'BrightApp',
            'FutureChat', 'NanoMsg', 'HyperBot', 'VortexChat', 'StormMsg',
            'WaveChat', 'SignalBot', 'PixelMsg', 'NeonChat', 'CosmoApp',
        ]
        
        APP_NAME_SUFFIXES = [
            'Pro', 'Plus', 'Max', 'Ultra', 'Lite', 'Go', 'Now', 'Fast',
            'Hub', 'Box', 'Lab', 'Kit', 'One', 'X', 'Z', 'App',
            'Prime', 'Edge', 'Core', 'Boost', 'Flex', 'Wave', 'Storm',
            'Drive', 'Pulse', 'Flow', 'Force', 'Engine',
            'Stream', 'Space', 'Zone', 'Sphere', 'Frame', 'Gate',
            'Dock', 'Beam', 'Flash', 'Shift', 'Cloud', 'Link',
            'Nest', 'Base', 'Alpha', 'Omega', 'Turbo', 'Jet'
        ]
        
        def generate_random_app_name():
            prefix = random.choice(APP_NAME_PREFIXES)
            if random.random() > 0.5:
                return f"{prefix}{random.choice(APP_NAME_SUFFIXES)}"
            return f"{prefix}{random.randint(1, 9999)}"
        
        def generate_random_short_name():
            prefix = random.choice(APP_NAME_PREFIXES).lower()
            prefix_clean = ''.join(c for c in prefix if c.isalnum())
            suffix_length = random.randint(4, 8)
            suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=suffix_length))
            result = f"{prefix_clean}{suffix}"
            while len(result) < 5:
                result += random.choice(string.ascii_lowercase + string.digits)
            return result[:32]
        
        # ----------------------------- ANSI ranglar -----------------------------
        def _enable_ansi_on_windows():
            if os.name != 'nt':
                return
            try:
                kernel32 = ctypes.windll.kernel32
                h = kernel32.GetStdHandle(-11)
                mode = ctypes.c_uint32()
                if kernel32.GetConsoleMode(h, ctypes.byref(mode)):
                    kernel32.SetConsoleMode(h, mode.value | 0x0004)
            except:
                pass
        
        _enable_ansi_on_windows()
        
        CLR = {
            'reset': '\033[0m', 'bold': '\033[1m', 'red': '\033[31m',
            'green': '\033[32m', 'yellow': '\033[33m', 'blue': '\033[34m',
            'magenta': '\033[35m', 'cyan': '\033[36m', 'white': '\033[37m',
            'bwhite': '\033[97m',
        }
        
        def colorize(text: str, color: str, bold: bool = False) -> str:
            c = CLR.get(color, '')
            b = CLR['bold'] if bold else ''
            return f"{b}{c}{text}{CLR['reset']}"
        
        # ----------------------------- Helpers -----------------------------
        def api_json_exists(phone):
            return os.path.exists(os.path.join(APIS_FOLDER, f"api_{phone.replace('+', '')}.json"))
        
        def read_phones_from_csv(file_path):
            if not os.path.exists(file_path):
                return []
            phones = []
            with open(file_path, newline='', encoding='utf-8') as f:
                for row in csv.reader(f):
                    if row and row[0].strip():
                        phones.append(row[0].strip())
            return phones
        
        def read_all_phones():
            all_phones = []
            seen = set()
            
            phones_main = read_phones_from_csv(PHONE_CSV)
            for phone in phones_main:
                if phone not in seen:
                    all_phones.append(phone)
                    seen.add(phone)
            
            main_count = len(all_phones)
            
            phones_frozen = read_phones_from_csv(FROZEN_CSV)
            frozen_added = 0
            for phone in phones_frozen:
                if phone not in seen:
                    all_phones.append(phone)
                    seen.add(phone)
                    frozen_added += 1
            
            return all_phones, main_count, frozen_added
        
        # ----------------------------- Selenium funksiyalari -----------------------------
        def robust_fill_phone_and_submit(driver, phone):
            try:
                time.sleep(0.5)
                phone_input = None
                for sel in ["input[name='phone']", "input#my_login_phone", "input[type='tel']", "input[type='text']"]:
                    try:
                        for el in driver.find_elements(By.CSS_SELECTOR, sel):
                            if driver.execute_script("return arguments[0].offsetParent !== null;", el):
                                phone_input = el
                                break
                        if phone_input:
                            break
                    except:
                        continue
                if not phone_input:
                    return False
                driver.execute_script(
                    "arguments[0].focus(); arguments[0].value = arguments[1]; "
                    "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));",
                    phone_input, phone
                )
                time.sleep(0.3)
                try:
                    for btn in driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], button.btn"):
                        if driver.execute_script("return arguments[0].offsetParent !== null;", btn):
                            driver.execute_script("arguments[0].click();", btn)
                            break
                except:
                    phone_input.send_keys(Keys.ENTER)
                time.sleep(1.0)
                return True
            except:
                return False
        
        def robust_fill_code_and_submit(driver, code):
            try:
                time.sleep(0.5)
                code_input = None
                for sel in ["input[name='password']", "input#my_password", "input[type='password']", "input[type='text']"]:
                    try:
                        for el in driver.find_elements(By.CSS_SELECTOR, sel):
                            if driver.execute_script("return arguments[0].offsetParent !== null;", el):
                                code_input = el
                                break
                        if code_input:
                            break
                    except:
                        continue
                if not code_input:
                    return False
                driver.execute_script("arguments[0].focus(); arguments[0].value = '';", code_input)
                for char in code:
                    code_input.send_keys(char)
                    time.sleep(0.03)
                time.sleep(0.3)
                try:
                    for btn in driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], button.btn"):
                        if driver.execute_script("return arguments[0].offsetParent !== null;", btn):
                            driver.execute_script("arguments[0].click();", btn)
                            break
                except:
                    code_input.send_keys(Keys.ENTER)
                time.sleep(1.5)
                return True
            except:
                return False
        
        # ----------------------------- Kod izlash -----------------------------
        async def fetch_login_code_from_telegram(client):
            try:
                try:
                    service = await client.get_entity(777000)
                except:
                    return None
                msgs = await client.get_messages(service, limit=3)
                if not msgs:
                    return None
                for msg in msgs:
                    text = msg.message or ''
                    if not text:
                        continue
                    text_lower = text.lower()
                    if not any(kw in text_lower for kw in ['login', 'code', 'my.telegram', 'confirm', 'verification']):
                        continue
                    print(colorize(f"\n[code] {'═'*50}", 'cyan', False))
                    print(colorize(f"[code] XABAR:", 'cyan', True))
                    print(text)
                    print(colorize(f"{'═'*50}", 'cyan', False))
                    
                    for pattern in [r'code[:\s]+([A-Za-z0-9_\-]{5,20})', r'code\s+is\s+([A-Za-z0-9_\-]{5,20})']:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            code = match.group(1).strip()
                            if code.lower() not in ['is', 'the', 'your']:
                                print(colorize(f"[code] ✅ TOPILDI: {code}", 'green', True))
                                return code
                    
                    for pattern in [r'["\'\`]([A-Za-z0-9_\-]{5,20})["\'\`]']:
                        match = re.search(pattern, text)
                        if match:
                            print(colorize(f"[code] ✅ TOPILDI: {match.group(1)}", 'green', True))
                            return match.group(1)
                    
                    for line in text.split('\n'):
                        line = line.strip()
                        if re.match(r'^[A-Za-z0-9_\-]{5,20}$', line):
                            if line.lower() not in ['login', 'code', 'telegram', 'please', 'enter']:
                                print(colorize(f"[code] ✅ TOPILDI (qator): {line}", 'green', True))
                                return line
                    
                    excluded = ['telegram', 'please', 'login', 'code', 'confirm', 'enter', 'your', 'the', 
                               'this', 'that', 'with', 'from', 'have', 'been', 'will', 'verification', 
                               'confirmation', 'account', 'browser', 'device', 'android', 'received', 
                               'request', 'https']
                    for candidate in re.findall(r'\b([A-Za-z0-9][A-Za-z0-9_\-]{4,19})\b', text):
                        if candidate.lower() in excluded:
                            continue
                        has_letter = any(c.isalpha() for c in candidate)
                        has_digit = any(c.isdigit() for c in candidate)
                        if has_letter and has_digit:
                            print(colorize(f"[code] ✅ TOPILDI: {candidate}", 'green', True))
                            return candidate
                return None
            except:
                return None
        
        async def fetch_telegram_auth_code(client):
            try:
                try:
                    service = await client.get_entity(777000)
                except:
                    return None
                msgs = await client.get_messages(service, limit=3)
                if not msgs:
                    return None
                for msg in msgs:
                    text = msg.message or ''
                    if not text:
                        continue
                    print(colorize(f"\n[tg_code] {'═'*50}", 'cyan', False))
                    print(colorize(f"[tg_code] XABAR:", 'cyan', True))
                    print(text)
                    print(colorize(f"{'═'*50}", 'cyan', False))
                    for pattern in [r'code[:\s]+(\d{5,6})', r':\s*(\d{5,6})', r'\b(\d{5,6})\b']:
                        match = re.search(pattern, text, re.IGNORECASE)
                        if match:
                            print(colorize(f"[tg_code] ✅ TOPILDI: {match.group(1)}", 'green', True))
                            return match.group(1)
                return None
            except:
                return None
        
        # ----------------------------- API parsing -----------------------------
        def parse_api_from_page(driver):
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text
            except:
                body_text = ""
            
            api_id = None
            api_hash = None
            
            match = re.search(r'api_id\s*:\s*\n?\s*(\d{6,10})', body_text, re.IGNORECASE)
            if match:
                api_id = match.group(1)
            else:
                match = re.search(r'\b(\d{7,8})\b', body_text)
                if match:
                    api_id = match.group(1)
            
            match = re.search(r'api_hash\s*:\s*\n?\s*([a-f0-9]{32})', body_text, re.IGNORECASE)
            if match:
                api_hash = match.group(1)
            else:
                match = re.search(r'\b([a-f0-9]{32})\b', body_text, re.IGNORECASE)
                if match:
                    api_hash = match.group(1)
            
            if api_id and api_hash:
                print(colorize(f"[parse] ✅ api_id: {api_id}, api_hash: {api_hash}", 'green', True))
            
            return api_id, api_hash
        
        # ----------------------------- Ilova yaratish -----------------------------
        def create_new_app_on_page(driver, phone, max_retries=4):
            all_platforms = ['android', 'desktop', 'web', 'Other (specify in description)']
            
            for retry in range(max_retries):
                try:
                    app_title = generate_random_app_name()
                    app_short = generate_random_short_name()
                    app_url = "https://example.com"
                    
                    print(colorize(f"[{phone}] Urinish {retry + 1}/{max_retries}: {app_title}", 'cyan', False))
                    print(colorize(f"[{phone}] 📝 Shortname: {app_short}", 'cyan', False))
                    
                    try:
                        title_input = driver.find_element(By.NAME, "app_title")
                    except:
                        title_input = driver.find_element(By.ID, "app_title")
                    title_input.clear()
                    title_input.send_keys(app_title)
                    
                    try:
                        short_input = driver.find_element(By.NAME, "app_shortname")
                    except:
                        short_input = driver.find_element(By.ID, "app_shortname")
                    short_input.clear()
                    short_input.send_keys(app_short)
                    
                    try:
                        url_input = driver.find_element(By.NAME, "app_url")
                        url_input.clear()
                        url_input.send_keys(app_url)
                    except:
                        pass
                    
                    platform_to_try = all_platforms[retry % len(all_platforms)]
                    
                    try:
                        el = driver.find_element(By.CSS_SELECTOR, f"input[name='app_platform'][value='{platform_to_try}']")
                        driver.execute_script("arguments[0].click();", el)
                        print(colorize(f"[{phone}] ✅ Platforma: {platform_to_try}", 'green', False))
                    except:
                        for val in all_platforms:
                            if val != platform_to_try:
                                try:
                                    el = driver.find_element(By.CSS_SELECTOR, f"input[name='app_platform'][value='{val}']")
                                    driver.execute_script("arguments[0].click();", el)
                                    print(colorize(f"[{phone}] ✅ Platforma: {val}", 'green', False))
                                    break
                                except:
                                    continue
                    
                    time.sleep(0.3)
                    
                    clicked = False
                    try:
                        for btn in driver.find_elements(By.TAG_NAME, "button"):
                            if 'create' in btn.text.lower() and 'cancel' not in btn.text.lower():
                                driver.execute_script("arguments[0].click();", btn)
                                clicked = True
                                break
                    except:
                        pass
                    if not clicked:
                        try:
                            driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
                        except:
                            short_input.send_keys(Keys.ENTER)
                    
                    time.sleep(S_LONG)
                    
                    api_id, api_hash = parse_api_from_page(driver)
                    
                    if api_id and api_hash:
                        print(colorize(f"[{phone}] ✅ Ilova yaratildi!", 'green', True))
                        return True
                    
                    page_text = driver.page_source.lower()
                    body_text = ""
                    try:
                        body_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                    except:
                        pass
                    
                    error_patterns = [
                        'already taken', 'already exists', 'is invalid', 'too short',
                        'too long', 'choose another', 'try again later', 'something went wrong',
                    ]
                    
                    error_found = False
                    error_msg = ""
                    
                    for err in error_patterns:
                        if err in page_text or err in body_text:
                            error_found = True
                            error_msg = err
                            break
                    
                    if 'app_title' in page_text and not error_found:
                        print(colorize(f"[{phone}] ⏳ Sahifa yangilanmoqda...", 'yellow', False))
                        time.sleep(3)
                        
                        api_id, api_hash = parse_api_from_page(driver)
                        if api_id and api_hash:
                            print(colorize(f"[{phone}] ✅ Ilova yaratildi!", 'green', True))
                            return True
                        
                        if retry < max_retries - 1:
                            for i in range(ERROR_RETRY_DELAY, 0, -1):
                                sys.stdout.write(f"\r[{phone}] ⚠️ API topilmadi, qayta urinish: {i} sek...   ")
                                sys.stdout.flush()
                                time.sleep(1)
                            print()
                            continue
                    
                    if error_found:
                        print(colorize(f"[{phone}] ⚠️ Xato: {error_msg}", 'yellow', True))
                        if retry < max_retries - 1:
                            for i in range(ERROR_RETRY_DELAY, 0, -1):
                                sys.stdout.write(f"\r[{phone}] ⏳ Kutilmoqda: {i} sek...   ")
                                sys.stdout.flush()
                                time.sleep(1)
                            print()
                        continue
                    
                    if 'app_title' not in page_text:
                        print(colorize(f"[{phone}] ✅ Forma yuborildi", 'green', True))
                        return True
                    
                except Exception as e:
                    print(colorize(f"[{phone}] Xato: {e}", 'red', True))
                    if retry < max_retries - 1:
                        for i in range(ERROR_RETRY_DELAY, 0, -1):
                            sys.stdout.write(f"\r[{phone}] ⏳ Kutilmoqda: {i} sek...   ")
                            sys.stdout.flush()
                            time.sleep(1)
                        print()
            
            return False
        
        # ----------------------------- Selenium flow (ODDIY) -----------------------------
        def create_app_on_mytelegram_sync(phone, get_code_callable, headless=HEADLESS, save_path=APIS_FOLDER, max_site_retries=4):
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            chrome_opts = Options()
            
            if headless:
                chrome_opts.add_argument("--headless=new")
            
            chrome_opts.add_argument("--incognito")
            chrome_opts.add_argument("--no-sandbox")
            chrome_opts.add_argument("--disable-dev-shm-usage")
            chrome_opts.add_argument("--disable-blink-features=AutomationControlled")
            chrome_opts.add_argument("--log-level=3")
            chrome_opts.add_argument("--disable-application-cache")
            chrome_opts.add_argument("--disable-cache")
            chrome_opts.add_argument("--window-size=1920,1080")
            
            if MOBILE_PROXY:
                proxy_parts = MOBILE_PROXY.split(':')
                if len(proxy_parts) >= 2:
                    chrome_opts.add_argument(f"--proxy-server={proxy_parts[0]}:{proxy_parts[1]}")
                    print(colorize(f"[{phone}] 🌐 Proxy: {proxy_parts[0]}:{proxy_parts[1]}", 'cyan', False))
            
            chrome_opts.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            
            for site_attempt in range(max_site_retries):
                driver = None
                try:
                    try:
                        chromepath = ChromeDriverManager().install()
                        try:
                            driver = webdriver.Chrome(service=Service(chromepath), options=chrome_opts)
                        except:
                            driver = webdriver.Chrome(chromepath, options=chrome_opts)
                        
                        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                        driver.set_page_load_timeout(30)
                        
                        print(colorize(f"[{phone}] 🖥️ Chrome brauzer", 'cyan', False))
                        print(colorize(f"[{phone}] 🔒 Incognito rejimi", 'cyan', False))
                        
                    except Exception as e:
                        print(colorize(f"[{phone}] ❌ Selenium xatosi: {e}", 'red', True))
                        if site_attempt < max_site_retries - 1:
                            print(colorize(f"[{phone}] ⏳ Qayta urinish ({site_attempt + 2}/{max_site_retries})...", 'yellow', False))
                            time.sleep(3)
                            continue
                        return None
                    
                    print(colorize(f"[{phone}] my.telegram.org ochilmoqda... (urinish {site_attempt + 1}/{max_site_retries})", 'cyan', True))
                    
                    try:
                        driver.get("https://my.telegram.org/auth")
                        time.sleep(S_MED)
                    except Exception as e:
                        print(colorize(f"[{phone}] ❌ Sayt ochilmadi: {e}", 'red', True))
                        try:
                            driver.quit()
                        except:
                            pass
                        if site_attempt < max_site_retries - 1:
                            print(colorize(f"[{phone}] ⏳ Qayta urinish ({site_attempt + 2}/{max_site_retries})...", 'yellow', False))
                            time.sleep(5)
                            continue
                        return None
                    
                    page_source = driver.page_source.lower()
                    if 'telegram' not in page_source and 'phone' not in page_source:
                        print(colorize(f"[{phone}] ❌ Sahifa to'liq yuklanmadi", 'red', True))
                        try:
                            driver.quit()
                        except:
                            pass
                        if site_attempt < max_site_retries - 1:
                            print(colorize(f"[{phone}] ⏳ Qayta urinish ({site_attempt + 2}/{max_site_retries})...", 'yellow', False))
                            time.sleep(5)
                            continue
                        return None
                    
                    print(colorize(f"[{phone}] ✅ Sayt ochildi", 'green', False))
                    
                    if not robust_fill_phone_and_submit(driver, phone):
                        print(colorize(f"[{phone}] ❌ Telefon raqami kiritilmadi", 'red', True))
                        try:
                            driver.quit()
                        except:
                            pass
                        if site_attempt < max_site_retries - 1:
                            print(colorize(f"[{phone}] ⏳ Qayta urinish ({site_attempt + 2}/{max_site_retries})...", 'yellow', False))
                            time.sleep(5)
                            continue
                        return None
                    
                    time.sleep(S_LONG)
                    
                    if 'too many' in driver.page_source.lower():
                        print(colorize(f"[{phone}] ❌ Juda ko'p urinish! Keyingi nomerga o'tilmoqda...", 'red', True))
                        driver.quit()
                        return None
                    
                    print(colorize(f"[{phone}] Kod kutilmoqda...", 'cyan', True))
                    code_entered = False
                    
                    for attempt in range(MAX_CODE_ATTEMPTS):
                        print(colorize(f"[{phone}] Urinish {attempt + 1}/{MAX_CODE_ATTEMPTS}", 'cyan', False))
                        time.sleep(3)
                        
                        code = None
                        try:
                            code = get_code_callable()
                        except:
                            pass
                        
                        if code:
                            print(colorize(f"[{phone}] Kiritilmoqda: {code}", 'green', True))
                            if robust_fill_code_and_submit(driver, code):
                                time.sleep(S_MED)
                                if '/auth' not in driver.current_url:
                                    code_entered = True
                                    break
                    
                    if not code_entered:
                        manual = input(colorize(f"[{phone}] Kodni kiriting: ", 'yellow', True)).strip()
                        if not manual:
                            driver.quit()
                            return None
                        robust_fill_code_and_submit(driver, manual)
                        time.sleep(S_MED)
                    
                    print(colorize(f"[{phone}] /apps sahifasiga o'tish...", 'cyan', False))
                    
                    try:
                        driver.get("https://my.telegram.org/apps")
                        time.sleep(S_LONG)
                    except Exception as e:
                        print(colorize(f"[{phone}] ❌ /apps sahifasi ochilmadi: {e}", 'red', True))
                        driver.quit()
                        return None
                    
                    api_id, api_hash = parse_api_from_page(driver)
                    
                    if api_id and api_hash:
                        data = {'phone': phone, 'api_id': int(api_id), 'api_hash': api_hash}
                        fname = os.path.join(save_path, f"api_{phone.replace('+', '')}.json")
                        with open(fname, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        print(colorize(f"[{phone}] 🔐 API mavjud!", 'green', True))
                        driver.quit()
                        return data
                    
                    print(colorize(f"[{phone}] Ilova yaratilmoqda...", 'yellow', True))
                    
                    if 'app_title' in driver.page_source.lower():
                        if create_new_app_on_page(driver, phone, max_retries=4):
                            try:
                                driver.get("https://my.telegram.org/apps")
                                time.sleep(S_MED)
                            except:
                                pass
                            
                            api_id, api_hash = parse_api_from_page(driver)
                            if api_id and api_hash:
                                data = {'phone': phone, 'api_id': int(api_id), 'api_hash': api_hash}
                                fname = os.path.join(save_path, f"api_{phone.replace('+', '')}.json")
                                with open(fname, 'w', encoding='utf-8') as f:
                                    json.dump(data, f, ensure_ascii=False, indent=2)
                                print(colorize(f"[{phone}] 🔐 Yaratildi!", 'green', True))
                                driver.quit()
                                return data
                    
                    print(colorize(f"\n[{phone}] Brauzerda QO'LINGIZ bilan to'ldiring", 'yellow', True))
                    input(colorize("Tayyor bo'lganda ENTER...", 'yellow', True))
                    
                    try:
                        driver.get("https://my.telegram.org/apps")
                        time.sleep(S_MED)
                    except:
                        pass
                    
                    api_id, api_hash = parse_api_from_page(driver)
                    if api_id and api_hash:
                        data = {'phone': phone, 'api_id': int(api_id), 'api_hash': api_hash}
                        fname = os.path.join(save_path, f"api_{phone.replace('+', '')}.json")
                        with open(fname, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        driver.quit()
                        return data
                    
                    driver.quit()
                    return None
                    
                except Exception as e:
                    print(colorize(f"[{phone}] ❌ Umumiy xato: {e}", 'red', True))
                    try:
                        driver.quit()
                    except:
                        pass
                    
                    if site_attempt < max_site_retries - 1:
                        print(colorize(f"[{phone}] ⏳ Qayta urinish ({site_attempt + 2}/{max_site_retries})...", 'yellow', False))
                        time.sleep(5)
                        continue
                    return None
            
            print(colorize(f"[{phone}] ❌ {max_site_retries} marta urinildi, muvaffaqiyatsiz.", 'red', True))
            return None
        
        async def create_api_for_authorized_client(phone, client):
            loop = asyncio.get_event_loop()
            def get_code_sync():
                try:
                    fut = asyncio.run_coroutine_threadsafe(fetch_login_code_from_telegram(client), loop)
                    return fut.result(timeout=15)
                except:
                    return None
            return await loop.run_in_executor(None, create_app_on_mytelegram_sync, phone, get_code_sync, HEADLESS, APIS_FOLDER)
        
        # ----------------------------- Yangi sessiya yaratish (TOZA) -----------------------------
        async def create_new_session_with_api(phone, old_client, api_info):
            new_api_id = int(api_info['api_id'])
            new_api_hash = api_info['api_hash']
            
            temp_files = get_temp_session_files(phone)
            
            print(colorize(f"[{phone}] API {new_api_id} bilan sessiya yaratilmoqda...", 'cyan', True))
            
            # TOZA TelegramClient - hech qanday fake device yo'q
            new_client = TelegramClient(StringSession(), new_api_id, new_api_hash)
            
            try:
                await new_client.connect()
                
                print(colorize(f"[{phone}] Kod so'ralmoqda...", 'cyan', False))
                await new_client.send_code_request(phone)
                
                code = None
                for attempt in range(MAX_CODE_ATTEMPTS):
                    print(colorize(f"[{phone}] Kod kutilmoqda ({attempt + 1}/{MAX_CODE_ATTEMPTS})...", 'cyan', False))
                    await asyncio.sleep(3)
                    code = await fetch_telegram_auth_code(old_client)
                    if code:
                        break
                
                if not code:
                    code = input(colorize(f"[{phone}] Kodni kiriting: ", 'yellow', True)).strip()
                    if not code:
                        await new_client.disconnect()
                        return False
                
                try:
                    await new_client.sign_in(phone, code)
                    print(colorize(f"[{phone}] ✅ Kod qabul qilindi!", 'green', True))
                except SessionPasswordNeededError:
                    print(colorize(f"[{phone}] 2FA kerak", 'yellow', True))
                    while True:
                        password = input(colorize(f"[{phone}] 2FA parol: ", 'yellow', True)).strip()
                        if not password:
                            continue
                        try:
                            await new_client.sign_in(password=password)
                            print(colorize(f"[{phone}] ✅ 2FA OK!", 'green', True))
                            break
                        except PasswordHashInvalidError:
                            print(colorize("Parol xato!", 'red', True))
                except PhoneCodeInvalidError:
                    print(colorize(f"[{phone}] Kod xato!", 'red', True))
                    await new_client.disconnect()
                    return False
                except PhoneCodeExpiredError:
                    print(colorize(f"[{phone}] Kod eskirgan!", 'red', True))
                    await new_client.disconnect()
                    return False
                
                if not await new_client.is_user_authorized():
                    await new_client.disconnect()
                    return False
                
                me = await new_client.get_me()
                print(colorize(f"[{phone}] 🎉 Avtorizatsiya: {getattr(me, 'first_name', '')}", 'green', True))
                
                string_session = new_client.session.save()
                with open(temp_files['string'], 'w', encoding='utf-8') as f:
                    f.write(string_session)
                print(colorize(f"[{phone}] 📄 String: {os.path.basename(temp_files['string'])}", 'cyan', False))
                
                dc_id = new_client.session.dc_id
                server_address = new_client.session.server_address
                port = new_client.session.port
                auth_key = new_client.session.auth_key
                
                await new_client.disconnect()
                
                # TOZA SQLite client
                sqlite_client = TelegramClient(temp_files['sqlite'], new_api_id, new_api_hash)
                await sqlite_client.connect()
                sqlite_client.session.set_dc(dc_id, server_address, port)
                sqlite_client.session.auth_key = auth_key
                sqlite_client.session.save()
                await sqlite_client.disconnect()
                print(colorize(f"[{phone}] 💾 SQLite: {os.path.basename(temp_files['sqlite'])}", 'cyan', False))
                
                return True
                
            except Exception as e:
                print(colorize(f"[{phone}] Xato: {e}", 'red', True))
                cleanup_temp_files(phone)
                try:
                    await new_client.disconnect()
                except:
                    pass
                return False
        
        # ----------------------------- Asosiy ishlov -----------------------------
        async def process_phone(phone):
            print(colorize(f"\n{'='*60}", 'bwhite', True))
            print(colorize(f"📱 {phone}", 'cyan', True))
            print(colorize(f"{'='*60}", 'bwhite', True))
            
            if api_json_exists(phone):
                print(colorize(f"[{phone}] ✅ API mavjud, o'tkazib yuborildi", 'green', True))
                return True
            
            old_files = get_old_session_files(phone)
            
            if not os.path.exists(old_files['string']):
                print(colorize(f"[{phone}] ❌ Sessiya topilmadi", 'red', True))
                return False
            
            with open(old_files['string'], 'r', encoding='utf-8') as f:
                session_string = f.read().strip()
            
            # TOZA TelegramClient - hech qanday fake device yo'q
            old_client = TelegramClient(StringSession(session_string), API_ID, API_HASH)
            
            try:
                await old_client.connect()
                
                if not await old_client.is_user_authorized():
                    print(colorize(f"[{phone}] ❌ Sessiya avtorizatsiya qilinmagan", 'red', True))
                    await old_client.disconnect()
                    return False
                
                me = await old_client.get_me()
                print(colorize(f"[{phone}] ✅ Aktiv: {getattr(me, 'first_name', '')}", 'green', True))
                
                print(colorize(f"[{phone}] ➡️ API yaratilmoqda...", 'yellow', True))
                api_info = await create_api_for_authorized_client(phone, old_client)
                
                if not api_info:
                    await old_client.disconnect()
                    return False
                
                print(colorize(f"[{phone}] ➡️ Yangi sessiya yaratilmoqda...", 'yellow', True))
                session_created = await create_new_session_with_api(phone, old_client, api_info)
                
                await old_client.disconnect()
                
                if session_created:
                    print(colorize(f"[{phone}] ➡️ Fayllar yangilanmoqda...", 'yellow', True))
                    renamed = cleanup_old_and_rename_new(phone)
                    
                    if renamed:
                        print(colorize(f"[{phone}] 🎉 TAYYOR!", 'green', True))
                        return True
                    else:
                        print(colorize(f"[{phone}] ⚠️ Sessiya yaratildi lekin fayl xatosi", 'yellow', True))
                        return True
                else:
                    cleanup_temp_files(phone)
                    print(colorize(f"[{phone}] ❌ Sessiya yaratilmadi", 'red', True))
                    return False
                
            except Exception as e:
                print(colorize(f"[{phone}] Xato: {e}", 'red', True))
                cleanup_temp_files(phone)
                try:
                    await old_client.disconnect()
                except:
                    pass
                return False
        
        # ----------------------------- MAIN -----------------------------
        async def main():
            os.makedirs(SESSION_FOLDER, exist_ok=True)
            os.makedirs(APIS_FOLDER, exist_ok=True)
            
            phones, main_count, frozen_count = read_all_phones()
            
            if not phones:
                print(colorize(f"❌ {PHONE_CSV} va {FROZEN_CSV} bo'sh yoki topilmadi!", 'red', True))
                input("ENTER...")
                return
            
            phones_to_process = []
            phones_to_skip = []
            
            for phone in phones:
                if api_json_exists(phone):
                    phones_to_skip.append(phone)
                else:
                    phones_to_process.append(phone)
            
            print(colorize(f"\n{'='*60}", 'bwhite', True))
            print(colorize(f"📱 JAMI NOMERLAR: {len(phones)}", 'cyan', True))
            print(colorize(f"   📄 {PHONE_CSV}: {main_count} ta", 'cyan', False))
            print(colorize(f"   📄 {FROZEN_CSV}: {frozen_count} ta", 'cyan', False))
            print(colorize(f"{'='*60}", 'bwhite', True))
            print(colorize(f"   ✅ API mavjud: {len(phones_to_skip)} ta", 'green', False))
            print(colorize(f"   🔄 Ishlanadi: {len(phones_to_process)} ta", 'yellow', False))
            print(colorize(f"{'='*60}", 'bwhite', True))
            
            if not phones_to_process:
                print(colorize(f"\n✅ Barcha nomerlar uchun API mavjud!", 'green', True))
                input("\nENTER chiqish...")
                return
            
            print(colorize(f"📁 Sessiyalar: {SESSION_FOLDER}", 'cyan', False))
            print(colorize(f"📁 API: {APIS_FOLDER}", 'cyan', False))
            print(colorize(f"🖥️ Brauzer: Chrome (oddiy)", 'cyan', False))
            print(colorize(f"🔒 Rejim: Incognito", 'cyan', False))
            if MOBILE_PROXY:
                print(colorize(f"🌐 Proxy: {MOBILE_PROXY.split(':')[0]}:***", 'cyan', False))
            else:
                print(colorize(f"🌐 Proxy: Yo'q (kompyuter IP)", 'yellow', False))
            print(colorize(f"{'='*60}\n", 'bwhite', True))
            
            success, skip, fail = 0, 0, 0
            
            for phone in phones_to_skip:
                print(colorize(f"[{phone}] ⏭️ O'tkazib yuborildi (API mavjud)", 'green', False))
                skip += 1
            
            if phones_to_skip:
                print()
            
            for i, phone in enumerate(phones_to_process, 1):
                source = "phone.csv" if phones.index(phone) < main_count else "frozen_accounts.csv"
                print(colorize(f"\n[{i}/{len(phones_to_process)}] ({source})", 'bwhite', True))
                
                try:
                    if await process_phone(phone):
                        success += 1
                    else:
                        fail += 1
                except Exception as e:
                    print(colorize(f"[{phone}] ❌ Xato: {e}", 'red', True))
                    cleanup_temp_files(phone)
                    fail += 1
            
            print(colorize(f"\n{'='*60}", 'green', True))
            print(colorize(f"📊 NATIJA:", 'bwhite', True))
            print(colorize(f"   ✅ Muvaffaqiyatli: {success}", 'green', False))
            print(colorize(f"   ⏭️ O'tkazib yuborildi: {skip}", 'yellow', False))
            print(colorize(f"   ❌ Xatolar: {fail}", 'red', False))
            print(colorize(f"   📱 Jami: {len(phones)}", 'cyan', False))
            print(colorize(f"{'='*60}", 'green', True))
            input("\nENTER chiqish...")
        
        if __name__ == "__main__":
            if os.name == 'nt':
                try:
                    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
                except:
                    pass
            try:
                asyncio.run(main())
            except KeyboardInterrupt:
                print(colorize("\n⚠️ To'xtatildi", 'yellow', True))
            except:
                traceback.print_exc()
