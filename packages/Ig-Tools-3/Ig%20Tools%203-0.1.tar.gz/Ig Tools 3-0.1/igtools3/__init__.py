from .request import get, post, sess
from .exception import LoginError
from .core import randomAgent
import json
from bs4 import BeautifulSoup as bs

class Session:
	def __init__(self):
		self.is_login = False
		self.s = sess()
		self.base = "https://instagram.com"
		self.url = self.base + "/accounts/login/ajax"
		self.csrf = self.s.get(self.base).cookies["csrftoken"]
		self.headers = {
			'origin':'https://www.instgram.com',
			'pragma':'no-cache',
			'referer':'https://www.instagram.com/account/login/',
			'user-agent':randomAgent(),
			'x-csrftoken':self.csrf,
			'x-requested-with':'XMLHttpRequest'
		}

	def login(self, user, pwd):
		data = {"username":user, "password":pwd,'queryParams':'{}'}
		self.s.headers = self.headers
		login = self.s.post(self.url, data=data)
		if '"authenticated": true' in login.text:
			self.is_login = True
			return True
		else:
			raise LoginError("Failed Login")

	def get_info(self, name):
		data = {}
		r = get("http://www.insusers.com/"+name+"/followers", headers={"User-Agent":randomAgent()})
		b = bs(r.text, "html.parser")
		for a in b.findAll("li"):
			dat = a.find("a")
			if "followings" in str(dat.get("href")):
				data["followings"] = a.text
			if "followers" in str(dat.get("href")):
				data["followers"] = a.text
		for title in b.findAll("div", {"class":"prright"}):
			data["title"] = str(title).replace("<p>", "").replace("</p>", "").replace("<br/>", "\n").replace('<div class="prright">', '').replace("</div>","")
		return data
