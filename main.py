#!/usr/bin/env python

import datetime
import re
import requests
import selenium
from selenium import webdriver
import sys

options = webdriver.firefox.options.Options()
options.headless = True

wd = webdriver.Firefox(options=options)

with open("login.txt") as file:
	cj = requests.cookies.RequestsCookieJar()
	cj.set("connect.sid", file.readline())

	session = requests.Session()
	session.cookies = cj

class Repl:
	def __init__(self, title):
		response = session.post("https://repl.it/data/repls/new", data={
			"language": "java10",
			"title": title
		}, headers={
			"Referer": "https://repl.it/",
			"X-Requested-With": "XMLHttpRequest"
		}).json()

		try:
			self.id_ = response["id"]
			self.url = f"https://repl.it{response['url']}"
		except KeyError:
			print(response["message"])

			sys.exit(1)

	def write(self, filename, data):
		timestamp = datetime.datetime.now().timestamp() * 1000
		response = session.get(f"https://repl.it/data/repls/signed_urls/{self.id_}/{filename}?d={timestamp:.0f}").json()
		requests.put(response["urls_by_action"]["write"], data=data.encode("utf-8"))

main_method = re.compile(r"^[ \t]*public +static +void +main", re.M)
main_class = re.compile(r"^[ \t]*(?:public +)?class +([a-zA-Z]+[a-zA-Z\d_]*)", re.M)

def handle_url(url):
	wd.get(url)

	for element in wd.find_elements_by_css_selector(".ac_section > .ac_section"):
		code = wd.execute_script("return arguments[0].CodeMirror.getValue()", element.find_element_by_class_name("CodeMirror"))

		# Find the name of the main class
		if method_match := main_method.search(code):
			class_match = None

			for class_match in main_class.finditer(code[:method_match.start()]):
				pass
		else:
			class_match = main_class.search(code)

		# (E.g. "Activity: 8.1.4.2 ActiveCode (2DArrayCreate)" -> "8.1.4.2 Activity")
		caption = re.search(r"[0-9]+(?:\.[0-9]+)*", element.find_element_by_class_name("runestone_caption").text).group(0) + " Activity"

		# Create the repl
		repl = Repl(caption)

		if class_match is None:
			repl.write("Main.java", code)
		else:
			repl.write(f"{class_match.group(1)}.java", code)
			
			repl.write("Main.java", (
				"public class Main {\n"
				"	public static void main(String[] args) {\n"
				f"		{class_match.group(1)}.main(args);\n"
				"	}\n"
				"}\n"
			))

		print(repl.url)
	
	try:
		handle_url(wd.find_element_by_css_selector("#relations-next > a").get_attribute("href"))
	except selenium.common.exceptions.NoSuchElementException:
		pass

handle_url(sys.argv[1])
