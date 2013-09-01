import os
import sys
import glob
import jinja2
import shutil
import pkgutil
import importlib

# TODO: refactor!
class Site:
	def __init__(self, package_name, output_path, template_dir='templates', static_path='static'):
		self.package_name = package_name
		self.output_path = output_path
		
		module = importlib.import_module(self.package_name)
		self.static_path = os.path.join(os.path.dirname(module.__file__), static_path)

		self.env = jinja2.Environment(loader=jinja2.PackageLoader(package_name, template_dir))

	def write_template(self, name, context, destination):
		template = self.env.get_template(name)

		destination, file_name = os.path.split(os.path.join(self.output_path, destination, os.path.basename(name)))
		if not os.path.exists(destination):
			os.makedirs(destination)

		# we're generating a static site - in order to make the urls 'nice', always sue index.html in a corresponding dir
		file_name = 'index.html'

		print('[=> Writing] {0} to {1}'.format(name, destination))

		f = open(os.path.join(destination, file_name), mode='w', encoding='utf-8')
		try:
			f.write(template.render(context))
		except jinja2.exceptions.UndefinedError as e:
			print('\033[91m[Error]\033[0m Context error {0} in {1}'.format(e.args[0], os.path.join(destination, file_name)))

	def clear_build_dir(self):
		print('[Clearing] {0}'.format(self.output_path))
		if os.path.exists(self.output_path):
			shutil.rmtree(self.output_path)

	def collect_static_content(self, path, destination, allowed=['.png', '.jpg', '.jpeg', '.gif']):
		statics = []
		for ext in allowed:
			statics += glob.glob(path + '/*' + ext)

		for s in statics:
			shutil.copyfile(s, os.path.join(self.output_path, destination, os.path.basename(s)))

	def generate_templates(self, content_name = 'content'):

		def get_content_tree(name):
			c = importlib.import_module('.' + content_name, name)
			root = [c.__name__]
			children = [c for _, c, _ in pkgutil.walk_packages(c.__path__, c.__name__ + '.')]

			return sorted(root + children)
		def get_fallback_template(t, templates):

			def one_up(path):
				h, t = os.path.split(path)
				h, _ = os.path.split(h)
				return os.path.join(h, t).replace('\\', '/') # normalize with jinja paths

			f = one_up(t)
			while f != t:
				if f in templates:
					return f
				f = one_up(f)

			return 'index.html'

		content = get_content_tree(self.package_name)

		# every template that starts with '_' is treated as a master(ish) template		
		templates = sorted(self.env.list_templates(filter_func=lambda x: not x.startswith('_')), reverse=True)

		for c in content:
			x = importlib.import_module(c)
			ctx = {var: getattr(x, var) for var in dir(x) if not var.startswith('_')}

			# get template name
			t = c.replace(self.package_name + '.' + content_name, '')
			t = t.replace('_', '-')
			t = t.replace('.', '/')

			# module 'style' - foo.html
			tm = t + '.html' if len(t) > 0 else '.'

			# package 'style' - <foo>/index.html
			t += '/index.html'

			#remove trailing characters
			t = t[1:]
			tm = tm[1:]

			destination = os.path.dirname(t)

			print('[Processing] {0}'.format(c))

			if len(tm) > 0 and tm in templates:
				self.write_template(tm, ctx, destination)
			elif t in templates:
				self.write_template(t, ctx, destination)
			else:
				fallback = get_fallback_template(t, templates)
				self.write_template(fallback, ctx, destination)

			self.collect_static_content(x.__path__[0] if hasattr(x, '__path__') else os.path.dirname(x.__file__), destination)

	def copy_statics(self):
		print('[Statics] {0}'.format(self.static_path))
		shutil.copytree(self.static_path, self.output_path)

	def build(self):
		self.clear_build_dir()
		self.copy_statics()
		self.generate_templates()

def main():
	if len(sys.argv) < 2:
		print('Package parameter missing')
		exit()

	this_dir = os.path.abspath(os.path.dirname(__file__))
	output_path = os.path.join(this_dir, sys.argv[2] if len(sys.argv) > 2 else 'build')

	site = Site(sys.argv[1], output_path)
	site.build()
    
if __name__ == '__main__':
    main()
