def do_install():
	import importlib, os
	spec = importlib.util.spec_from_file_location("unprompted_install", os.path.join(os.path.dirname(__file__), "install.py"))
	unprompted_install = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(unprompted_install)


do_install()

# Prep main object
import inspect, os, sys, time
import unprompted.lib_unprompted.shared

module_path = os.path.dirname(os.path.dirname(inspect.getfile(unprompted.lib_unprompted.shared.Unprompted)))

# Add the directory to your system's path
sys.path.insert(0, f"{module_path}")

Unprompted = unprompted.lib_unprompted.shared.Unprompted(module_path)
Unprompted.webui = "comfy"
Unprompted.NODE_VERSION = "0.2.2"


class UnpromptedNode:
	"""
	A example node

	Class methods
	-------------
	INPUT_TYPES (dict): 
		Tell the main program input parameters of nodes.
	IS_CHANGED:
		optional method to control when the node is re executed.

	Attributes
	----------
	RETURN_TYPES (`tuple`): 
		The type of each element in the output tulple.
	RETURN_NAMES (`tuple`):
		Optional: The name of each output in the output tulple.
	FUNCTION (`str`):
		The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run Example().execute()
	OUTPUT_NODE ([`bool`]):
		If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
		The backend iterates on these output nodes and tries to execute all their parents if their parent graph is properly connected.
		Assumed to be False if not present.
	CATEGORY (`str`):
		The category the node should appear in the UI.
	execute(s) -> tuple || None:
		The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
		For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
	"""

	def __init__(self):
		pass

	@classmethod
	def INPUT_TYPES(s):
		"""
		Return a dictionary which contains config for all input fields.
		"""
		return {
		    "required": {
		        "string_field": (
		            "STRING",
		            {
		                "multiline": True,  # True if you want the field to look like the one on the ClipTextEncode node
		                "default": "This string will be parsed with the Unprompted language."
		            }),
		    },
		    "optional": {
		        "anything": ("*", {
		            "default": None
		        }),
		        "set_anything_to": ("STRING", {
		            "default": "comfy_var"
		        }),
		        "return_image_var": ("STRING", {
		            "default": "comfy_var",
		        }),
		        "always_rerun": ("BOOLEAN", {
		            "default": False
		        }),
		        "string_prefix": ("STRING", {
		            "forceInput": True,
		            "default": ""
		        }),
		        "string_suffix": ("STRING", {
		            "forceInput": True,
		            "default": ""
		        }),
		    }
		}

	RETURN_TYPES = (
	    "STRING",
	    "IMAGE",
	)
	#RETURN_NAMES = ("image_output_name",)

	FUNCTION = "do_unprompted"

	#OUTPUT_NODE = False

	# CATEGORY = "Example"

	def do_unprompted(self, **kwargs):
		Unprompted.shortcode_user_vars = {}

		if kwargs.get("anything") is not None:
			Unprompted.shortcode_user_vars[kwargs.get("set_anything_to")] = kwargs.get("anything")

		result = Unprompted.start(kwargs.get("string_prefix", "") + kwargs.get("string_field", "") + kwargs.get("string_suffix", ""))

		image_result = None
		if kwargs.get("return_image_var"):
			image_var = kwargs.get("return_image_var")
			if image_var in Unprompted.shortcode_user_vars:
				image_result = Unprompted.shortcode_user_vars[image_var]

		# Cleanup routines
		Unprompted.cleanup()
		Unprompted.goodbye()

		return (
		    result,
		    image_result,
		)

	"""
		The node will always be re executed if any of the inputs change but
		this method can be used to force the node to execute again even when the inputs don't change.
		You can make this node return a number or a string. This value will be compared to the one returned the last time the node was
		executed, if it is different the node will be executed again.
		This method is used in the core repo for the LoadImage node where they return the image hash as a string, if the image hash
		changes between executions the LoadImage node is executed again.
	"""

	#@classmethod
	def IS_CHANGED(**kwargs):
		if kwargs.get("always_rerun") is True:
			return str(time.time())


# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {"Unprompted": UnpromptedNode}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {"Unprompted": f"Unprompted v{Unprompted.NODE_VERSION}"}
