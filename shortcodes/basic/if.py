import operator
class Shortcode():
	def __init__(self,Unprompted):
		self.Unprompted = Unprompted
		self.ops = {"==":self.Unprompted.is_equal,"!=":self.Unprompted.is_not_equal,"<":operator.lt,"<=":operator.le,">":operator.gt,">=":operator.ge}
	def run_block(self, pargs, kwargs, context, content):
		_not = "_not" in pargs
		_any = "_any" in pargs

		is_true = not _any

		# Normal expressions
		_is = kwargs["_is"] if "_is" in kwargs else "=="
		for key, value in kwargs.items():
			if (key[0] == "_"): continue # Skips system arguments

			this_value = self.Unprompted.parse_advanced(value,context)
			
			# Fix data type
			if (_is != "==" and _is != "!="):
				self.Unprompted.shortcode_user_vars[key] = float(self.Unprompted.shortcode_user_vars[key])
				this_value = float(this_value)
			
			if (self.ops[_is](self.Unprompted.shortcode_user_vars[key],this_value)):
				if _any:
					is_true = True
					break
			elif not _any:
				is_true = False
				break

		# Support advanced expressions
		for key in pargs:
			if (key[0] == "_"): continue # Skips system arguments
			if (self.Unprompted.parse_advanced(key,context) == 1):
				if _any:
					is_true = True
					break
			elif not _any:
				is_true = False
				break

		if ((is_true and not _not) or (_not and not is_true)):
			self.Unprompted.shortcode_objects["else"].do_else = False
			return(self.Unprompted.parse_alt_tags(content,context))
		else:
			self.Unprompted.shortcode_objects["else"].do_else = True
			return("")