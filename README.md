# [CSAwesome](https://csawesome.runestone.academy/runestone/books/published/csawesome/index.html) to [Repl.it](https://repl.it/)

Because the code editor in CSAwesome isn't very feature-rich, this project arose out of a need to mass-create Repl.it projects from CSAwesome activities.

## How to Use:

1. Download the project and its dependencies:
	```
	$ git clone https://github.com/jadenPete/csawesome_to_replit.git
	$ cd csawesome_to_replit
	$ poetry install
	```
2. Install Firefox and geckodriver:
	* Arch Linux: `# pacman -S firefox geckodriver`
	* Ubuntu: `# apt install firefox firefox-geckodriver`
2. Create `login.txt` and copy the contents of the `connect.sid` cookie from Repl.it into it:
3. Run `./main.py` with the URL of a CSAwesome lesson; e.g.:
	```
	$ ./main.py 'https://csawesome.runestone.academy/runestone/books/published/csawesome/Unit1-Getting-Started/topic-1-2-java-intro.html'
	```
