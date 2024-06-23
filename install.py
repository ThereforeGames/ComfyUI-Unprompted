print("### ComfyUI-Unprompted: Check dependencies")
import os, re, threading, locale, subprocess, sys, pkg_resources
from packaging import version

this_path = os.path.dirname(os.path.realpath(__file__))
debug = False

# Code for pip_install and is_installed comes from ComfyUI-Impact-Pack (install.py)
# (Why doesn't ComfyUI provide these functions natively?)

if "python_embeded" in sys.executable or "python_embedded" in sys.executable:
	pip_install = [sys.executable, "-s", "-m", "pip", "install", "--upgrade"]
else:
	pip_install = [sys.executable, "-m", "pip", "install", "--upgrade"]


def handle_stream(stream, is_stdout):
	stream.reconfigure(encoding=locale.getpreferredencoding(), errors='replace')

	for msg in stream:
		if is_stdout:
			print(msg, end="", file=sys.stdout)
		else:
			print(msg, end="", file=sys.stderr)


def process_wrap(cmd_str, cwd=None, handler=None):
	print(f"[Impact Pack] EXECUTE: {cmd_str} in '{cwd}'")
	process = subprocess.Popen(cmd_str, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1)

	if handler is None:
		handler = handle_stream

	stdout_thread = threading.Thread(target=handler, args=(process.stdout, True))
	stderr_thread = threading.Thread(target=handler, args=(process.stderr, False))

	stdout_thread.start()
	stderr_thread.start()

	stdout_thread.join()
	stderr_thread.join()

	return process.wait()


pip_list = None


def get_installed_packages():
	global pip_list

	if pip_list is None:
		try:
			result = subprocess.check_output([sys.executable, '-m', 'pip', 'list'], universal_newlines=True)
			pip_list = set([line.split()[0].lower() for line in result.split('\n') if line.strip()])
		except subprocess.CalledProcessError as e:
			print(f"[ComfyUI-Unprompted] Failed to retrieve the information of installed pip packages.")
			return set()

	return pip_list


def is_installed(name):
	name = name.strip().split("@")[0]  # Split the name at '@' and take the first part
	pattern = r'([^<>!=]+)([<>!=]=?)'
	match = re.search(pattern, name)

	if match:
		name = match.group(1)

	result = name.lower() in get_installed_packages()
	return result


requirements = os.path.join(this_path, "requirements.txt")
with open(requirements) as file:
	for package in file:
		try:
			# package_with_comment = package.split("#", 1)
			# package = package_with_comment[0].strip()
			# reason = package_with_comment[1].strip()

			if "==" in package:
				package_name, package_version = package.split("==")
				if "@" in package_name:
					package = package_name
					package_name = package_name.strip().split("@")[0]
				try:
					installed_version = pkg_resources.get_distribution(package_name).version
					if version.parse(installed_version) < version.parse(package_version):
						print(f"Upgrading `{package_name}` from {installed_version} to {package_version}")
						process_wrap(pip_install + [package])
				except pkg_resources.DistributionNotFound:
					# Package is not installed, install it
					process_wrap(pip_install + [package])
			elif not is_installed(package):
				process_wrap(pip_install + [package])
		except Exception as e:
			print(e)
			print(f"(ERROR) Failed to install {package} dependency for Unprompted.")
			pass
