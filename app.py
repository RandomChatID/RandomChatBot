import telepot
import random
import time
import os
import json

token = "2107328374:AAGvzAomH66zLYHz91mEbYPb0divk36hrPY"
bot = telepot.Bot(token)

queue = {
	"free":[],
	"occupied":{}
}

def saveConfig(data):
	return open('config.json', 'w').write(json.dumps(data))

if __name__ == '__main__':
	s = time.time()
	print('[#] Swirlbot 2\n[i] Created by sadnesstalk - @sadnesstalk\n')
	print('[#] Checking config...')
	if not os.path.isfile('config.json'):
		print('[#] Creating config file...')
		open('config.json', 'w').write('{}')
		print('[#] Done')
	else:
		print('[#] Config found!')
	print('[i] Bot online ' + str(time.time() - s) + 's')
def exList(list, par):
	a = list
	a.remove(par)
	return a

def handle(update):
	global queue
	try:
		config = json.loads(open('config.json', 'r').read())
		if 'text' in update:
			text = update["text"]
		else:
			text = ""
		uid = update["from"]["id"]

		if not uid in config and text != "/nopics":
			config[str(uid)] = {"pics":True}
			saveConfig(config)

		if uid in queue["occupied"]:
			if 'text' in update:
				if text != "/end":
					bot.sendMessage(queue["occupied"][uid], "Stranger 🌸: " + text)
			
			if 'photo' in update:
				if config[str(queue["occupied"][uid])]["pics"]:
					photo = update['photo'][0]['file_id']
					bot.sendPhoto(queue["occupied"][uid], photo)
					bot.sendMessage(queue["occupied"][uid], "Stranger mengirimi anda foto 📷!")
				else:
					bot.sendMessage(queue["occupied"][uid], "Stranger mencoba mengirimi anda foto, tapi kamu menonaktifkan ini, Anda dapat mengaktifkan foto dengan menggunakan perintah /nopics")
					bot.sendMessage(uid, "Stranger foto yang dinonaktifkan, dan tidak akan menerima foto anda")

			if 'video' in update:
				video = update['video']['file_id']
				bot.sendVideo(queue["occupied"][uid], video)
				bot.sendMessage(queue["occupied"][uid], "Stranger mengirimi anda video 🎥!")

			if 'sticker' in update:
				sticker = update['sticker']['file_id']
				bot.sendDocument(queue["occupied"][uid], sticker)
				bot.sendMessage(queue["occupied"][uid], "Stranger mengirimi anda stiker 🖼️!")

		if text == "/end" and uid in queue["occupied"]:
			print('[SB] ' + str(uid) + ' Keluar percakapan dengan ' + str(queue["occupied"][uid]))
			bot.sendMessage(uid, "Percakapan anda selesai, Saya harap anda menikmatinya :)")
			bot.sendMessage(uid, "Ketik /start untuk dicocokkan dengan pasangan baru")
			bot.sendMessage(uid, "Kami mengakhiri percakapan...")
			bot.sendMessage(queue["occupied"][uid], "Percakapan Anda selesai, Saya harap Anda menikmatinya :)")
			bot.sendMessage(queue["occupied"][uid], "Mitra percakapan anda meninggalkan obrolan")
			del queue["occupied"][queue["occupied"][uid]]
			del queue["occupied"][uid]

		if text == "/start":
			if not uid in queue["occupied"]:
				bot.sendMessage(uid, 'Mencari stranger yang cocok denganmu... Tunggu!')
				print("[SB] " + str(uid) + " bergabung dalam antrian")
				queue["free"].append(uid)

		if text == "/help":
			bot.sendMessage(uid, "Help:\n\nMenggunakan /start untuk mulai mencari pasangan percakapan, setelah kamu cocok, anda dapat menggunakan /end untuk mengakhiri percakapan.\n\nJika anda memiliki pertanyaan atau memerlukan bantuan, join @sadnesstalk atau bertanya @sadnesstalk.\n@antigabutbrothers")

		if text == "/nopics":
			config[str(uid)]["pics"] = not config[str(uid)]["pics"] 
			if config[str(uid)]["pics"]:
				bot.sendMessage(uid, "Strangers sekarang dapat mengirimi anda foto!")
			else:
				bot.sendMessage(uid, "Strangers tidak akan dapat mengirimi anda foto lagi!")
			saveConfig(config)

		if len(queue["free"]) > 1 and not uid in queue["occupied"]:
			partner = random.choice(exList(queue["free"], uid))
			if partner != uid:
				print('[SB] ' + str(uid) + ' matched with ' + str(partner))
				queue["free"].remove(partner)
				queue["occupied"][uid] = partner
				queue["occupied"][partner] = uid
				bot.sendMessage(uid, 'Anda telah cocok, bersenang-senang!')
				bot.sendMessage(partner, 'Anda telah cocok, bersenang-senang!')
	except 	Exception as e:
		print('[!] Error: ' + str(e))

if __name__ == '__main__':
	bot.message_loop(handle)

	while True:
		time.sleep(10)
