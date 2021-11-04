import json,os,datetime,time
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetParticipantsRequest, GetFullChannelRequest, InviteToChannelRequest
from telethon.tl.types import InputPeerEmpty, ChannelParticipantsSearch,UserStatusOffline, UserStatusRecently, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError

lgr = "\033[90m"
lr = "\033[91m"
lg = "\033[92m"
ly = "\033[93m"
lb = "\033[94m"
lc = "\033[96m"
lx = "\033[0m"

def banner(user=None):
	user = user.get_me().first_name if user else "User"
	banner_text = f"""{lc}

[̲̅M][̲̅R] [̲̅L][̲̅O][̲̅M][̲̅B][̲̅E][̲̅N][̲̅K] {ly}SPJ
{lgr}By Mr Lombenk Production SPJ 
{lg}Welcome {ly}{user}{lg} !
{lx}"""
	os.system('clear')
	print(banner_text)
def loading(delay):
	rg = delay
	for i in range(rg):
		try:
			print(f"\r{lgr}    Tajeng Jolo Campe Boss!!! ({rg-(i+1)}s){lx}",end="",flush=True)
			time.sleep(1)
		except:
			exit()
	print()
def date_format(message):
	"""
	:param message:
	:return:
	"""
	if type(message) is datetime:
		return message.strftime("%Y-%m-%d %H:%M:%S")
def paginate(data,col=2):
	n_data = round(len(data)/col) + 1
	new_data_part = []
	batas = 0
	for i in range(n_data):
		new_data = []
		for x in range(batas,col+batas):
			try:
				new_data.append(data[x])
			except:
				pass
			batas += 1
		if new_data: new_data_part.append(new_data)
	return new_data_part

def init():
	banner()
	try:
		os.mkdir(".tmp")
	except:
		pass
	try:
		os.mkdir(".users")
	except:
		pass
	try:
		os.mkdir("results")
	except:
		pass

	if not "user.config" in os.listdir(".tmp"):
		json.dump({"phone":None},open(".tmp/user.config","w"))
	phone = json.load(open(".tmp/user.config"))['phone']
	if not phone:
		list_user = os.listdir(".users")
		if not list_user:
			phone = input(f"{lg}[*]{lx} Nomorta Gare (ex:+62812..): ")
			while not "+62" in phone:
				print(f'{lr}[*]{lx} Harus Awalannya  +62 Ta Pahanni bos?!!!')
				phone = input(f"{lg}[*]{lx}Nomorta Gare (ex:+62812..): ")
		else:
			print(f"{lg}[*]{lx} Purani Tama akun e Sebelumnya.\nPilih User")
			for usr in list_user:
				print(f"   {lg}{n}.{lx} {usr}")
				n += 1
			us = input(f"{lg}[*]{lx} Pilih atau ENTER Masuk Akun Laingge ")
			if us:
				cred = json.load(open(f".users/{list_user[int(us)-1]}"))
				phone = "+"+cred["phone"]
			else:
				phone = input(f"{lg}[*]{lx} Nomorta Gare (ex:+62812..): ")
				while not "+62" in phone:
					print(f'{lr}[*]{lx} Harus Awalannya  +62 Ta Pahanni bos?!!!')
					phone = input(f"{lg}[*]{lx}Nomorta Gare (ex:+62812..): ")
	client = login(phone)
	main_menu(client)
def main_menu(client):
	banner(client)
	print(f"""
    Select Menu
    
1. Tambahkan Ke Groupta 
2. Dapatkan Id Member Group
3. Menu Akun
4. Reset Robot
5. Exit
""")
	menu = input(f"{lg}[*]{lx} Input Menu : ")
	if menu in ["1","01"]:
		menu_add_members(client)
	elif menu in ["2","02"]:
		get_group_members(client)
	elif menu in ["3","03"]:
		menu_account(client)
	elif menu in ["4","04"]:
		dlt = input("Reset Robot ? [y/n]: ")
		if dlt == "y":
			try:
				os.system("rm -rf .tmp")
				os.system("rm -rf .users")
				os.system("rm -rf results")
				os.system("rm  *.session")
			except:
				pass
	else:
		exit()
def menu_account(client):
	user = client.get_me()
	banner(client)
	print("""
1. Detail Akun Saat ini
2. Tambahkan Akun Baru
3. Pindah ke Akun Lain
4. Hapus Akun

Enter to back
""")
	opt = input(f"{lg}[*]{lx} Select Menu : ")
	if opt == "1":
		uid = user.id if user.id else "-"
		ufname = user.first_name if user.first_name else "-"
		ulname = user.last_name if user.last_name else "-"
		uname = "@"+user.username if user.username else "-"
		uphone = "+"+user.phone if user.phone else "-"
		detail = f"""
[̲̅M][̲̅R] [̲̅L][̲̅O][̲̅M][̲̅B][̲̅E][̲̅N][̲̅K]
{lg}--------------------{lx}

ID           : {uid}
First Name   : {ufname}
Last Name    : {ulname}
Username     : {uname}
Phone Number : {uphone}
"""
		print(detail)
		input("Enter to back ")
		menu_account(client)

	elif opt == "2":
		phone = input(f"{lg}[*]{lx}Nomorta Gare (ex:+62812..): ")
		client = login(phone)
		main_menu(client)
	elif opt == "3":
		n = 1
		list_user = os.listdir(".users")
		if len(list_user) != 0:
			print(f"{lg}[*]{lx} Select User")
			for usr in list_user:
				print(f"   {lg}{n}.{lx} {usr}")
				n += 1
			us = input(f"{lg}[*]{lx} Select: ")
			if us:
				cred = json.load(open(f".users/{list_user[int(us)-1]}"))
				phone = "+"+cred["phone"]
				if cred["phone"] == user.phone:
					print(f"{ly}[*]{lx} Ini adalah akun login Anda saat ini. Pilih yang lain atau tambahkan akun baru")
					exit()
				else:
					client = login(phone)
					main_menu(client)
					
		else:
			print(f"{ly}[*]{lx} Dewiddeng Tama. Loginki Jolo Bos!!!")
			exit()
			
	elif opt == "4":
		n = 1
		list_user = os.listdir(".users")
		if len(list_user) != 0:
			print(f"{lg}[*]{lx} Select Account To Delete")
			for usr in list_user:
				print(f"   {lg}{n}.{lx} {usr}")
				n += 1
			us = input(f"{lg}[*]{lx} Select: ")
			if us:
				cred = json.load(open(f".users/{list_user[int(us)-1]}"))
				phone = "+"+cred["phone"]
				if cred["phone"] == user.phone:
					dlt = input(f"{ly}[*]{lx} Ini adalah akun login Anda saat ini. Menghapus ? [y/n] : ")
					if dlt != "y":
						exit()
				print(f"{lg}[*]{lx} Deleting {cred['first_name']} account..")
				sess = phone + ".session"
				os.remove(sess)
				os.remove(f".users/{list_user[int(us)-1]}")
				os.remove(f".tmp/user.config")
				print(f"{lg}[*]{lx} Done !")
				exit()

		else:
			print(f"{ly}[*]{lx} Belumpaki Je itu Masuk e, Loginki Dulu Bos !!!")
			exit()
	else:
		main_menu(client)
		
		
def menu_add_members(client):
	banner(client)
	print(f"{lr}NOTE: {lx}Ini adalah alat Mr Lombenk. Menggunakan alat ini berarti Dewedding abbereang akko tania Anggota MR LOMBENK #PAGGURIKIE ")
	print(f"{ly}TIPS: {lx}Gunakan alat ini dengan benar. maksimum menambahkan pengguna ke grub adalah 200 orang per akun. Setiap 50 pengguna, akun akan dibatasi hingga ±15 menit untuk menambahkan pengguna berikutnya. Jika ini terjadi pada akun Anda, silakan gunakan akun lain.")
	#print(f"\n\n{lg}[*]{lx} Enter limit of add member (max 200/account) or pass to use default limit (50)")
	#limit = input(f"{lg}   > {lx}")
	print(f"{lg}[*]{lx} Kita kasih Masuk dulu waktu tunda dalam hitungan detik Supaya Dena Drop Server e Boskuuu Ladde!! (60 detik)")
	delay = input(f"{lg}   > {lx}")
	if delay:
		print(f"{lg}[*]{lx} Gunakan Kostum Delay ({delay}s)")
		add_member(client,delay=int(delay))
	#elif limit and not delay:
	#	print(f"{lg}[*]{lx} Use custom limit ({limit} users) and default delay (60s)")
	#	add_member(client,limit=int(limit))
	#elif delay and not limit:
	#	print(f"{lg}[*]{lx} Use default limit (50 users) and custom delay ({delay}s)")
	#	add_member(client,delay=int(delay))
	else:
		print(f"{lg}[*]{lx} Gunakan Default Delay (60s)")
		add_member(client)
		
	

def login(phone=None):
	print(f"{lg}[*]{lx} Login..")
	api_id = 19619354
	api_hash = '10659065b0f3e0be75a2050225e596da'
	try:
		client = TelegramClient(phone, api_id, api_hash)
		client.connect()
		if not client.is_user_authorized():
			client.send_code_request(phone)
			client.sign_in(phone, input(f'{lg}[*]{lx} Kita Kasih Masuk Gare Kodenya : '))
		json.dump({"phone":phone},open(".tmp/user.config","w"))
		json.dump(client.get_me().to_dict(), open(f".users/{client.get_me().first_name}-{client.get_me().id}.json","w"), default=date_format)
		user = client.get_me()
		user_name = user.first_name
		return client
	except Exception as e:
		print(f"{lr}[*]{lx} Error Login E {ly}{e}{lx}")
		
def isActive(user):
	is_active = False
	status = user.status
	if isinstance(status, UserStatusOffline):
		return (datetime.datetime.now(tz=datetime.timezone.utc) - status.was_online) <= datetime.timedelta(days=1)
	elif isinstance(status,UserStatusRecently):
		return True
	else:
		return False
		
def get_group_list(client,add=False):
	chats = []
	last_date = None
	chunk_size = 200
	groups=[]
	result = client(GetDialogsRequest(
				offset_date=last_date,
				offset_id=0,
				offset_peer=InputPeerEmpty(),
				limit=chunk_size,
				hash = 0
				))
	chats.extend(result.chats)
	for chat in chats:
		dik = chat.to_dict()
		# check if chat type is group, not channel
		if "invite_users" in str(dik):
			#print(json.dumps(dik, default=date_format,indent=2))
			if add:
				if dik["admin_rights"]:
					groups.append(chat)
			else:
				if not dik["admin_rights"]:
					groups.append(chat)
	if len(groups) != 0:
		index = 1
		print(f"{lg}[*] {lx}Daftar Groupta \n")
		for i in groups:
			print(f"    {lg}{index}.{lx} {i.title} ({ly}{i.participants_count} {lx}members)")
			index +=1
		sl = input(f"\n{lg}[*] {lx}Pilihki Group: ")
		if not sl:
			main_menu(client)
		else:
			sltd = groups[int(sl) - 1]
			return sltd
	else:
		if add:
			print(f"{ly}[*]{lx} BelumPaki Bikin Group.\nBuatki dulu Group dan Menjadi ADMIN")
		else:
			print(f"{ly}[*]{lx} Belum bisaki join digroup ini \nJoinki dulu 1 group dan kita coba kembali")
		exit()
			
def get_group_members(client):
	sltd = get_group_list(client)
	print(f"{lg}[*]{lx} Fetching {ly}{sltd.title}{lx} Anggota Aktif e  {lc}{sltd.participants_count}{lx} Total Member")
	members = []
	all_members = client.get_participants(sltd, aggressive=True)
	for member in all_members:
		u_id = member.id
		u_hash = member.access_hash
		f_name = member.first_name if member.first_name else ""
		l_name = member.last_name if member.last_name else ""
		u_name = member.username if member.username else ""
		u_phone = member.phone if member.phone else ""
		data = {
				"first_name":f_name,
				"last_name":l_name,
				"username":u_name,
				"id":u_id,
				"hash":u_hash,
				"phone":u_phone
				}
		if isActive(member):
			members.append(data)
			print(f"\r{lg}[*] {lx}Mengambil Anggota Aktif ni Robot e: {ly}{round((len(members)/sltd.participants_count) * 100,2)}%{lx}..",end="",flush=True)
	print(f"\n{lg}[*] {ly}{round((len(members)/sltd.participants_count) * 100,2)}%{lx} ({lc}{len(members)}{lx}) Anggota aktif Sudah di Ambil Bosku !!!")
	sv = input(f"{lg}[*]{lx} Simpan Sebagai Default (members-{sltd.title}.json) or Kostum ? [d/c]: ")
	if sv.upper() == "D":
		fname = f"members-{sltd.title}.json"
	else:
		fname = input(f"{lg}[*]{lx} Enter file name (ex: myid.json) : ")
	print(f"{lg}[*]{lx} Saving result as \"{ly}results/{fname}{lx}\"..")
	json.dump({"amounts":len(members),"data":members},open(f"results/{fname}","w"),indent=2)
	print(f"{lg}[*]{lx} Done!\nFile saved as {ly}{fname}{lx}")
	exit()

def add_member(client,limit=50,delay=60):
	print(f"{lg}[*]{lx} Pilihki dulu group yang mau kt tambahkan")
	selected_group = get_group_list(client,add=True)
	target_group = InputPeerChannel(selected_group.id,selected_group.access_hash)
	if os.listdir("results"):
		print(f"{lg}[*]{lx} Pilih ID ?")
		index = 1
		for i in os.listdir("results"):
			print(f"    {lg}{index}.{lx} {i}")
			index += 1
		sltd_id = json.load(open("results/"+os.listdir("results")[int(input(f"{lg}[*]{lx} Select: ")) -1]))
		print(f"{lg}[*]{lx} {ly}{len(sltd_id['data'])}{lx} ID loaded !")
		n = 1
		member_part = paginate(sltd_id["data"],50)
		"""
		indx = 1
		start = 1
		print(f"{lg}[*]{lx} Select index of ID from ID list")
		for data in member_part:
			number = f"{lg}{format(indx,str(len(str(len(member_part)))))}. {lx}"
			print(number,end="")
			indx += 1
			part = f"{format(start,str(len(str(len(sltd_id['data'])))))} {ly}-{lx} {start + len(data) - 1}"
			start += len(data)
			print(part)
		print()
		slx = input(f"{lg}[*]{lx} Select index: ")
		slxtd = member_part[int(slx)-1]
		"""
		print(f"{lg}[*]{lx} Input index (ex: 100-200)")
		idx = input(f"{lg}[*]{lx} Input: ")
		start,end = idx.split("-")
		slxtd = sltd_id["data"][int(start)-1:int(end)-1]
		print(f"{lg}[*]{lx} {len(slxtd)} IDs selected")
		print(f"{lg}[*]{lx} Starting !")
		for user in slxtd:
			try:
				user_to_add = InputPeerUser(user['id'], user['hash'])
				print(f'  {lg}{n}.{lx} Add {lc}{user["first_name"]} {user["last_name"]}{lx} to {lc}{selected_group.title}{lx}..')
				n += 1
				client(InviteToChannelRequest(target_group,[user_to_add]))
				loading(delay)
			except UserPrivacyRestrictedError:
				print(f"    {lr}!{lx} Iyena iyehe Pasolangi Robot e , Naruntu sih Privasi Telegram na.")
				continue
			except Exception as e:
				print(f"    {lr}!{lx} Error i : {ly}{e}{lx}")
				continue
	else:
		print(f"{ly}[*]{lx} Belumpaki punya ID List.")
		get_group_members(client)
		add_member(client)
init()


