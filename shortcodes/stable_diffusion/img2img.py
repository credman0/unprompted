class Shortcode():
	'''Runs an img2img task inside of an [after] block'''
	def __init__(self,Unprompted):
		self.Unprompted = Unprompted
	def run_atomic(self, pargs, kwargs, context):
		import modules.img2img
		from modules import sd_samplers

		if "mask_mode" not in self.Unprompted.shortcode_user_vars: self.Unprompted.shortcode_user_vars["mask_mode"] = 0
		init_mask = None
		if "init_mask" in self.Unprompted.shortcode_user_vars: init_mask = self.Unprompted.shortcode_user_vars["init_mask"]
		elif "init_mask_inpaint" in self.Unprompted.shortcode_user_vars: init_mask = self.Unprompted.shortcode_user_vars["init_mask_inpaint"]

		# TODO: There might be a function to retrieve sampler index from its name, if so use that instead
		for i in range(len(sd_samplers.samplers_for_img2img)):
			if sd_samplers.samplers_for_img2img[i].name == self.Unprompted.shortcode_user_vars["sampler_name"]:
				sampler_index = i
				break

		img2img_result = modules.img2img.img2img(
			self.Unprompted.shortcode_user_vars["mode"] if "mode" in self.Unprompted.shortcode_user_vars else 0, #p.mode
			self.Unprompted.shortcode_user_vars["prompt"],
			self.Unprompted.shortcode_user_vars["negative_prompt"],
			"None", #prompt_style1
			"None", #prompt_style2
			self.Unprompted.shortcode_user_vars["init_images"][len(self.Unprompted.after_processed.images) - 1],
			None, # p.init_img_with_mask
			None, # p.init_img_with_mask_orig
			self.Unprompted.shortcode_user_vars["init_images"][len(self.Unprompted.after_processed.images) - 1], # p.init_img_inpaint
			init_mask, # p.init_mask_inpaint
			self.Unprompted.shortcode_user_vars["mask_mode"],
			self.Unprompted.shortcode_user_vars["steps"],
			sampler_index,
			self.Unprompted.shortcode_user_vars["mask_blur"] if "mask_blur" in self.Unprompted.shortcode_user_vars else 0, # p.mask_blur
			0.0, #p.mask_alpha
			0, # p.inpainting_fill
			self.Unprompted.shortcode_user_vars["restore_faces"],
			self.Unprompted.shortcode_user_vars["tiling"],
			self.Unprompted.shortcode_user_vars["n_iter"] if "n_iter" in self.Unprompted.shortcode_user_vars else 1, #p.n_iter
			self.Unprompted.shortcode_user_vars["batch_size"] if "batch_size" in self.Unprompted.shortcode_user_vars else 1, #p.batch_size
			self.Unprompted.shortcode_user_vars["cfg_scale"],
			self.Unprompted.shortcode_user_vars["denoising_strength"] if self.Unprompted.shortcode_user_vars["denoising_strength"] is not None else 0.5,
			self.Unprompted.shortcode_user_vars["seed"],
			self.Unprompted.shortcode_user_vars["subseed"],
			self.Unprompted.shortcode_user_vars["subseed_strength"],
			self.Unprompted.shortcode_user_vars["seed_resize_from_h"],
			self.Unprompted.shortcode_user_vars["seed_resize_from_w"],
			0, # seed_enable_extras
			self.Unprompted.shortcode_user_vars["height"],
			self.Unprompted.shortcode_user_vars["width"],
			self.Unprompted.shortcode_user_vars["resize_mode"] if "resize_mode" in self.Unprompted.shortcode_user_vars else 0,
			self.Unprompted.shortcode_user_vars["inpaint_full_res"] if "inpaint_full_res" in self.Unprompted.shortcode_user_vars else True, # p.inpaint_full_res
			self.Unprompted.shortcode_user_vars["inpaint_full_res_padding"] if "inpaint_full_res_pdding" in self.Unprompted.shortcode_user_vars else 0, # p.inpaint_full_res_padding
			0, # p.inpainting_mask_invert
			"", #p.batch_input_directory
			"", #p.batch_output_directory
			0, # this is the *args tuple and I believe 0 indicates we are not using an extra script in img2img
		)

		# Get the image stored in the first index
		img2img_images = img2img_result[0]

		# Add the new image(s) to our main output
		self.Unprompted.after_processed.images.append(img2img_images[0])

		return("")